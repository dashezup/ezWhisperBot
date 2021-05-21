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
from datetime import datetime

from pyrogram import Client, filters, emoji
from pyrogram.types import (Message,
                            InlineKeyboardMarkup, InlineKeyboardButton,
                            CallbackQuery)

from data import whispers

LEARN_TEXT = (
    "This bot works only in inline mode, a example use would be like "
    "this:\n\n"
    "- Write a whisper to @username\n"
    "`@ezWhisperBot @username some text here`\n\n"
    "- Whisper to the first one who open it (can also be used in PM)\n"
    "`@ezWhisperBot some text here`"
)
LEARN_REPLY_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "Next",
                callback_data="learn_next"
            )
        ]
    ]
)

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
        ],
        [
            InlineKeyboardButton(
                "My Whispers",
                callback_data="list_whispers"
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
        text_start = LEARN_TEXT
        reply_markup = LEARN_REPLY_MARKUP
    else:
        text_start = DEFAULT_TEXT
        reply_markup = DEFAULT_REPLY_MARKUP
    await m.reply_text(
        text_start,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex("^(learn_next|start)$"))
async def show_main_page(_, cq: CallbackQuery):
    await cq.edit_message_text(
        text=DEFAULT_TEXT,
        disable_web_page_preview=True,
        reply_markup=DEFAULT_REPLY_MARKUP
    )
    if cq.data == "learn_next":
        await cq.answer(f"{emoji.ROBOT} Now you may try it in inline mode")


@Client.on_callback_query(filters.regex("^list_whispers$"))
async def list_whispers(_, cq: CallbackQuery):
    user_id = cq.from_user.id
    user_whispers = [
        i for i in whispers.values() if i['sender_uid'] == user_id
    ]
    if len(user_whispers) == 0:
        text = "You don't have any whispers"
    else:
        text = f"You have **{len(user_whispers)}** whispers"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"{emoji.WASTEBASKET}  Delete My Whispers",
                    callback_data="delete_my_whispers"
                )
            ],
            [
                InlineKeyboardButton(
                    f"{emoji.BACK_ARROW}  Back to Main Page",
                    callback_data="start"
                )
            ]
        ]
    )
    await cq.edit_message_text(
        text=text,
        reply_markup=reply_markup
    )


@Client.on_callback_query(filters.regex("delete_my_whispers"))
async def delete_my_whispers(_, cq: CallbackQuery):
    user_id = cq.from_user.id
    deleted_whispers = [
        whispers.pop(k)
        for k, v in list(whispers.items())
        if v['sender_uid'] == user_id
    ]
    if len(deleted_whispers) == 0:
        await cq.answer("You don't have any whispers")
    else:
        await cq.answer(f"Removed {len(deleted_whispers)} whispers")
        utcnow = datetime.utcnow().strftime('%F %T')
        await cq.edit_message_text(
            f"Your whispers has been removed at `{utcnow}`",
            reply_markup=cq.message.reply_markup
        )
