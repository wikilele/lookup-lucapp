""" Takes the screenshot and tries to guess the answer.

Each option is red and searched in parallel.
"""

from multiprocessing import Process, Manager
from imgtotext import *
from gsearch import *


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


def get_and_search_option(i, screenpath, question, lineno, negative_question, return_dict):
    """Taking the screenshot and the parsed question this function read one option and search it.

     This function will be called in parallel so that the option detection and the searching is faster."""
    optionpath = get_option(screenpath, lineno, i)
    option = apply_pytesseract(optionpath)

    google_wiki(question, option, negative_question, return_dict)


@handle_exceptions
def solve_quiz(screenpath):
    """Given a path to a valid screenshot it tries to solve the quiz in parallel."""
    question, lineno = get_question(screenpath)
    # simpler_question is an object of type ParsedQuestion
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
