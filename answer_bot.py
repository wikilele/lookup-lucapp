

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

    It loads the words to be removed and the negative words from the steeings.json file;
    it also gets and returns the token for the telegram bot.
    """
    global remove_words, negative_words, screenno
    remove_words = json.loads(open("Data/settings.json").read())["remove_words"]
    negative_words = json.loads(open("Data/settings.json").read())["negative_words"]

    token = json.loads(open("Data/bottoken.json").read())["token"]
    return token


def show_img(str, img):
    cv2.imshow(str, img)
    cv2.waitKey(2000)

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
    linenumber = len(question.splitlines())
    print("lines in the question: " + str(linenumber))

    return question, linenumber


def get_option(path, lineno, index):
    crop_config = [41 / 100, 45 / 100, 46 / 100]
    end_q = crop_config[lineno - 1] + (index - 1)*11/100

    image = cv2.imread(path)
    height, width = image.shape[:2]

    start_row, start_col = int(height * end_q), int(0)
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

    # os.remove(screenshot_file)

    return text


def get_and_search_option(i, screenpath, question, lineno, negative_question, return_dict):
    optionpath = get_option(screenpath, lineno, i)
    option = apply_pytesseract(optionpath)

    google_wiki(question, option, negative_question, return_dict)


def simplify_ques(question):
    """Simplify question and remove the words in the setting.json"""
    neg = False
    qwords = question.lower().split()
    # check if the question is a negative one
    if [i for i in qwords if i in negative_words]:
        neg = True
    cleanwords = [word for word in qwords if word.lower() not in remove_words]
    temp = ' '.join(cleanwords)
    clean_question = ""
    #remove ?
    for ch in temp:
        if ch!="?" or ch!="\"" or ch!="\'":
            clean_question=clean_question+ch

    return clean_question.lower(), neg


# get web page
def get_page(link):
    try:
        if link.find('mailto') != -1:
            return ''
        req = urllib2.Request(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
        html = urllib2.urlopen(req).read()
        return html
    except (urllib2.URLError, urllib2.HTTPError, ValueError) as e:
        return ''


# split the string
def split_string(source):
    splitlist = ",!-.;/?@ #"
    output = []
    atsplit = True
    for char in source:
        if char in splitlist:
            atsplit = True
        else:
            if atsplit:
                output.append(char)
                atsplit = False
            else:
                output[-1] = output[-1] + char
    return output


# normalize points // get rid of common appearances // "quote" wiki option + ques
def normalize():
    return None


# take screen shot of screen every 2 seconds and check for question
def check_screen():
    return None


# wait for certain milli seconds 
def wait(msec):
    return None


# answer by combining two words
def smart_answer(content,qwords):
    zipped= zip(qwords,qwords[1:])
    points=0
    for el in zipped :
        if content.count(el[0]+" "+el[1])!=0 :
            points+=1000
    return points


# use google to get wiki page
@handle_exceptions
def google_wiki(sim_ques, options, neg, return_dict):
    print("Searching ..." + sim_ques)
    # spinner = Halo(text='Googling and searching Wikipedia', spinner='dots2')
    # spinner.start()
    num_pages = 1
    points = 0
    content = ""
    maxo=""
    maxp=-sys.maxsize
    words = split_string(sim_ques)
    o = options

    o = o.lower()
    original=o
    o += ' wiki'

    # get google search results for option + 'wiki'
    search_wiki = google.search(o, num_pages)

    if not search_wiki:
        return_dict[options[0]] = points
        return

    link = search_wiki[0].link
    content = get_page(link)
    soup = BeautifulSoup(content,"lxml")
    page = soup.get_text().lower()

    temp=0

    for word in words:
         temp = temp + page.count(word)
    temp+=smart_answer(page, words)
    if neg:
        temp*=-1
    points = temp
    if temp>maxp:
        maxp=temp
        maxo=original

    # spinner.succeed()
    # spinner.stop()

    return_dict[options] = points
    return
    # return points, maxo



@handle_exceptions
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
    chat_id = update.message.chat_id
    bot.send_message(chat_id, text="hi!")


def screen(bot, update):
    chat_id = update.message.chat_id
    file_id = update.message.photo[-1].file_id
    newFile = bot.getFile(file_id)
    imgpath = "Screens/screenshot.png"
    newFile.download(imgpath)

    bot.send_message(chat_id, text="Screenshot received")

    answer = solve_quiz(imgpath)
    bot.send_message(chat_id, text=answer)


def main(ttoken):
    updater = Updater(ttoken)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('hello', hello))
    dp.add_handler(MessageHandler(Filters.photo, screen))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':

    ttoken = load_settings()
    print(bcolors.WARNING + "\nThe script/bot is running | Ctrl-C to stop \n" + bcolors.ENDC)

    main(ttoken)
