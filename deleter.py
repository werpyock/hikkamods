__version__ = (1, 2, 0)
# meta developer: @werpyock0

from .. import loader, utils

@loader.tds
class DeleterMod(loader.Module):
    """Модуль для удаления твоих сообщений в указанном чате или текущем чате (не используй для удаления слишком много)."""

    strings = {"name": "DeleterMod"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.command(ru_doc="<количество> [чат_id | username] - Удаляет указанное количество твоих сообщений.")
    async def deleter(self, message):
        args = utils.get_args(message)
        
        if not args:
            await message.edit("❌ <b>Укажи количество сообщений для удаления.</b>")
            return

        count = args[0]
        if not count.isdigit():
            await message.edit("❌ <b>Количество должно быть числом.</b>")
            return

        count = int(count)
        if count <= 0:
            await message.edit("❌ <b>Количество должно быть положительным.</b>")
            return

        chat_id = message.chat_id

        if len(args) > 1:
            chat_id = args[1]
            if chat_id.lstrip("-").isdigit():
                chat_id = int(chat_id)

        try:
            entity = await self.client.get_entity(chat_id)
            chat_id = entity.id
        except Exception:
            await message.edit("❌ <b>Не удалось найти указанный чат.</b>")
            return

        await message.delete()

        deleted = 0
        async for msg in self.client.iter_messages(chat_id, from_user="me"):
            if deleted >= count:
                break
            try:
                await msg.delete()
                deleted += 1
            except Exception:
                pass

        await self.client.send_message(chat_id, f"✅ <b>Удалено {deleted} сообщений.</b>")
