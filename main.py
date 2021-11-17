import asyncio
import webbrowser
import os
import re

from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import Message
import simpleaudio as sa
import rgbcontrol

CHANNEL_ID = 1218633492 # FE PartAlert
# CHANNEL_ID = 1685409009 # Test channel
SELF_ID = 1302716583

load_dotenv()

API_ID = os.environ['API_ID']
API_HASH = os.environ['API_HASH']
GPU_MODEL = os.environ['GPU_MODEL']
WEBSITE = os.environ['WEBSITE']
RGBALARM = os.environ['RGBALARM']

client = TelegramClient('anon', API_ID, API_HASH)
alarm_obj = sa.WaveObject.from_wave_file('./alarm.wav')
chrome = webbrowser.get('C:/Program Files/Google/Chrome/Application/chrome.exe %s')
rgbControl = None
if RGBALARM == 'TRUE':
    rgbControl = rgbcontrol.RGBControl()

def parse_notify(message: Message):
    gpu, region = (None,)*2
    match = re.search(r'(RTX \d{4}(?: Ti)?)\s*(?:\((\w{2})\))?', message.raw_text)
    if match is not None:
        gpu, region = match.groups()

    url = None
    match = re.search(r'https?://(?:www\.)?\w+\.(?:com|nl|de|it|es|co\.uk)(?:/)?[\w+\+-/:@&=$,]+', message.raw_text)
    if match is not None:
        url = match.group(0)

    return (gpu, region, url, message.date)

@client.on(events.NewMessage(chats=CHANNEL_ID, incoming=True))
async def msg_handler(event: events.NewMessage.Event):
    gpu, region, url, date = parse_notify(event)
    if gpu == GPU_MODEL and url is not None and WEBSITE in url:
        print(f'{date}\t{gpu}\t{region}\t{url}')
        chrome.open_new(url)
        alarm_obj.play()
        if rgbControl is not None:
            asyncio.create_task(rgbControl.Blink(0x000000ff, 0x00000000, 15))


async def main():
    await client.start()
    
    await client.get_me()
    await client.get_dialogs()

    # async for dialog in client.iter_dialogs():
    #     print("{:>14}: {}".format(dialog.entity.id, dialog.title))
    

    # async for message in client.iter_messages(entity=CHANNEL_ID, limit=None):
    #     if message.raw_text:
    #         gpu, region, url, date = parse_notify(message)


if __name__ == '__main__':
    client.loop.run_until_complete(main())
    client.run_until_disconnected()