import asyncio
import telegram

BOTTOKEN = "6904929646:AAF7Whf8oxTMRE8l70CIngGFm6sE7BWHJhg"
CHANNELID = -1002044896879

async def sendMessage(text):
    bot = telegram.Bot(BOTTOKEN)
    async with bot:
        await bot.send_message(text=text, chat_id=-1002044896879) # type: ignore