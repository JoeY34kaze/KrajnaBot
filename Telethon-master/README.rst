Telethon
========
.. epigraph::

  ⭐️ Thanks **everyone** who has starred the project, it means a lot!

**Telethon** is Telegram client implementation in **Python 3** which uses
the latest available API of Telegram. Remember to use **pip3** to install!

Installing
----------

.. code:: sh

  pip install telethon




Doing stuff
-----------

.. code:: python

  print(me.stringify())

  client.send_message('username', 'Hello! Talking to you from Telethon')
  client.send_file('username', '/home/myself/Pictures/holidays.jpg')

  client.download_profile_photo(me)
  total, messages, senders = client.get_message_history('username')
  client.download_media(messages[0])


Next steps
----------

Once you've decided that you like the way Telethon looks and feel comfortable
with this code, go ahead and read the full
`README <https://github.com/LonamiWebs/Telethon/blob/HEAD/README-long.rst>`_ :)
