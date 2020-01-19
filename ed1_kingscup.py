from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, ConversationHandler
from telegram import ChatAction, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from datetime import datetime
import json
import os
import requests
import logging
import random



# Initialise logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Load bot token
with open('token.ini', 'r') as file:
    BOT_TOKEN = file.read()

# Create the bot
updater = Updater(token=BOT_TOKEN, use_context=True)

# Load persistent state
if os.path.isfile('data.txt'):
    with open('data.txt', 'r') as file:
        counter_dict = json.load(file)
else:
    counter_dict = {}

#Deck
pokerDeck = ['2 ♦️',
        '3 ♦️',
        '4 ♦️',
        '5 ♦️',
        '6 ♦️',
        '7 ♦️',
        '8 ♦️',
        '9 ♦️',
        '10 ♦️',
        'J ♦️',
        'Q ♦️',
        'K ♦️',
        'A ♦️',
        '2 ♣️',
        '3 ♣️',
        '4 ♣️',
        '5 ♣️',
        '6 ♣️',
        '7 ♣️',
        '8 ♣️',
        '9 ♣️',
        '10 ♣️',
        'J ♣️',
        'Q ♣️',
        'K ♣️',
        'A ♣️',
        '2 ♥️',
        '3 ♥️',
        '4 ♥️',
        '5 ♥️',
        '6 ♥️',
        '7 ♥️',
        '8 ♥️',
        '9 ♥️',
        '10 ♥️',
        'J ♥️',
        'Q ♥️',
        'K ♥️',
        'A ♥️',
        '2 ♠️',
        '3 ♠️',
        '4 ♠️',
        '5 ♠️',
        '6 ♠️',
        '7 ♠️',
        '8 ♠️',
        '9 ♠️',
        '10 ♠️',
        'J ♠️',
        'Q ♠️',
        'K ♠️',
        'A ♠️']

#Rules
rule = {'A':"CHEERS — Everyone drinks!",
        '2':"YOU — Point at that unlucky fella who has to take a sip",
        '3':"ME — The person who drew this card drinks",
        '4':"THUMB MASTER — Last person to put their thumb on the table drinks!",
        '5':"DICKS — All guys drink",
        '6':"CHICKS — All girls drink",
        '7':"HANDS UP — Raise up your hand! The last person to do so must drink.",
        '8':"BUDDY — Choose a buddy, whenever you drink, your buddy drinks too!",
        '9':"RHYME TIME — Go around the circle rhyming one word. The person who fail to rhyme drinks!",
        '10':"R-O-C-K ROCK — The person who drew chooses a category, and then everyone must name something in it.",
        'J':"RULE MASTER — Whoever picks Jack gets to come up with a rule that everybody has to follow.",
        'K': "ALL HAIL THE KING — Add whatever you want into the King’s Cup.",
        'Q':"QUESTIONS — Ask questions, whoever that answers you drinks!"
        }

counter = 0 
# make new deck
Deck = []
def newDeck():
    global Deck
    Deck = pokerDeck.copy()

# Add /start handler
def start(update, context):
    global counter
    newDeck()
    counter = 0
    reply_keyboard = [['/draw']]

    update.message.reply_text(
        f'Hi {update.effective_message.chat.first_name}! Click /draw to start the game and receive a card.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False))


    #context.bot.send_message(
    #    chat_id=update.effective_chat.id,
    #    text=f'Hello {update.effective_message.chat.first_name}! Type /draw to receive a card.'
    #)
    random.shuffle(Deck)

# Add /draw handler
def draw(update, context):
    global counter
    # Send drawing message
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Hmm... Picking your lucky card...'
    )

    # Send typing status
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    #Drawing random card
    thisCard = Deck[0]

    if thisCard[0] == 'K':
        global rule
        counter += 1
        if counter >= 4:
            reply_keyboard = [['/start']]

            update.message.reply_text(
                f"Wah really lucky card.. {thisCard}, no more K's left..\n\nShag Bro... Bopez ah, TAH THE CUP!\n\n" +
                "Click /start to play another round! No drunk no go home!",
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False))
            #context.bot.send_message(
            #chat_id = update.effective_chat.id,
            #text=f"Wah really lucky card.. {thisCard}, no more K's left..\n\nShag Bro... Bopez ah, TAH THE CUP!"
            #)
        else:
            context.bot.send_message(
            chat_id = update.effective_chat.id,
            text=f"Your lucky card is {thisCard}! {4 - counter} K's left\n" + rule[thisCard[0]]
            )

    else:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text=f"Your lucky card is {thisCard}!\n" + rule[thisCard[0]]
        )



    del Deck[0]
    
updater.dispatcher.add_handler(
    CommandHandler('start', start)
)

updater.dispatcher.add_handler(
    CommandHandler('draw', draw)
)

# Start the bot
updater.start_polling()
print('Bot started!')

# Wait for the bot to stop
updater.idle()

# Dump persistent state
with open('data.txt', 'w') as file:
    json.dump(counter_dict, file)

print('Bot stopped!')