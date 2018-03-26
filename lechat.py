"""Provide chatting capabilities for a Le bot."""

from collections import defaultdict as _defaultdict
from difflib import get_close_matches as _get_close_matches

from random import (
    choice as _choice,
    random as _random,
)

from telegram.ext import (
    Filters as _Filters,
    MessageHandler as _MessageHandler,
)


_talkativeness = 0.5

_rooms = _defaultdict(
    lambda: {'dict': {}, 'last_message': '', 'last_user': None})


def _update_last_message(room, message, user):
    """Update the last message in the room."""
    room['last_message'] = message
    room['last_user'] = user


def _try_to_say_something(bot, message):
    """Find a response and maybe say something."""
    try:
        room = _rooms[message.chat_id]

        previous_messages = room['dict'].keys()
        similar_messages = _get_close_matches(message.text, previous_messages)

        if len(similar_messages) > 0 and _random() < _talkativeness:
            choosen_message = _choice(similar_messages)
            response = room['dict'][choosen_message]
            bot.send_message(message.chat_id, response)
            _update_last_message(room, response, 'bot')

    except TypeError as te:
        if "'NoneType' object is not iterable" in str(te):
            # this happens when message.text==None
            return

        else:
            raise


def _parse_message(bot, update):
    """Parse a message and maybe respond to it."""
    room = _rooms[update.message.chat_id]

    record_response = (
        room['last_message']
        and update.message.text     # current message
        and room['last_user'] != update.message.from_user.id
    )

    if record_response:
        last_message = room['last_message']
        room['dict'][last_message] = update.message.text

    _update_last_message(
        room, update.message.text, update.message.from_user.id)

    _try_to_say_something(bot, update.message)


_handler = _MessageHandler(_Filters.all, _parse_message)
