# seed-phrase-telegram-distributor
Python script to generate 12 words seed phrase, split it into parts, and distribute among participants over Telegram.


## Purpose
This is a script that has the same purpose as https://www.random.org/ - for clear generate, spit and distribute a seed phrase for ETH (could be changed to any other blockchain). Distribution makes over Telegram bot. 

For example, you want to generate a seed phrase with 12 words and split it between 3 participants, and send their seed's part over Telegram. For this task you need to run the command:

```
python generator.py --bot-token BOT_TOKEN --count-parts 3
```
where:
 * BOT_TOKEN - token for Telegram bot, e.g.: 1730562302:AAGQ7B0K5-_zhgzD6xN3fNNAvmB7zGTO54w
 * --count-parts 3 - mean count of participants

See the Workflow section for more information.


## Workflow
1. First, you need to create a bot over https://t.me/BotFather and get the BOT_TOKEN. More info is here: https://core.telegram.org/bots#6-botfather
2. Clone this repository and install the required library by command `pip install -r requirements.txt`
3. Run the command `python generator.py --bot-token BOT_TOKEN --count-parts 2` with correct BOT_TOKEN to distribute seed phrase between 2 participants. Then you should see such a message:
```
------------------------------------------------------------
| Generate seed phrase for 2 people(s) using bot @xspotbot |
------------------------------------------------------------

Link for invitation participants: https://t.me/xspotbot?start=1634043786387
```
4. Then you need to copy the invitation link and with no killing, the script sends them an invitation link `Link for invitation participants: https://t.me/xspotbot?start=1634043786387`
5. Each participant goes by link and starts the bot. After the needed number of participants will activate the bot - each of them will receive the address and part of the seed phrase.
6. Full script output:
```
Connected 1/2 participant: 91******55
Connected 2/2 participant: 88*****23
All participants are on the boat! Generating seed phrase and send their parts
*** SEED PHRASE GENERATED! Address is 0x1304E7db3d760833fC969062473E8a5f2967f553 ***
Base HD Path:  m/44'/60'/0'/0/0 

Sent words 1..6 to 1 participant: 91******55
Sent words 7..12 to 2 participant: 91******55
Done!
```
7. Message received by participants:
```
Word [1..6] for address 0x1304E7db3d760833fC969062473E8a5f2967f553 is: 

protect romance decorate hill snap banner
```

## Docker
You can use a prebuild Docker image: https://hub.docker.com/repository/docker/inc0dewetrust/seed-phase-distributor

To run the script just need (don't forget about `BOT_TOKEN`):
```
docker run --rm -it inc0dewetrust/seed-phase-distributor python generator.py --bot-token BOT_TOKEN --count-parts 2
```
