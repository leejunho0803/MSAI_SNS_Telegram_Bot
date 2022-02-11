# Step1. Import Libraries

# Web Crawling Package
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Telegram Package
import telegram
import telepot
import random
import threading
import sched
from datetime import datetime
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,CallbackContext, MessageHandler, Filters

# A package for periodically running a program
from apscheduler.schedulers.blocking import BlockingScheduler




# Step 2. Call the telegram bot

# Store the token at parameter
bot_token = '5280020077:AAHMEKP5xUuijZu_9Z2KseqyWEWww5SmB7A'

# Bot function
bot = telepot.Bot(bot_token)

# Bot chat information & message update
updates = bot.getUpdates()

# chat_id
chat_id = bot.getUpdates()[-1]['message']['chat']['id']
name_last = bot.getUpdates()[-1]['message']['chat']['last_name']
name_first = bot.getUpdates()[-1]['message']['chat']['first_name']

# Sending the message to aquired chat_id
bot.sendMessage(chat_id = chat_id or '1781255293', text = "Elon Musk's Twitter real-time notification has begun.\
    If you enter the '/start', you can find out more information\
    And if you enter the '/task', you can check various functions by pressing the button.")



'''
Start function
'''
#step1.Updater, Dispatcher
updater = Updater(token = bot_token, use_context=True)
dispatcher = updater.dispatcher

#step2./start 
def start(update, context):
    text = 'Hello {}, This bot was created to notify Elon Musk\'s Twitter in real time. The tweet will be updated every 60 seconds and if there are no new tweets, it will send a message that there are no tweets.'.format(name_first)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

#step3. CommandHandler
start_handler = CommandHandler('start', start)

#step4.Add Handler to Dispatcher
dispatcher.add_handler(start_handler)

#step5.Updater monitoring(polling)
updater.start_polling()




'''
Button
'''

def cmd_task_buttons(update, context):
    task_buttons = [
        [
            InlineKeyboardButton("Your name", callback_data = 1), InlineKeyboardButton("Whose Tweeter?", callback_data = 2)
        ],
        [
            InlineKeyboardButton("Quit", callback_data = 9)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(task_buttons)
    context.bot.send_message(
        chat_id = update.message.chat_id,
        text = 'Please Select the task.',
        reply_markup = reply_markup
        )

def cb_button(update, context):
    query = update.callback_query
    data = query.data

    context.bot.send_chat_action(
        chat_id = update.effective_user.id,
        action = ChatAction.TYPING
    )

    if data == "9":
        context.bot.edit_message_text(
            text = f"The task has ended.",
            chat_id = query.message.chat_id,
            message_id = query.message.message_id
        )
    elif data == "1":
        context.bot.edit_message_text(
            text = f"{name_last} {name_first}",
            chat_id = query.message.chat_id,
            message_id = query.message.message_id
        )
    elif data == "2":
        context.bot.edit_message_text(
            text = "Elon Musk",
            chat_id = query.message.chat_id,
            message_id = query.message.message_id
        )


def add_handler(cmd, func):
    updater.dispatcher.add_handler(CommandHandler(cmd, func))

def callback_handler(func):
    updater.dispatcher.add_handler(CallbackQueryHandler(func))

add_handler("task", cmd_task_buttons)
callback_handler(cb_button)
updater.start_polling




# Step 3. Create a scheduler to run commands periodically
sched = BlockingScheduler()



# Step 4. Create a list to store previously sent messages
old_contents = []



# Step 5. Create a function to crawl Twitter messages (parameter is a list of previously collected messages)
def get_content(old_contents = []):

    #Access Elon Musk's Twitter with Chromedriver
    url = 'https://twitter.com/elonmusk'
    driver = webdriver.Chrome('C:\chromedriver\chromedriver.exe')
    driver.get(url)
    time.sleep(3)

    contents = []

    for i in range(10):
        try:
            twitter = driver.find_element_by_xpath(f'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/section/div/div/div[{i}]/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div/span')
            contents.append(twitter.text)
        
        except:
            pass

    time.sleep(3)

    new_contents = []

    for content in contents:
        if content not in old_contents:
            new_contents.append(content)
    
    return new_contents




# Step 6. Telegram Message Sending Function
def send_contents():
    global old_contents
    new_contents = get_content(old_contents)
    
    if new_contents:
        for content in new_contents:
            bot.sendMessage(chat_id=chat_id, text=" **** Elon's Tweet **** " + "\n" + content)
    else:
        pass
        bot.sendMessage(chat_id=chat_id, text=' ****There are no new tweets. **** ')

    old_contents += new_contents.copy()
    # old_contents = list(set(old_contents))




# Step 7. Initial startup, scheduler setup and operation
send_contents()
sched.add_job(send_contents, 'interval', seconds = 60)
sched.start()