#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Simple Bot to send timed Telegram messages.
# This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler
import logging
from telegram.ext.filters import Filters, BaseFilter
# import cv2
# import urllib
# import urllib.request
import numpy as np

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi! Use /set <seconds> to set a timer')


def alarm(bot, job):
    """Send the alarm message."""
    bot.send_message(job.context, text='Beep!')


def set_timer(bot, update, args, job_queue, chat_data):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        # Add job to queue
        job = job_queue.run_once(alarm, due, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Timer successfully set!')
        print('Timer set by ' + str(args[0]))

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def unset(bot, update, chat_data):
    """Remove the job if the user changed their mind."""
    if 'job' not in chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('Timer successfully unset!')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def getImage(bot, update, user_data, chat_data):
	updates = update
	print('\n\n\n\n')
	print(update.message.photo[0].file_id)
	bot.send_message(chat_id=update.message.chat_id, text=str(update.message.photo))
    
	for obj in update.message.photo:
		bot.send_photo(chat_id=update.message.chat_id, photo=obj.file_id)
		break

	# 'https://telegram.org/img/t_logo.png'
	# print('\n\n\n suret \n')
	# imgPath = update.message.photo[0].get_file().file_path
	# req = urllib.request.urlopen(str(imgPath))
	# arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
	# img = cv2.imdecode(arr, -1) # 'Load it as it is'

	
	# bot.send_photo(chat_id=297542068, photo=update.message.photo[0].file_id)
	# print('\n', update.message.chat_id)
	

	# print([u.message.photo for u in updates if u.message.photo])
	# print(updates[0].message)
	# print('Kazakh\n\n\n\n')
	# print(updates)
	# print('\n\n\n\n')
	# print(user_data)
	# print(chat_data)

def main():
    """Run bot."""
    updater = Updater("590657376:AAGPekOrdaSNSjJys5ouPEopUsSKaChYKBw")


    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))
    dp.add_handler((CommandHandler("img", getImage)))

    mh = MessageHandler(
    	filters=Filters.photo, 
    	callback=getImage, 
    	pass_update_queue=False, 
    	pass_job_queue=False, 
    	pass_user_data=True, 
    	pass_chat_data=True, 
    	message_updates=True, 
    	channel_post_updates=True, 
    	edited_updates=True)
    dp.add_handler(mh)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()



# opencv-python = "*"
# numpy = "*"
# cmake = "*"
# dlib = "*"
# face_recognition = "*"