

# TODO:
# * Implement normalize func
# * Attempt to google wiki \"...\" part of question
# * Rid of common appearances in 3 options
# * Automate screenshot process
# //Script is in working condition at all times
# //TODO is for improving accuracy


# answering bot for Live Quiz
import json
import urllib.request as urllib2
from bs4 import BeautifulSoup
from google import google
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import pyscreenshot as Imagegrab
import signal
import sys
import functools
import np
import time, threading
from os import listdir
from os.path import isfile, join
from multiprocessing import Process, Manager
from threading import Thread
# import wx
from halo import Halo

from telegram.ext import *
import requests
import re


# for terminal colors 
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# list of words to clean from the question during google search
remove_words = []

# negative words
negative_words = []


def handle_exceptions(func):
    """ This function is used as a decorator to wrap the implemented method avoiding weird crashes"""
    @functools.wraps(func)  # supports introspection
    def wrapper_decorator(*args, **kwargs):
        try:
            value = func(*args, **kwargs)
            return value
        except Exception as e:
            print("Something went wrong ...")
            print(e)
    return wrapper_decorator


def load_settings():
    """ Loads all the configuration of the application.

    It loads the words to be removed and the negative words from the settings.json file;
    it also gets and returns the token for the telegram bot.
    """
    global remove_words, negative_words
    remove_words = json.loads(open("Data/settings.json").read())["remove_words"]
    negative_words = json.loads(open("Data/settings.json").read())["negative_words"]

    # get the telegram bot toekn
    token = json.loads(open("Data/bottoken.json").read())["token"]
    return token

# MODULE GET TEXT FROM IMAGE


def show_img(title, img):
    """"Shows an image (Usefull for debugging)."""
    cv2.imshow(title, img)
    cv2.waitKey(2500)

    cv2.destroyAllWindows()


def get_question(path):
    """Reading the question and guessing the line number."""
    image = cv2.imread(path)
    height, width = image.shape[:2]

    # The problem of this huge portion of code is that the question hasn't always the same lenght
    # Let's get the starting pixel coordiantes (top left of cropped top)
    start_row, start_col = int(height * 24 / 100), int(0)
    # Let's get the ending pixel coordinates (bottom right of cropped top)
    end_row, end_col = int(height * 43 / 100), int(width)

    cropped_img = image[start_row:end_row, start_col:end_col]
    # show_img("question", cropped_img)
    cv2.imwrite("Screens/question.png", cropped_img)

    question = apply_pytesseract("Screens/question.png")
    question = question.splitlines()
    linenumber = len(question)
    print("lines in the question: " + str(linenumber))

    # returning the question without \n
    return " ".join(question), linenumber


def get_option(path, lineno, index):
    """" Crops the image to get the interesting portion (that one with an option).

    The image cutting depends on the line number (lineno) of the question.
    This function just works for one option (depending on the index parameter).
    It will be called in parallel to process all the other options."""
    # this values derives from empirical tries
    # they refer to the end position of the question that depends on the lineno
    # for istance if the question has 2 lines, the options will start at crop_cropconfig[2-1]
    crop_config = [41 / 100, 45 / 100, 46 / 100]
    end_q = crop_config[lineno - 1] + (index - 1)*11/100

    image = cv2.imread(path)
    height, width = image.shape[:2]

    start_row, start_col = int(height * end_q), int(0)
    # they height of an option box is 11/100 of the entire image height (more or less).
    end_row, end_col = int(height * (end_q + 11 / 100)), int(width)

    cropped_img = image[start_row:end_row, start_col:end_col]
    # show_img("option" + index, cropped_img)
    imgpath = "Screens/answer" + str(index) + ".png"
    cv2.imwrite(imgpath, cropped_img)

    return imgpath


# # GETTING THE QUESTION AND THE ASWERS
# # Let's get the starting pixel coordiantes (top left of cropped top)
# start_row, start_col = int(height * 27/100), int(0)
# # Let's get the ending pixel coordinates (bottom right of cropped top)
# end_row, end_col = int(height * 79/100), int(width)
# cropped_img = image[start_row:end_row, start_col:end_col]
# cv2.imwrite("Screens/cropped.png", cropped_img)


