# VoipDaily
A program for asterisk pbx servers to read your daily google calendar events and calls you to tell you them at a scheduled time. 
## How to install
> At the current moment you need your own Google OAuth2 credentials.json to make a token.pickle, in future updates it will be part of an authentication flow

Run this on your asterisk pbx server to get the tools and dialplan added:

```curl -fsSl https://raw.githubusercontent.com/mrcoat2/VoipDaily/refs/heads/main/install.sh | bash```

This automatically adds extension 262 for scheduling a call and 263 that gets your daily events.

## How to remove
### **You must remove dialplan manually**
`curl -fsSl https://raw.githubusercontent.com/mrcoat2/VoipDaily/refs/heads/main/install.sh | bash -s -- remove`

I still need to make it so it automatically removes the dialplan. For now delete the lines underneath `[wakeup-call]` inside of `/etc/asterisk/extensions_custom.conf` 
