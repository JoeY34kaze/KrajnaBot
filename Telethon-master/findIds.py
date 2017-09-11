import telethon
from pprint import pprint
from telethon import TelegramClient

api_id = 78862 # change this too
api_hash = '36d610d36b1aa79625169abe74205779'
# 'session_id' can be 'your_name'. It'll be saved as your_name.session
client = TelegramClient('RecniGollum2', api_id, api_hash)
client.connect()
if not client.is_user_authorized():
	client.send_code_request('+386 31803597')
	client.sign_in('+386 31803597', input('Enter code: '))
# Now you can use the connected client as you wish
dialogs, entities = client.get_dialogs(0)
print('\n'.join('{}. {}'.format(i, str(e))
                for i, e in enumerate(entities)))
