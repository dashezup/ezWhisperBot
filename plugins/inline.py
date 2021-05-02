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
from pyrogram import Client, filters, emoji
from pyrogram.types import InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery, ChosenInlineResult, User
from pyrogram.errors.exceptions.bad_request_400 import MessageIdInvalid

whispers = {}

# https://www.freeiconspng.com/downloadimg/37535
WHISPER_ICON_URL = "https://www.freeiconspng.com/uploads/whisper-icon-0.png"


@Client.on_inline_query()
async def answer_iq(_, iq: InlineQuery):
    query = iq.query
    split = query.split(' ', 1)
    if len(split) != 2:
        await iq.answer(
            results=[
                InlineQueryResultArticle(
                    title=f"{emoji.FIRE} Write a whisper message to @username",
                    input_message_content=InputTextMessageContent(
                        "**Send whisper messages through inline mode**\n\n"
                        "Usage: `@ezWhisperBot @username text`"
                    ),
                    description="Usage: @ezWhisperBot @username text",
                    thumb_url=WHISPER_ICON_URL,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Learn more...",
                                    url="https://t.me/ezWhisperBot"
                                )
                            ]
                        ]
                    )
                )
            ],
            switch_pm_text=f"{emoji.INFORMATION} Learn how to send whispers",
            switch_pm_parameter="learn"
        )
        return
    u_target = f"@{split[0].removeprefix('@')}"
    await iq.answer(
        results=[
            InlineQueryResultArticle(
                title=f"{emoji.LOCKED} A whisper message to {u_target}",
                input_message_content=InputTextMessageContent(
                    f"{emoji.LOCKED} A whisper message to {u_target}"
                ),
                description=f"{emoji.SHUSHING_FACE} {split[1]}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                f"{emoji.LOCKED_WITH_KEY} show message",
                                callback_data="show_whisper"
                            )
                        ]
                    ]
                )
            )
        ]
    )


@Client.on_chosen_inline_result()
async def chosen_inline_result(_, cir: ChosenInlineResult):
    split = cir.query.split(' ', 1)
    if len(split) != 2:
        return
    sender_uid = cir.from_user.id
    receiver_uname, text = split
    inline_message_id = cir.inline_message_id
    whispers[inline_message_id] = {
        'sender_uid': sender_uid,
        'receiver_uname': receiver_uname.removeprefix('@'),
        'text': text
    }


@Client.on_callback_query(filters.regex("^show_whisper$"))
async def answer_cq(_, cq: CallbackQuery):
    inline_message_id = cq.inline_message_id
    if not inline_message_id or inline_message_id not in whispers:
        await cq.edit_message_text(f"{emoji.NO_ENTRY} invalid")
        return
    else:
        whisper = whispers[inline_message_id]
        sender_uid = whisper['sender_uid']
        receiver_uname: str = whisper['receiver_uname']
        whisper_text = whisper['text']
        from_user: User = cq.from_user
        if from_user.username and \
                from_user.username.lower() == receiver_uname.lower():
            await cq.answer(whisper_text, show_alert=True)
            try:
                await cq.edit_message_text(
                    f"{emoji.UNLOCKED} {from_user.first_name} "
                    f"(@{from_user.username}) read the message"
                )
            except MessageIdInvalid:
                await cq.edit_message_reply_markup(None)
            whispers.pop(inline_message_id)
            return
        elif from_user.id == sender_uid:
            await cq.answer(whisper_text, show_alert=True)
            return
        else:
            await cq.answer("This is not for you", show_alert=True)
