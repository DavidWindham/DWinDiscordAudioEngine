# DWin's DiscordAudioEngine

A simple open source discord music player bot

## Setup

1. Clone the repo, open the folder, and install requirements with the following commands
```
git clone https://github.com/DavidWindham/DWinDiscordAudioEngine.git
cd DWinDiscordAudioEngine
pip install -r requirements.txt
```

2. Create a discord bot using the discord developers dashboard [here](https://discord.com/developers/applications) and set the "TOKEN" variable in the .env file with the token your bot generates

3. (optional) set the MongoDB URI and Port in the .env file if you wish for a stateful bot, without the bot will just run in stateless mode

4. Invite the bot to your server with the following permissions
  ![image](https://user-images.githubusercontent.com/41753798/166912232-32d8c1a5-f06d-473e-ac2f-8cc8b77e09d3.png)

5. Start the bot with the following command
```
python main.py
```


## Still to implement
* Get history
* Refactor better dependency injection for elements such as the MessageHandler
