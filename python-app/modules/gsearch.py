
"""Search the question and one given option.

The module searches the question and one option; it then tries to count the number of matches.

TODO improve the accuracy of the seach
"""


import json
import urllib.request as urllib2
from bs4 import BeautifulSoup
from google import google
import re
import modules.mydecorators as mydecorators
import sys

# list of words to clean from the question during google search
remove_words = json.loads(open("data/settings.json").read())["remove_words"]

# negative words
negative_words = json.loads(open("data/settings.json").read())["negative_words"]


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
        # if two subsequent words has the first letter uppercased they probably refers to a proper noun
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


@mydecorators.timeit("actualsearch")
def search(searched_option):
    # searched_option += ' wiki'
    # get google search results for option + 'wiki'
    return google.search(searched_option, pages=1, lang="it")


def get_score(link, words, sim_ques):
    points = 0
    content = get_page(link)
    soup = BeautifulSoup(content, "lxml")
    page = soup.get_text().lower()

    for word in words:
        points = points + page.count(word)
    for pn in sim_ques.proper_nouns:
        points = points + page.count(pn.lower()) * 10

    return points


@mydecorators.handle_exceptions
@mydecorators.timeit("googlesearch")
def google_wiki(sim_ques, option, neg):
    """Searches the question and the single option on google and wikipedia.

    sim_ques must be a ParsedQuestion object.
    """
    print("Searching ..." + sim_ques.original + "?  " + option)

    # removing the first word like 'Il' 'Una'
    option = option.split()
    option = option[1:] if option[0].lower() in remove_words else option
    option = " ".join(option)

    words = sim_ques.simplyfied.split()
    # TODO force google to search for the exact match ??? using quotes
    searched_option = option.lower()

    search_wiki = search(searched_option)

    if not search_wiki or not search_wiki[0].link:
        # maxint was removed
        # not so clear
        return -sys.maxsize if neg else sys.maxsize

    points = get_score(search_wiki[0].link, words, sim_ques)

    return points if not neg else -points


