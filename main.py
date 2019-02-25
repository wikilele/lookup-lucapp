"""Telegram bot used to get the screenshot from the smartphone and pass it to the solver function.
"""


from telegram.ext import *
from telegram import *
from gsearch import *
from answer_bot import solve_quiz, bcolors


def load_settings():
    """ Loads all the configuration of the application.

    It gets and returns the token for the telegram bot.
    """
    # get the telegram bot token
    token = json.loads(open("Data/bottoken.json").read())["token"]
    return token


def hello(bot, update):
    """Called when the users sends /hello, just to see if the bot is alive."""
    chat_id = update.message.chat_id
    bot.send_message(chat_id, text="hi!")


def get_feedback(bot, update):
    query = update.callback_query
    query.edit_message_text(text="Thanks for the feedback! {}".format(query.data))


def screen(bot, update):
    """Takes the screenshot from the telegram bot chat, saves it and calls the solve function."""
    chat_id = update.message.chat_id
    file_id = update.message.photo[-1].file_id
    newfile = bot.getFile(file_id)
    imgpath = "Screens/screenshot.png"
    newfile.download(imgpath)

    bot.send_message(chat_id, text="screenshot received")

    answer = solve_quiz(imgpath)
    bot.send_message(chat_id, text=answer)

    # returning the possible answer
    # And asking for a feedback (to have correct/totquestion statistic)
    keyboard = [[InlineKeyboardButton("Wrong", callback_data='wrong'),
                 InlineKeyboardButton("Correct", callback_data='correct')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("give us a feedback", reply_markup=reply_markup)


def main(ttoken):
    """Starts the telegram bot registering the callback functions."""
    updater = Updater(ttoken)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('hello', hello))
    dp.add_handler(MessageHandler(Filters.photo, screen))

    dp.add_handler(CallbackQueryHandler(get_feedback))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    ttoken = load_settings()

    if len(sys.argv) > 1 and sys.argv[1] == '-tbot':
        print(bcolors.WARNING + "\nThe script/bot is running | Ctrl-C to stop \n" + bcolors.ENDC)

        main(ttoken)
    else:
        solve_quiz("Screens/livequiz1.jpg")
