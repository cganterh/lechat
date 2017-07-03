"""Provide chatting capabilities for a Le bot."""

from difflib import get_close_matches
from logging import getLogger
from random import choice, random

from telegram.ext import Filters, MessageHandler


rooms = {}


def parse_message(bot, update):
    """Parse a message and maybe respond to it."""
    cur_message = update.message.text
    chat_id = update.message.chat_id
    user = update.message.from_user.id

    if chat_id not in rooms:
        rooms[chat_id] = {
            'dict': {},
            'last_message': '',
            'last_user': None,
        }

    d = rooms[chat_id]['dict']
    last_message = rooms[chat_id]['last_message']
    last_user = rooms[chat_id]['last_user']

    if cur_message and last_message and last_user != user:
        d[last_message] = cur_message

    rooms[chat_id]['last_message'] = cur_message if cur_message else ''
    rooms[chat_id]['last_user'] = user

    previous_messages = d.keys()
    try:
        similar_messages = get_close_matches(cur_message, previous_messages)

    except:
        getLogger().exception(
            'This is the error we want to debug.\n\n'
            'cur_message = {}\n\n'
            'previous_messages={}'.format(cur_message, previous_messages)
        )

    if len(similar_messages) > 0 and random() > 0.5:
        choosen_message = choice(similar_messages)
        response = d[choosen_message]
        bot.sendMessage(chat_id=update.message.chat_id, text=response)
        rooms[chat_id]['last_message'] = response


handler = MessageHandler(Filters.all, parse_message)
