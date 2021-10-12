"""
Copyright (C) seed-phrase-telegram-distributor InCode-WeTrust (in.c.w.trust@gmail.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import telebot
import argparse
import time
import math

# https://github.com/meherett/python-hdwallet
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from typing import Optional

PASSPHRASE: Optional[str] = None


def generate_seed():
	# Generate english mnemonic words
	mnemonic: str = generate_mnemonic(language="english", strength=128)
	# Secret passphrase/password for mnemonic

	# Initialize Ethereum mainnet BIP44HDWallet
	bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
	# Get Ethereum BIP44HDWallet from mnemonic
	bip44_hdwallet.from_mnemonic(
		mnemonic=mnemonic, language="english", passphrase=PASSPHRASE
	)
	# Clean default BIP44 derivation indexes/paths
	bip44_hdwallet.clean_derivation()

	# Derivation from Ethereum BIP44 derivation path
	bip44_derivation: BIP44Derivation = BIP44Derivation(
		cryptocurrency=EthereumMainnet, account=0, change=False, address=0
	)
	# Drive Ethereum BIP44HDWallet
	bip44_hdwallet.from_path(path=bip44_derivation)
	# Print address_index, path, address and private_key
	addr = bip44_hdwallet.address()
	# Clean derivation indexes/paths
	bip44_hdwallet.clean_derivation()
	return [mnemonic.split(" "), addr]

def mask_partic_id(id):
	id = str(id)
	return id[:2] + ("*" * (len(id)-1)) + id[-2:]


def main(args):
	print()
	print()

	bot = telebot.TeleBot(args.bot_token, threaded=False)
	count_participants = args.count_parts
	bot_name = bot.get_me().username
	invite_token = str(int(time.time()*1000))
	participants = []

	welcome_mess = f"| Generate seed phrase for {count_participants} people(s) using bot @{bot_name} |"
	border_mess = "%s" % ("-" * (len(welcome_mess)) )
	print(border_mess)
	print(welcome_mess)
	print(border_mess)

	print()

	print(f"Link for invitation participants: https://t.me/{bot_name}?start={invite_token}")

	@bot.message_handler(commands=['start'])
	def invited_participant(message):
		if message.text.find(invite_token) < 0:
			print(f"Failed participant's [{mask_partic_id(message.chat.id)}] invitation token")
			return None
		participant_id = message.chat.id
		if participant_id in participants:
			print(f"Participant [{mask_partic_id(message.chat.id)}] is in the list already")
			return None

		participants.append(participant_id)
		print(f"Connected {len(participants)}/{count_participants} participant: {mask_partic_id(message.chat.id)}")
		if len(participants) == count_participants:
			# generate and send to parts
			print("All participants are on the boat! Generating seed phrase and send their parts")
			seed, addr = generate_seed()
			print(f"*** SEED PHRASE GENERATED! Address is {addr} ***")
			print("Base HD Path:  m/44'/60'/0'/0/0", "\n")

			cperp = math.ceil(len(seed)/count_participants)
			seed_parts = [seed[i: i+cperp] for i in range(0, len(seed), cperp)]
			for i in range(count_participants):
				bot.send_message(participants[i], f"Word [{i*cperp+1}..{(i+1)*cperp}] for address {addr} is: \n\n{' '.join(seed_parts[i])}")
				print(f"Sent words {i*cperp+1}..{(i+1)*cperp} to {i+1} participant: {mask_partic_id(participants[i])}")
			print("Done!")
			print(border_mess)
			bot.stop_bot()
		else:
			bot.send_message(participant_id, "Great! Waiting for the other participants...")


	bot.polling(none_stop=False)

	print()
	print()


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--bot-token', type=str, required=True, help="Telegram bot token to communicate with participants")
	parser.add_argument('--count-parts', type=int, required=True, help="How many participants waiting")
	return parser.parse_args()


if __name__ == '__main__':
	main(parse_args())
