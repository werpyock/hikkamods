__version__ = (1, 0, 0)
# meta developer: @wmodules

from .. import loader, utils

@loader.tds
class DeleterMod(loader.Module):
    """Модуль для удаления твоих сообщений."""

    strings = {"name": "DeleterMod"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.command(ru_doc="<количество> - Удаляет указанное количество твоих сообщений в текущем чате.")
    async def deleter(self, message):
        args = utils.get_args_raw(message)
        if not args.isdigit():
            await message.edit("❌ <b>Пожалуйста, укажи количество сообщений для удаления.</b>")
            return

        count = int(args)
        if count <= 0:
            await message.edit("❌ <b>Количество должно быть положительным числом.</b>")
            return

        await message.delete()

        deleted = 0
        async for msg in self.client.iter_messages(message.chat_id, from_user="me"):
            if deleted >= count:
                break
            try:
                await msg.delete()
                deleted += 1
            except Exception:
                pass

        await self.client.send_message(message.chat_id, f"✅ <b>Удалено {deleted} сообщений.</b>")
