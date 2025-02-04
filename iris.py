__version__ = (1, 0, 2)
# meta developer: @werpyock0
from hikka import loader, utils
import asyncio
from telethon.errors import TimeoutError

@loader.tds
class IrisMod(loader.Module):
    """Модуль для отправки сообщения ирису и получения ответа."""
    strings = {"name": "IrisMod"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.command()
    async def iris(self, message):
        """Отправляет команду @iris_black_bot."""
        command_text = utils.get_args_raw(message)
        if not command_text:
            await message.edit("<b>❌ Укажите команду для @iris_black_bot</b>")
            return

        bot_username = "iris_black_bot"
        try:
            async with self.client.conversation(bot_username, timeout=15) as conv:
                await conv.send_message(command_text)
                response = await conv.get_response()
                await message.edit(response.text)
        except TimeoutError:
            await message.edit("<b>❌ Бот не ответил в течение 15 секунд</b>")
        except Exception as e:
            await message.edit(f"<b>❌ Ошибка: {e}</b>")
