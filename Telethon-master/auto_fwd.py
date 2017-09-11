import telethon
from telethon import TelegramClient
#from telethon.tl.functions.messages.forward_messages import ForwardMessagesRequest
#from telethon.tl.functions.messages import ForwardMessagesRequest


from telethon.tl.types import InputPeerChannel, InputPeerChat
from pprint import pprint
from time import gmtime, strftime

FROM_TO_CHATS = {
	1130120557: 389614156, # kajkam
}

def sprint(string, *args, **kwargs):
	"""Safe Print (handle UnicodeEncodeErrors on some terminals)"""
	try:
		print(string, *args, **kwargs)
	except UnicodeEncodeError:
		string = string.encode('utf-8', errors='ignore')\
					   .decode('ascii', errors='ignore')
		print(string, *args, **kwargs)

class FwdClient(TelegramClient):
	def __init__(self, session_user_id, user_phone, api_id, api_hash, proxy=None):
		super().__init__(session_user_id, api_id, api_hash, proxy)

		if not self.connect():
			print('Initial connection failed. Retrying...')
			if not self.connect():
				print('Could not connect to Telegram servers.')
				return

		# Then, ensure we're authorized and have access
		if not self.is_user_authorized():
			print('First run. Sending code request...')
			self.send_code_request(user_phone)

			self_user = None
			while self_user is None:
				code = input('Enter the code you just received: ')
				try:
					self_user = self.sign_in(user_phone, code)

				# Two-step verification may be enabled
				except SessionPasswordNeededError:
					pw = getpass('Two step verification is enabled. '
								 'Please enter your password: ')

					self_user = self.sign_in(password=pw)
		# now get input peers
		self.get_input_peers()

	def get_input_peers(self):
		global FROM_TO_CHATS

		self.from_to_dict = {}

		TO_FROM = {}

		for k, v in FROM_TO_CHATS.items():
			self.from_to_dict[k] = [None, None]
			if v in TO_FROM:
				TO_FROM[v].append(k)
			else:
				TO_FROM[v] = [k]

		_, entities = self.get_dialogs(0)
		for e in entities:
			# print(e.id, '\n------')
			if e.id in FROM_TO_CHATS:
				self.from_to_dict[e.id][0] = telethon.utils.get_input_peer(e)
			elif e.id in TO_FROM:
				for o_f in TO_FROM[e.id]:
					self.from_to_dict[o_f][1] = telethon.utils.get_input_peer(e)
		pprint(self.from_to_dict)

	def run(self):
		# Listen for updates
		self.add_update_handler(self.update_handler)
		try:
			while True:
				pass
		except KeyboardInterrupt:
			pass

	def check_update(self, update_object):
		if len(update_object.updates) == 0:
			return
		try:
			u_id = update_object.updates[0].message.to_id.channel_id
		except:
			if len(update_object.chats) == 0:
				return
			u_id = update_object.chats[0].id
		if not (u_id in self.from_to_dict):
			return
		from_ipc, to_ipc = self.from_to_dict[u_id]
		return update_object.updates, from_ipc, to_ipc

	def check_msg(self, upd):
		try:
			u_id = upd.chat_id 
			if (u_id in self.from_to_dict):
				upd_arr = [upd]
				upd_arr.extend(self.from_to_dict[u_id])
				return(upd_arr)
		except Exception as e:
			print('u.messed.up', e)
			pass

		return

	def fwd_msgs_from_chan(self, fwd_wat):
		FWD_OBJ, FROM_IPC, TO_IPC = fwd_wat[0], fwd_wat[1], fwd_wat[2]
		idz = [u.message.id for u in FWD_OBJ]
		r_idz = [telethon.helpers.generate_random_long() for _ in range(len(idz))]
		sendresp = ForwardMessagesRequest(from_peer=FROM_IPC,
									 id=idz, 
									 random_id=r_idz,
									 to_peer=TO_IPC)
		self(sendresp)

	def fwd_msgs_from_chat(self, fwd_wat):
		FWD_OBJ, FROM_IPC, TO_IPC = fwd_wat[0], fwd_wat[1], fwd_wat[2]
		iid = FWD_OBJ.id
		r_id = telethon.helpers.generate_random_long()
		sendresp = ForwardMessagesRequest(from_peer=FROM_IPC,
									 id=[iid], 
									 random_id=[r_id],
									 to_peer=TO_IPC)
		self(sendresp)


	def update_handler(self, update_object):
		try:
			self._auaua(update_object)
		except Exception as e:
			print('------------')
			print(e)
			print('------------')
			pprint(update_object)
			pprint(vars(update_object))

	def _auaua(self, update_object):
		tstamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		print(tstamp, 'got an update')
		# sprint(update_object)
		if isinstance(update_object, telethon.tl.types.updates_tg.UpdatesTg):
			any_fwd = self.check_update(update_object)
			if any_fwd is not None:
				self.fwd_msgs_from_chan(any_fwd)
		if isinstance(update_object, telethon.tl.types.UpdateShortMessage):
			if update_object.out:
				sprint('You sent {} to user #{}'.format(
					update_object.message, update_object.user_id))
			else:
				sprint('[User #{} sent {}]'.format(
					update_object.user_id, update_object.message))

		elif isinstance(update_object, telethon.tl.types.UpdateShortChatMessage):
			if update_object.out:
				sprint('You sent {} to chat #{}'.format(
					update_object.message, update_object.chat_id))
			else:
				# from group..
				any_fwd = self.check_msg(update_object)
				if any_fwd is not None:
					self.fwd_msgs_from_chat(any_fwd)
				else:
					sprint('[Chat #{}, user #{} sent {}]'.format(
						   update_object.chat_id, update_object.from_id,
						   update_object.message))
		else:
			print(type(update_object))

if __name__ == '__main__':
	api_id = 78862 # change this
	api_hash = '36d610d36b1aa79625169abe74205779'
	phone_no = '+386 31803597'
	fwww = FwdClient('RecniGollum', phone_no, api_id, api_hash)
	fwww.run()

