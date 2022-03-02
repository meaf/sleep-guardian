# Sleep-guardian 🇺🇦
Russian warship, go f*ck yourself

### What is this (user)bot for?
This bot is aimed to make a call to registered users when a post with certain words is received from a channel, that user has requested the bot to track  

Curently it saves data to files and  makes calls from external API - two points that has to be improved 
### Installation guideline: 

```bash
apt install python3.9
apt install python3-pip
pip3 install tgcrypto
pip3 install pyrogram
pip3 install -U pytgcalls[pyrogram]
```

replace `{api_id}` / `{api_hash}` with yours from https://my.telegram.org/apps
```bash
git clone https://github.com/meaf/sleep-guardian.git
cd sleep-guardian
mv ./store /tmp/store
echo '[pyrogram]
api_id = {api_id}
api_hash = {api_hash}' > config.ini
python3.8 main.py
``` 
log in to you account with first launch of the guardian


###  Install as a service (linux for now)
to not risk it exiting in the middle of the night, we need to install it as a service

you also might want to change path to main.py in `./service/sleep-guardian.service` and change father's name in constants.py and in store/subscriptions =) 
```bash
mv ./service/sleep-guardian.service /usr/lib/systemd/system/
systemctl stop sleep-guardian.service
systemctl daemon-reload
systemctl enable sleep-guardian.service
systemctl start sleep-guardian.service
systemctl status sleep-guardian.service
```