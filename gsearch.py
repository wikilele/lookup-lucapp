"""Search the question and one given option.

The module searches the question and one option; it then tries to count the number of matches.

TODO improve the accuracy of the seach
"""


import json
import urllib.request as urllib2
from bs4 import BeautifulSoup
from google import google
import re
import functools
import sys

# list of words to clean from the question during google search
remove_words = json.loads(open("Data/settings.json").read())["remove_words"]

# negative words
negative_words = json.loads(open("Data/settings.json").read())["negative_words"]


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
    # TODO have a better exception handing here
    except (urllib2.URLError, urllib2.HTTPError, ValueError) or Exception:
        return ''


@handle_exceptions
def google_wiki(sim_ques, option, neg, return_dict):
    """Searches the question and the single option on google and wikipedia.

    sim_ques must be a ParsedQuestion object.
    """
    print("Searching ..." + sim_ques.original + "?  " + option)
    points = 0
    option = option[1:] if option[0].lower() in remove_words else option

    words = sim_ques.simplyfied.split()
    # TODO force google to search for the exact match ??? using quotes
    searched_option = option.lower()

    # searched_option += ' wiki'

    # get google search results for option + 'wiki'
    search_wiki = google.search(searched_option, pages=1, lang="it")

    if not search_wiki or not search_wiki[0].link:
        # maxint was removed
        # not so clear
        return_dict[option] = -sys.maxsize if neg else sys.maxsize
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

