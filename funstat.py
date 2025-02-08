__version__ = (1, 1, 0)
# meta developer: @wmodules
from hikka import loader, utils
from telethon.tl.types import Message
from telethon import events

@loader.tds
class FunstatMod(loader.Module):
    """Модуль на фанстат, использует бота @fanstarttt_bot чтобы получить ответ."""
    strings = {"name": "FunstatMod"}

    async def client_ready(self, client, db):
        self.client = client
        self.bot_username = '@fanstarttt_bot'

    async def funstatcmd(self, message: Message):
        """Отправляет команду фанстату."""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("Пожалуйста, укажите команду для отправки боту.")
            return

        async with self.client.conversation(self.bot_username) as conv:
            await conv.send_message(args)
            response = await conv.get_response()

            sent_message = await message.respond(
                response.text,
                buttons=response.buttons
            )

            @self.client.on(events.MessageEdited(chats=conv.chat_id))
            async def handler(event):
                if event.message.from_id == (await self.client.get_peer_id(self.bot_username)):
                    await sent_message.edit(
                        event.text,
                        buttons=event.buttons
                    )
