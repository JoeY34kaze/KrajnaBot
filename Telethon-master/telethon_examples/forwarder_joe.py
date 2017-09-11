import os
from getpass import getpass

from telethon import TelegramClient, ConnectionMode
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import UpdateShortChatMessage, UpdateShortMessage
from telethon.utils import get_display_name
import time


from1=1130120557
from2=1145370905

from1ID=0
from2ID=0


to1=1123059821
to1ID=0

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
    """Full featured Telegram client, meant to be used on an interactive
       session to see what Telethon is capable off -

       This client allows the user to perform some basic interaction with
       Telegram through Telethon, such as listing dialogs (open chats),
       talking to people, downloading media, and receiving updates.
    """
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
                elif entities[x].id == from1 :
                    print("najden")
                    print(entities[x].id)
                    from1ID = x
                elif entities[x].id == from2 :
                    print("najden")
                    print(entities[x].id)
                    from2ID = x

                    #self.send_message(
                     #   entities[x], 'shit works yo', link_preview=False)



        total_count, messages, senders = self.get_message_history(
                        entities[from1ID], limit=20)
        messages_from1=messages
        total_count, messages, senders = self.get_message_history(
                        entities[from2ID], limit=20)
        messages_from2=messages

      #  for msg in messages_from1:
       #     print(msg.message)
        #    print('----------------')

        time.sleep(5)
        while True:
            total_count, messages, senders = self.get_message_history(
                entities[from1ID], limit=20)
            messages_from1_new = messages

            total_count, messages, senders = self.get_message_history(
                entities[from2ID], limit=20)
            messages_from2_new = messages

            if(messages_from1[0].message != messages_from1_new[0].message):
                print("TREBA JE SYNCAT!!")
                start_writing=False
                for msg in reversed(messages_from1_new):
                    if(start_writing == True):
                        self.send_message(
                        entities[to1ID], msg.message, link_preview=False)
                    if(msg.message==messages_from1[0].message):
                        start_writing=True

            messages_from1=messages_from1_new

            if (messages_from2[0].message != messages_from2_new[0].message):
                print("TREBA JE SYNCAT!!")
                start_writing = False
                for msg in reversed(messages_from2_new):
                    if (start_writing == True):
                        self.send_message(
                            entities[to1ID], msg.message, link_preview=False)
                    if (msg.message == messages_from2[0].message):
                        start_writing = True
            messages_from1=messages_from1_new

            time.sleep(30)




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
        if isinstance(update_object, UpdateShortMessage):
            if update_object.out:
                sprint('You sent {} to user #{}'.format(
                    update_object.message, update_object.user_id))
            else:
                sprint('[User #{} sent {}]'.format(
                    update_object.user_id, update_object.message))

        elif isinstance(update_object, UpdateShortChatMessage):
            if update_object.out:
                sprint('You sent {} to chat #{}'.format(
                    update_object.message, update_object.chat_id))
            else:
                sprint('[Chat #{}, user #{} sent {}]'.format(
                       update_object.chat_id, update_object.from_id,
                       update_object.message))
