# meta developer: @werpyock0
from .. import loader, utils
import random
from telethon.tl.types import InputMessagesFilterGif

class KomaruMod(loader.Module):
    """Достает рандомную гифку из @komarumodgif"""
    strings = {"name": "KomaruMod"}

    async def client_ready(self, client, db):
        self.client = client

    async def komarugifcmd(self, message):
        """Рандомная гифка"""
        channel = "@komarumodgif"
        gifs = [msg async for msg in self.client.iter_messages(channel, filter=InputMessagesFilterGif)]
        if not gifs:
            await message.edit("<b>Нет доступных GIF-ов в канале!</b>")
            return
        random_gif = random.choice(gifs)
        await self.client.send_file(message.chat_id, random_gif)
        await message.delete()
