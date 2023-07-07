#    Copyright (C) 2021 - Avishkar Patil | @AvishkarPatil


import os
import sys
import time
import logging
import pyrogram
import aiohttp
import asyncio
import requests
import aiofiles
from random import randint
from progress import progress
from config import Config
from pyrogram.errors import UserNotParticipant, UserBannedInChannel
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQuery, InputTextMessageContent


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

DOWNLOAD = "./"

# vars
APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
BOT_TOKEN = Config.BOT_TOKEN


bot = Client(
    "AnonFilesBot",
    api_id=APP_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN)


START_TEXT = """
__**𝐒𝐞𝐧𝐝𝐂𝐌𝐁𝐨𝐓**  \n\n𝐔𝐩𝐥𝐨𝐚𝐝 𝐅𝐢𝐥𝐞𝐬 𝐓𝐨 𝐒𝐞𝐧𝐝.𝐜𝐦\n\n𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐝 𝐛𝐲 :** @SirdLay**
"""
HELP_TEXT = """
**𝐒𝐞𝐧𝐝𝐂𝐌𝐁𝐨𝐓 Hᴇʟᴘ**\n\n𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐌𝐞 𝐅𝐨𝐫 𝐒𝐮𝐩𝐩𝐨𝐫𝐭\n\n** @SirdLay**
"""
ABOUT_TEXT = """
- **Bot :** `SendCMBoT`
- **Creator :** [SirdLay](https://telegram.me/SirdLay)
"""

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )


@bot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT,
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    else:
        await update.message.delete()


@bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT
    reply_markup = START_BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )


@bot.on_message(filters.media & filters.private)
async def upload(client, message):
    if Config.UPDATES_CHANNEL is not None:
        try:
            user = await client.get_chat_member(Config.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.chat.id,
                    text="**Contact** [Dᴇᴠᴇʟᴏᴘᴇʀ](https://telegram.me/SirdLay).",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.chat.id,
                text="**Pʟᴇᴀsᴇ Jᴏɪɴ Mʏ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ Tᴏ Usᴇ Mᴇ 🏃‍♂**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ", url=f"https://t.me/{Config.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.chat.id,
                text="**Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ Wʀᴏɴɢ! Cᴏɴᴛᴀᴄᴛ ᴍʏ** [Dᴇᴠᴇʟᴏᴘᴇʀ](https://telegram.me/SirdLay).",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    m = await message.reply("**Dᴏᴡɴʟᴏᴀᴅɪɴɢ Yᴏᴜʀ FIʟᴇs Tᴏ Mʏ Sᴇʀᴠᴇʀ ....** ")
    now = time.time()
    sed = await bot.download_media(
                message, DOWNLOAD,
          progress=progress,
          progress_args=(
            "**Uᴘʟᴏᴀᴅ Pʀᴏᴄᴇss Sᴛᴀʀᴇᴅ Wᴀɪᴛ ᴀɴᴅ Wᴀᴛᴄʜ Mᴀɢɪᴄ**\n**Iᴛs Tᴀᴋᴇ ᴛɪᴍᴇ Aᴄᴄᴏʀᴅɪɴɢ Yᴏᴜʀ Fɪʟᴇs Sɪᴢᴇ** \n\n**ᴇᴛᴀ:** ",
            m,
            now
            )
        )
    try:
        with open(sed, 'rb') as f:
            files = {'file': (os.path.basename(sed), f)}


            await m.edit("**Uᴘʟᴏᴀᴅɪɴɢ ᴛᴏ Send.cm Sᴇʀᴠᴇʀ Pʟᴇᴀsᴇ Wᴀɪᴛ**")

            init_url = f'https://send.cm/api/upload/server?key=166147hy7jizm8k2dcoysj'
            init_response = requests.get(init_url)

            if init_response.status_code != 200:
                raise Exception("Failed to initialize upload with status code: {}".format(init_response.status_code))

            init_data = init_response.json()
            upload_url = init_data.get('result')
            sess_id = init_data.get('sess_id')

            if not upload_url or not sess_id:
                raise Exception("Missing 'result' or 'sess_id' in response.")

            data = {'sess_id': sess_id}
            upload_response = requests.post(upload_url, files=files, data=data)

            print(type(upload_response.json()), upload_response.json())

            final_url = upload_response.json()
            filecode = final_url[0].get('file_code')

            if upload_response.status_code != 200:
                raise Exception("Failed to upload file with status code: {}".format(upload_response.status_code))


            output = f"""
            <u>**Fɪʟᴇ Uᴘʟᴏᴀᴅᴇᴅ Tᴏ Send.cm**</u>


            **Dᴏᴡɴʟᴏᴀᴅ Lɪɴᴋ:** `https://send.cm/{filecode}`

            """

            btn = InlineKeyboardMarkup(
               [[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ Fɪʟᴇ", url=f"https://send.cm/{filecode}")]])


            await m.edit(output, reply_markup=btn)
            os.remove(sed)
    except Exception as e:
        await m.edit(f"Pʀᴏᴄᴇss Fᴀɪʟᴇᴅ, Mᴀʏʙᴇ Tɪᴍᴇ Oᴜᴛ Dᴜᴇ Tᴏ Lᴀʀɢᴇ Fɪʟᴇ Sɪᴢᴇ! Error: {str(e)}__")
        return



bot.start()
print("SendCMBoT Is Started!,  if Have Any Problems contact @SirdLay")
idle()