import logging
import json
from urllib.request import urlopen
from pyrogram import Client
from pyrogram import filters

app = Client("guardian")
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
    url = telebot_uri.format('@' + username, 'test+message')
    with urlopen(url) as f:
        print(json.load(f))

app.run()
