import json
import logging
from urllib.request import urlopen

from pyrogram import Client, idle
from pyrogram import filters
from pyrogram.errors import UsernameInvalid

from constants import *

app = Client("guardian")


@app.on_message(filters.command("join", prefixes="/"))
def join_channel_request(_, msg):
    try:
        channel_name = msg.text.split("/join ", maxsplit=1)[1]
        app.send_message(father, "request from " +
                         msg.from_user.username
                         + " to join channel " + channel_name)
        join_channel(msg.from_user.username, channel_name)
        app.send_message(msg.from_user.username, "Joined " + channel_name)
    except UsernameInvalid as e:
        app.send_message(msg.from_user.username, "Failed to join a channel! "
                                                 "request format:"
                                                 "\n/join @channelname")


@app.on_message(filters.command("leave", prefixes="/"))
def leave_channel_request(_, msg):
    try:
        channel_name = msg.text.split("/leave ", maxsplit=1)[1]
        app.send_message(father, "request from " +
                         msg.from_user.username
                         + " to leave channel " + channel_name)
        if leave_channel(msg.from_user.username, channel_name):
            app.send_message(msg.from_user.username, "Joined " + channel_name)
    except UsernameInvalid as e:
        app.send_message(msg.from_user.username, "Failed to join a channel! "
                                                 "request format:"
                                                 "\n/join @channelname")


@app.on_message(filters.command("help", prefixes="/"))
def show_help(_, msg):
    app.send_message(msg.from_user.username, HELP_MSG1)
    app.send_message(msg.from_user.username, HELP_MSG2)
    app.send_message(msg.from_user.username, HELP_MSG3)
    app.send_message(msg.from_user.username, HELP_MSG4)
    app.send_message(msg.from_user.username, alarm_msg_markers.join(', '))


@app.on_message(filters.channel & filters.text)
def alert(_, msg):
    orig_text = msg.text
    for marker in alarm_msg_markers:
        if marker.casefold() in orig_text.casefold():
            channel = msg.sender_chat.title
            if channel in track_channels:
                users_to_alert = track_channels[channel]
                for username in users_to_alert:
                    alert_user(username, msg)
                    logging.log(logging.INFO, username + "alerted")
            else:
                logging.log(logging.WARNING,
                            " channel has no recipients: " + orig_text
                            + "\nmarkers: " + alarm_msg_markers.__str__()
                            + "\ntrack_channels: " + track_channels.__str__())
                alert_user(father, msg)


@app.on_message(filters.command("ping", prefixes="/"))
def ping_back(_, msg):
    app.send_message(msg.from_user.username, "I'm here =)")


@app.on_message(filters.command("test_call", prefixes="/"))
def ping_back(_, msg):
    app.send_message(msg.from_user.username, "I'm here =)")


def join_channel(username, channel):
    app.join_chat(channel)
    channel = channel.replace("@", "")
    if channel not in track_channels:
        track_channels[channel] = []
    if username not in track_channels[channel]:
        track_channels[channel].append(username)
    save_dictionary()

def leave_channel(username, channel):
    channel = channel.replace("@", "")
    if channel not in track_channels:
        app.send_message(username,
                         "you are not subscribed to this channel's alerts")
        return False
    if username not in track_channels[channel]:
        app.send_message(username,
                         "you are not subscribed to this channel's alerts")
        return False
    track_channels[channel].remove(username)
    if not track_channels[channel]:
        app.leave_chat(channel)
    save_dictionary()
    return True


def alert_user(username, msg):
    app.send_message(username, msg.sender_chat.title + ": " + msg.text)
    url = telebot_uri.format("@" + username, "Alert!")
    with urlopen(url) as f:
        print(json.load(f))
    logging.log(logging.INFO, username + "alerted")


def save_dictionary():
    with open("./store/subscriptions", "w") as data:
        data.write(str(track_channels))


def load_data(path):
    with open(path) as f:
        data = f.read()
    return json.loads(data.replace("'", '"'))


def on_startup():
    app.send_message(father, "Guardian started...")


telebot_uri = "http://api.callmebot.com/start.php?user={}&text={}&rpt=2&cc=yes"
alarm_msg_markers = load_data("./store/markers")
track_channels = load_data("./store/subscriptions")

app.start()
on_startup()

idle()
