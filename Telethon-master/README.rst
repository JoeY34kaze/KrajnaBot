Telethon
========
.. epigraph::

  ⭐️ Thanks **everyone** who has starred the project, it means a lot!

**Telethon** is Telegram client implementation in **Python 3** which uses
the latest available API of Telegram. Remember to use **pip3** to install!


Installing Telethon
-------------------
Installing Telethon via pip

On a terminal, issue the following command:

sudo -H pip install telethon
If you get something like "SyntaxError: invalid syntax" on the from error line, it's because pip defaults to Python 2. Use pip3 instead.

If you already have Telethon installed, upgrade with pip install --upgrade telethon!

Installing Telethon manually

Install the required pyaes and rsa modules: sudo -H pip install pyaes rsa (GitHub, package index)
Clone Telethon's GitHub repository: git clone https://github.com/LonamiWebs/Telethon.git
Enter the cloned repository: cd Telethon
Run the code generator: python3 setup.py gen_tl
Done!
To speed up the crypto part of Telethon, you should also install sympy and libssl on your computer. This step is optional.



-------------
Running the bot
- once telethom is working run it with
- python startBot.py
