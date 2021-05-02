"""
ezWhisperBot, Telegram Bot for sending whisper messages
Copyright (C) 2021  Dash Eclipse

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from pyrogram import Client, filters
from pyrogram.types import (Message,
                            InlineKeyboardMarkup, InlineKeyboardButton,
                            CallbackQuery)

DEFAULT_TEXT = (
    "This bot allows you to send whisper messages, "
    "works only in inline mode\n\n"
    "[Source Code](https://github.com/dashezup/ezWhisperBot)"
    " | [Developer](https://t.me/dashezup)"
    " | [Support Chat](https://t.me/ezupdev)"
)
DEFAULT_REPLY_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "Select a Chat to Try",
                switch_inline_query=""
            ),
            InlineKeyboardButton(
                "Try in This Chat",
                switch_inline_query_current_chat=""
            )
        ]
    ]
)


@Client.on_message(filters.text
                   & filters.incoming
                   & ~filters.edited
                   & filters.command("start"))
async def command_start(_, m: Message):
    if len(m.command) == 2 and m.command[1] == "learn":
        text_start = (
            "This bot works only in inline mode, a example use would be like "
            "this:\n\n"
            "- Write a whisper to @username\n"
            "`@ezWhisperBot @username some text here`\n\n"
            "- Whisper to the first one who open it (can also be used in PM)\n"
            "`@ezWhisperBot some text here`"
        )
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Next",
                        callback_data="learn_next"
                    )
                ]
            ]
        )
    else:
        text_start = DEFAULT_TEXT
        reply_markup = DEFAULT_REPLY_MARKUP
    await m.reply_text(
        text_start,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex("^learn_next$"))
async def back_to_inline(_, cq: CallbackQuery):
    await cq.edit_message_text(
        text=DEFAULT_TEXT,
        disable_web_page_preview=True,
        reply_markup=DEFAULT_REPLY_MARKUP
    )
    await cq.answer("Now you can back to inline mode")
