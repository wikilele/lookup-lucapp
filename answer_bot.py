

# TODO:
# * Implement normalize func
# * Attempt to google wiki \"...\" part of question
# * Rid of common appearances in 3 options
# * Automate screenshot process
# //Script is in working condition at all times
# //TODO is for improving accuracy


# answering bot for Live Quiz
from multiprocessing import Process, Manager
from telegram.ext import *
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


def load_settings():
    """ Loads all the configuration of the application.

    It gets and returns the token for the telegram bot.
    """
    # get the telegram bot token
    token = json.loads(open("Data/bottoken.json").read())["token"]
    return token


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
    newfile = bot.getFile(file_id)
    imgpath = "Screens/screenshot.png"
    newfile.download(imgpath)

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
    solve_quiz("Screens/livequiz0.jpg")
    exit(0)

    print(bcolors.WARNING + "\nThe script/bot is running | Ctrl-C to stop \n" + bcolors.ENDC)

    main(ttoken)
