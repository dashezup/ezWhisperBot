# import logging
from pyrogram import Client

plugins = dict(
    root="plugins",
    include=[
        "inline",
        "private"
    ]
)

# logging.basicConfig(level=logging.DEBUG)
print('>>> BOT STARTED')
Client("ezWhisperBot", plugins=plugins).run()
print('\n>>> BOT STOPPED')
