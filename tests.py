"""Tests for lechat."""

from unittest import (
    main,
    TestCase,
)

from unittest.mock import (
    MagicMock,
    patch,
)

import lechat

from lechat import (
    _parse_message,
    _update_last_message,
)


def is_private(string):
    """Return ``True`` if string is a private attribute name."""
    return string.startswith('_')


def is_public(string):
    """Return ``True`` if string is a public attribute name."""
    return not is_private(string)


class TestParseMessage(TestCase):
    """Test the ``_parse_message`` function."""

    def setUp(self):
        """Call ``_parse_message`` with ``update.message.text=None``."""
        self.bot = MagicMock()

    def test_parse_message_handles_empty_message(self):
        """Thest that ``_parse_message`` can handle an empty message.

        ``update.message.text`` is ``None`` when a user sends a message
        with other types of condent, but without writing text. i.e.
        Photos or stickers.

        When ``None`` is passed as the first argument to
        ``difflib.get_close_matches``, that function throws an error.
        ``update.message.text`` should avoid passing ``None`` or handle
        the exception.
        """
        update = MagicMock()
        update.message.text = None

        try:
            _parse_message(self.bot, update)

        except TypeError as te:
            if "'NoneType' object is not iterable" in str(te):
                self.fail(
                    '_parse_message seems not to be handling empty messages.')

            else:
                raise

    @patch('lechat._talkativeness', 1)
    def test__parse_message_simple_response(self):
        """Test that ``_parse_message`` can send a simple response."""
        update1 = MagicMock(
            **{'message.text': '8746128376', 'message.chat_id': '1'})

        update2 = MagicMock(
            **{'message.text': 'dhfgsdhfgsd', 'message.chat_id': '1'})

        _parse_message(self.bot, update1)
        _parse_message(self.bot, update2)
        _parse_message(self.bot, update1)

        self.bot.send_message.assert_called_with('1', 'dhfgsdhfgsd')


class TestLeChatModule(TestCase):
    """Test lechat module contents."""

    def test_lechat_has_no_public_attributes(self):
        """Test that lechat has no public attributes."""
        self.assertEqual([], [a for a in dir(lechat) if is_public(a)])


class TestUpdateLastMessage(TestCase):
    """Test the ``lechat._update_last_message`` function."""

    def test_simple_call_to_update_last_message(self):
        """Test a simple call to ``_update_last_message``."""
        room = {'last_message': 'Hi!', 'last_user': 'Alice'}
        _update_last_message(room, 'Hi Alice!', 'Bob')

        self.assertEqual(
            room, {'last_message': 'Hi Alice!', 'last_user': 'Bob'})


if __name__ == '__main__':
    main()
