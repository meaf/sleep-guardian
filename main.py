import asyncio
import logging
import os
import time
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from pyrogram.types import ChatPermissions

import time
from time import sleep
import random
from pyrogram import Client
from pyrogram import filters
from pytgcalls import idle
from pytgcalls import PyTgCalls
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream

import misc

POOL_SIZE = 10

app = Client("guardian")
app_caller = PyTgCalls(app)
app_caller.start()

father = "meaffs"
alarm_msg_markers = ['укритт',
                     'сирен',
                     'тривог'
                     ]

track_channels = {'yaremche_live': [father], 'boryspilnews': [father]}

telebot_uri = 'http://api.callmebot.com/start.php?' \
              'user={}' \
              '&text={}' \
              '&rpt=2' \
              '&cc=yes'
# '&timeout=[time out]'


def make_client():
    return Client("caller")


async def make_call(username):
    file = './input.raw'
    while not os.path.exists(file):
        time.sleep(0.125)
    await get_caller().join_group_call(
        username,
        InputStream(
            InputAudioStream(
                file,
            ),
        ),
        stream_type=StreamType().local_stream,
    )


async def hang(username):
    await get_caller().leave_group_call(
        username,
    )


@app.on_message(filters.regex('!p1'))
async def call2(_, msg):
    file = './input.raw'
    while not os.path.exists(file):
        await asyncio.sleep(0.125)
    await app_caller.join_group_call(
        msg.chat.id,
        InputStream(
            InputAudioStream(
                file,
            ),
        ),
        stream_type=StreamType().local_stream,
    )


@app.on_message(filters.regex('!s1'))
async def hang2(_, msg):
    await app_caller.leave_group_call(
        msg.chat.id,
    )


def get_caller():
    return app_caller
    # last_active[0] += 1
    #
    # return hotline[last_active[0] % 10]


# clients_pool = [make_client()] * POOL_SIZE
# hotline = []
# for cli in clients_pool:
#     caller = PyTgCalls(cli)
#     caller.start()
#     hotline.append(PyTgCalls(cli))
#
# last_active = [0]

###############################################################################
################################  CALL PART END
###############################################################################

@app.on_message(filters.text & filters.user)
def join_channel_request(_, msg):
    orig_text = msg.text
    app.send_message(father, "request from " + msg.from_user.username
                     + " to join channel: ")
    app.send_message(father, orig_text)
    app.join_chat(orig_text)


@app.on_message(filters.channel & filters.text)
def alert(_, msg):
    orig_text = msg.text
    for marker in alarm_msg_markers:
        if marker.casefold() in orig_text.casefold():
            channel = msg.sender_chat.title
            if channel in track_channels:
                users_to_alert = track_channels[channel]
                for username in users_to_alert:
                    alert_user(username)
                    logging.log(logging.INFO, username + 'alerted')
            else:
                logging.log(logging.WARNING,
                            " channel has no recipients: " + orig_text
                            + " markers: " + alarm_msg_markers.__str__()
                            + " track_channels: " + track_channels.__str__())
                alert_user(father)


def join_channel(username, channel):
    app.join_chat(channel)
    track_channels[channel] += [username]


def alert_user(username):
    logging.log(logging.INFO, username + 'alerted')
    app.send_message(username, "test alert message")
    asyncio.get_event_loop().run_until_complete(make_call(username))


    # url = telebot_uri.format('@' + username, )
    # with urlopen(url) as f:
    #     resp = json.load(f)




####################################################################
####################################################################
####################################################################
####################################################################

# Команда type
@app.on_message(filters.command("type", prefixes=".") & filters.me)
def type(_, msg):
    orig_text = msg.text.split(".type ", maxsplit=1)[1]
    text = orig_text
    tbp = "" # to be printed
    typing_symbol = "▒"

    while(tbp != orig_text):
        try:
            msg.edit(tbp + typing_symbol)
            sleep(0.05) # 50 ms

            tbp = tbp + text[0]
            text = text[1:]

            msg.edit(tbp)
            sleep(0.05)

        except FloodWait as e:
            sleep(e.x)



# misc.use_all()
# app.run()
idle()