def apply_pytesseract(input_image):
    """Convert the image to black and white and apply pytesseract to get the text"""

    # load the image
    image = cv2.imread(input_image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((1, 1), np.uint8)
    gray = cv2.dilate(gray, kernel, iterations=1)
    gray = cv2.erode(gray, kernel, iterations=1)

    gray_thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray_blur = cv2.medianBlur(gray, 3)

    # store grayscale image as a temp file to apply OCR
    filename = "Screens/{}blur.png".format(os.getpid())
    cv2.imwrite(filename, gray_blur)

    # load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)

    if not text:
        filename = "Screens/{}thresh.png".format(os.getpid())
        cv2.imwrite(filename, gray_thresh)

        # load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file
        text = pytesseract.image_to_string(Image.open(filename))
        os.remove(filename)

    return text


def get_and_search_option(i, screenpath, question, lineno, negative_question, return_dict):
    """Taking the screenshot and the parsed question this function read one option and search it.

     This function will be called in parallel so that the option detection and the searching is faster."""
    optionpath = get_option(screenpath, lineno, i)
    option = apply_pytesseract(optionpath)

    google_wiki(question, option, negative_question, return_dict)

# MODULE SEARCH


class ParsedQuestion:
    """Holding some elements extracted from the question"""
    def __init__(self, originalq, proper_nouns, simplyfiedq):
        self.original = originalq
        self.proper_nouns = proper_nouns
        self.simplyfied = simplyfiedq


def simplify_ques(question):
    """Simplify question and remove the words in the setting.json"""
    question = question.strip('?')
    splitted_question = question.split()
    # this line should remove the first words like 'Quale' 'Chi' 'In'
    splitted_question = splitted_question[1:] if splitted_question[0].lower() in remove_words else splitted_question

    # proper noun is a list with elements like "Marco Rossi" or "Title of a Song" or "GPRS"
    # this line catches element between quotes
    proper_nouns = re.findall('"([^"]*)"', " ".join(splitted_question))
    for i, _ in enumerate(splitted_question):
        # check for acronyms "NBA"
        if splitted_question[i].isupper():
            proper_nouns.append(splitted_question[i])
            continue
        # if two subsequent words has the first letter uppercased they probably refers to a proper nuon
        try:
            if splitted_question[i][0].isupper() and splitted_question[i + 1][0].isupper():
                proper_nouns.append(splitted_question[i] + " " + splitted_question[i + 1])
        except IndexError:
            pass

    qwords = question.lower().split()
    # check if the question is a negative one
    neg = True if [i for w in qwords if w in negative_words] else False

    cleanwords = [word for word in qwords if word not in remove_words]

    return ParsedQuestion(question, proper_nouns, " ".join(cleanwords)), neg


# get web page
def get_page(link):
    try:
        if link.find('mailto') != -1:
            return ''
        req = urllib2.Request(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
        html = urllib2.urlopen(req).read()
        return html
    except (urllib2.URLError, urllib2.HTTPError, ValueError):
        return ''


# use google to get wiki page
# @handle_exceptions
def google_wiki(sim_ques, option, neg, return_dict):
    """Searches the question and the single option on google and wikipedia.

    sim_ques must be a ParsedQuestion object.
    """
    print("Searching ..." + sim_ques.original + "?  " + option)
    points = 0
    option = option[1:] if option[0].lower() in remove_words else option

    words = sim_ques.simplyfied.split()
    # force google to search for the exact match
    searched_option = '\"' + option.lower() + '\"'

    searched_option += ' wiki'

    # get google search results for option + 'wiki'
    search_wiki = google.search(searched_option, pages=1, lang="it")

    if not search_wiki:
        return_dict[option] = points
        return

    link = search_wiki[0].link
    content = get_page(link)
    soup = BeautifulSoup(content, "lxml")
    page = soup.get_text().lower()

    temp = 0
    for word in words:
        temp = temp + page.count(word)
    for pn in sim_ques.proper_nouns:
        temp = temp + page.count(pn.lower()) * 10

    points = temp

    return_dict[option] = points if not neg else -points
    return


# MODULE MAIN

# @handle_exceptions
def solve_quiz(screenpath):
    """Given a path to a valid screenshot it tries to solve the quiz in parallel."""
    question, lineno = get_question(screenpath)
    simpler_question, negative_question = simplify_ques(question)

    # if the answer is negative the results are resversed we check for that one with less matches
    points_coeff = 1
    if negative_question:
        points_coeff = -1

    manager = Manager()
    return_dict = manager.dict()

    tasks = []
    for i in [1, 2, 3]:
        # searching in parallel
        proc = Process(target=get_and_search_option, args=(i, screenpath, simpler_question, lineno,
                                                           negative_question, return_dict))
        proc.start()
        tasks.append(proc)

    for t in tasks:
        t.join()

    points = return_dict.values()
    # taking the max match value
    max_point = max(points)
    print("\n" + bcolors.UNDERLINE + question + bcolors.ENDC + "\n")
    return_option = ""
    for point, option in zip(points, return_dict.keys()):
        if max_point == point:
            return_option = option
            # if this is the "correct" answer it will appear green
            option = bcolors.OKGREEN+option+bcolors.ENDC

        print(option + " { points: " + bcolors.BOLD + str(point*points_coeff) + bcolors.ENDC + " }\n")

    return return_option


def hello(bot, update):
    """Called when the users sends /hello, just to see if the bot is alive."""
    chat_id = update.message.chat_id
    bot.send_message(chat_id, text="hi!")


def screen(bot, update):
    """Takes the screenshot from the telegram bot chat, saves it and calls the solve function."""
    chat_id = update.message.chat_id
    file_id = update.message.photo[-1].file_id
    newFile = bot.getFile(file_id)
    imgpath = "Screens/screenshot.png"
    newFile.download(imgpath)

    bot.send_message(chat_id, text="Screenshot received")

    answer = solve_quiz(imgpath)
    # returning the possible answer
    bot.send_message(chat_id, text=answer)


def main(ttoken):
    """Starts the telegram bot registering the callback functions."""
    updater = Updater(ttoken)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('hello', hello))
    dp.add_handler(MessageHandler(Filters.photo, screen))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    ttoken = load_settings()
    solve_quiz("Screens/livequiz1.jpg")
    exit(0)

    print(bcolors.WARNING + "\nThe script/bot is running | Ctrl-C to stop \n" + bcolors.ENDC)

    main(ttoken)
