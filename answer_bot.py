'''

	TODO:
	* Implement normalize func
	* Attempt to google wiki \"...\" part of question
	* Rid of common appearances in 3 options
	* Automate screenshot process
	* Implement Asynchio for concurrency

	//Script is in working condition at all times
	//TODO is for improving accuracy

'''

# answering bot for trivia HQ and Cash Show
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
import sys
import functools
import np
import time, threading
from os import listdir
from os.path import isfile, join
from multiprocessing import Process, Manager
# import wx
from halo import Halo


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

# path where the smartphone is mounted
mypath = "phone/Archivio condiviso interno/DCIM/Screenshots/"
# number of screenshot already in this path
screenno = 0


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


# loads all he settings
def load_settings():
    """ Loads a list of words to be removed and negative words from a json file to a variable.
    It loads also questions from the previous games.
    """
    global remove_words, negative_words, screenno
    remove_words = json.loads(open("Data/settings.json").read())["remove_words"]
    negative_words = json.loads(open("Data/settings.json").read())["negative_words"]

    os.system("jmtpfs phone/")
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    screenno = len(onlyfiles)


def screen_grab():
    """ Takes a screenshot and saves it."""
    # 31,228 485,620 co-ords of screenshot// left side of screen
    # only if the image capture software has hgih quality
    # os.system(" import -window MIMAX2  " + to_save)
    os.system("jmtpfs phone/")
    mypath = "phone/Archivio condiviso interno/DCIM/Screenshots/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    # os.system("sudo umount phone/")
    print(onlyfiles[-1])
    return mypath + onlyfiles[-1] # -3,-8,-1


def crop_image(path):
    """Cropping the image to remove undesired stuff"""
    crop_config = [41/ 100, 45 / 100, 46/ 100]
    storepath = ["Screens/question.png", "Screens/answer1.png", "Screens/answer2.png", "Screens/answer3.png"]

    image = cv2.imread(path)
    height, width = image.shape[:2]

    # The problem of this huge portion of code is that the question hasn't always the same lenght
    # GETTING THE QUESTION
    # Let's get the starting pixel coordiantes (top left of cropped top)
    start_row, start_col = int(height * 24/100), int(0)
    # Let's get the ending pixel coordinates (bottom right of cropped top)
    end_row, end_col = int(height * 43/100), int(width)

    cropped_img = image[start_row:end_row, start_col:end_col]
    # cv2.imshow("question", cropped_img)
    # cv2.waitKey(2000)
    cv2.imwrite("Screens/question.png", cropped_img)

    question = apply_pytesseract("Screens/question.png")
    linenumber = len(question.splitlines())
    print(linenumber)
    end_q = crop_config[linenumber - 1]

    for img in storepath[1:]:
        # GETTING ANSWERS
        start_row, start_col = int(height * end_q), int(0)
        end_row, end_col = int(height * (end_q + 11 / 100)), int(width)

        cropped_img = image[start_row:end_row, start_col:end_col]
        # cv2.imshow(img, cropped_img)
        # cv2.waitKey(2000)
        cv2.imwrite(img, cropped_img)

        end_q = end_q + 11/100

    cv2.destroyAllWindows()

    # # GETTING THE QUESTION AND THE ASWERS
    # # Let's get the starting pixel coordiantes (top left of cropped top)
    # start_row, start_col = int(height * 27/100), int(0)
    # # Let's get the ending pixel coordinates (bottom right of cropped top)
    # end_row, end_col = int(height * 79/100), int(width)
    # cropped_img = image[start_row:end_row, start_col:end_col]
    # cv2.imwrite("Screens/cropped.png", cropped_img)

    return storepath


def apply_pytesseract(input_image):
    """Convert the image to black and white and apply pytesseract to get the text"""
    # prepare argparse
    ap = argparse.ArgumentParser(description='HQ_Bot')
    ap.add_argument("-i", "--image", required=False, default=input_image, help="path to input image to be OCR'd")
    ap.add_argument("-p", "--preprocess", type=str, default="blur", help="type of preprocessing to be done")
    args = vars(ap.parse_args())

    # load the image
    image = cv2.imread(args["image"])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((1, 1), np.uint8)
    gray = cv2.dilate(gray, kernel, iterations=1)
    gray = cv2.erode(gray, kernel, iterations=1)

    gray_thresh = cv2.threshold(gray, 0, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
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


def read_screen(screenshot_file):
    """ Get OCR text //questions and options"""
    # print("Taking the screen shot....")
    # screenshot_file = screen_grab()

    # temporary file used for testing
    # screenshot_file = "Screens/livequiz4.jpg"

    question_and_answers = crop_image(screenshot_file)

    question = apply_pytesseract(question_and_answers[0])
    answers = []
    for qa in question_and_answers[1:]:
        answerx = apply_pytesseract(qa)
        answers.append(answerx)

    print(question)
    print(answers)

    return question, answers


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
def google_wiki(sim_ques, options, neg, return_dict):
    print("Searching ..." + options)
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

    return_dict[options[0]] = points
    return
    # return points, maxo


def get_points_live(screenpath):
    """Main  control flow"""
    neg= False
    question, options = read_screen(screenpath)
    simq = ""
    points = []
    simq, neg = simplify_ques(question)
    maxo=""
    m=1
    if neg:
        m=-1
    #points, maxo = google_wiki(simq, options, neg)

    manager = Manager()
    return_dict = manager.dict()

    option1 = Process(target=google_wiki, args=(simq, options[0], neg, return_dict))
    option2 = Process(target=google_wiki, args=(simq, options[1], neg, return_dict))
    option3 = Process(target=google_wiki, args=(simq, options[2], neg, return_dict))

    option1.start()
    option2.start()
    option3.start()

    option1.join()
    option2.join()
    option3.join()

    print("\n" + bcolors.UNDERLINE + question + bcolors.ENDC + "\n")
    for point, option in zip(return_dict.values(), options):
        #if maxo == option.lower():
         #   option=bcolors.OKGREEN+option+bcolors.ENDC
        print(option + " { points: " + bcolors.BOLD + str(point*m) + bcolors.ENDC + " }\n")


def polling_dir():
    """Polling the directory every tot seconds to check if a new screenshot has been added"""
    global screenno
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    print("Polling the directory...")
    if len(onlyfiles) > screenno:
        screenno = screenno + 1  # necessary if not deleting the file
        get_points_live(mypath + onlyfiles[-1])


    threading.Timer(1, polling_dir).start()


# menu// main func
if __name__ == "__main__":
    load_settings()
    print(bcolors.WARNING + "\nThe script is running, Ctrl-C to stop, don't forget to umount phone/\n" + bcolors.ENDC)

    polling_dir()

