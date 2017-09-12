import os
from getpass import getpass

from telethon import TelegramClient, ConnectionMode
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import UpdateShortChatMessage, UpdateShortMessage
from telethon.utils import get_display_name
import time
from datetime import datetime

msgToSend=None
from1=1130120557 #subodh
#from1=1134996697 #test
from2=1145370905 #whales

from1ID=0
from2ID=0


to1=1123059821

to1ID=0
to1hash=-5299655350369332983

def sprint(string, *args, **kwargs):
    """Safe Print (handle UnicodeEncodeErrors on some terminals)"""
    try:
        print(string, *args, **kwargs)
    except UnicodeEncodeError:
        string = string.encode('utf-8', errors='ignore')\
                       .decode('ascii', errors='ignore')
        print(string, *args, **kwargs)


def print_title(title):
    # Clear previous window
    print('\n')
    print('=={}=='.format('=' * len(title)))
    sprint('= {} ='.format(title))
    print('=={}=='.format('=' * len(title)))


def bytes_to_string(byte_count):
    """Converts a byte count to a string (in KB, MB...)"""
    suffix_index = 0
    while byte_count >= 1024:
        byte_count /= 1024
        suffix_index += 1

    return '{:.2f}{}'.format(byte_count,
                             [' bytes', 'KB', 'MB', 'GB', 'TB'][suffix_index])


class InteractiveTelegramClient(TelegramClient):

    def __init__(self, session_user_id, user_phone, api_id, api_hash,
                 proxy=None):
        print_title('Initialization - Krajna')

        print('Initializing interactive example...')
        super().__init__(
            session_user_id, api_id, api_hash,
            connection_mode=ConnectionMode.TCP_ABRIDGED,
            proxy=proxy
        )

        # Store all the found media in memory here,
        # so it can be downloaded if the user wants
        self.found_media = set()

        print('Connecting to Telegram servers...')
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

    def run(self):
        # Listen for updates
        self.add_update_handler(self.update_handler)

        # Enter a while loop to chat as long as the user wants


        # Retrieve the top dialogs
        dialog_count = 50

        # Entities represent the user, chat or channel
        # corresponding to the dialog on the same index
        dialogs, entities = self.get_dialogs(dialog_count)


        # Retrieve the selected user (or chat, or channel)
        for x in range(0, len(entities)):
                if entities[x].id == to1 :
                    print("najden")
                    print(entities[x].id)
                    to1ID=x
                    to1hash=entities[x].access_hash
                    print(to1hash)
                elif entities[x].id == from1 :
                    print("najden")
                    print(entities[x].id)
                    from1ID = x
                elif entities[x].id == from2 :
                    print("najden")
                    print(entities[x].id)
                    from2ID = x

        while True:
            global msgToSend
            if(msgToSend is not None):
                self.send_message(entities[to1ID], msgToSend)
                msgToSend=None
                print ('Message forwarded')





    def send_photo(self, path, entity):
        self.send_file(
            entity, path,
            progress_callback=self.upload_progress_callback
        )
        print('Photo sent!')

    def send_document(self, path, entity):
        self.send_file(
            entity, path,
            force_document=True,
            progress_callback=self.upload_progress_callback
        )
        print('Document sent!')

    def download_media_by_id(self, media_id):
        try:
            # The user may have entered a non-integer string!
            msg_media_id = int(media_id)

            # Search the message ID
            for msg in self.found_media:
                if msg.id == msg_media_id:
                    print('Downloading media to usermedia/...')
                    os.makedirs('usermedia', exist_ok=True)
                    output = self.download_media(
                        msg.media,
                        file='usermedia/',
                        progress_callback=self.download_progress_callback
                    )
                    print('Media downloaded to {}!'.format(output))

        except ValueError:
            print('Invalid media ID given!')

    @staticmethod
    def download_progress_callback(downloaded_bytes, total_bytes):
        InteractiveTelegramClient.print_progress('Downloaded',
                                                 downloaded_bytes, total_bytes)

    @staticmethod
    def upload_progress_callback(uploaded_bytes, total_bytes):
        InteractiveTelegramClient.print_progress('Uploaded', uploaded_bytes,
                                                 total_bytes)

    @staticmethod
    def print_progress(progress_type, downloaded_bytes, total_bytes):
        print('{} {} out of {} ({:.2%})'.format(progress_type, bytes_to_string(
            downloaded_bytes), bytes_to_string(total_bytes), downloaded_bytes /
                                                total_bytes))

    @staticmethod
    def update_handler(update_object):
        try:
            if(update_object.updates[1].message.to_id.channel_id==from1):
                global msgToSend
                msgToSend=update_object.updates[1].message.message
                print(update_object.updates[1].message)
        except:
            pass


