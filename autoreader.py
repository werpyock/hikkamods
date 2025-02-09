__version__ = (1, 1, 0)
# meta developer: @wmodules

from .. import loader, utils
from telethon.tl.types import User, Chat, Channel

@loader.tds
class AutoReaderMod(loader.Module):
    """Авточиталка сообщений в указанных в конфиге чатов."""

    strings = {"name": "AutoReaderMod"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "CHATS", [], lambda: "Список чатов для авточиталки."
        )

    async def client_ready(self, client, db):
        self.client = client

    def get_display_name(self, entity):
        if isinstance(entity, User):
            return f"{entity.first_name or ''} {entity.last_name or ''}".strip()
        if isinstance(entity, (Chat, Channel)):
            return entity.title
        return str(entity)

    @loader.command()
    async def autoread(self, message):
        """Добавляет указанный чат в список авточиталки. Использование: .autoread [chat_id или @username] (если чат не указан, используется текущий чат)."""
        args = utils.get_args_raw(message)
        chat = await self.client.get_entity(args) if args else await message.get_chat()
        chat_id = chat.id
        chat_title = self.get_display_name(chat)
        auto_read_chats = self.config["CHATS"]

        if chat_id not in auto_read_chats:
            auto_read_chats.append(chat_id)
            self.config["CHATS"] = auto_read_chats
            await message.edit(f"✅Чат '{chat_title}' добавлен в список авточиталки")
        else:
            await message.edit(f"ℹ️Чат '{chat_title}' уже находится в списке авточиталки.")

    @loader.command()
    async def unautoread(self, message):
        """Удаляет указанный чат из списка авточиталки. Использование: .unautoread [chat_id или @username] (если чат не указан, используется текущий чат)."""
        args = utils.get_args_raw(message)
        chat = await self.client.get_entity(args) if args else await message.get_chat()
        chat_id = chat.id
        chat_title = self.get_display_name(chat)
        auto_read_chats = self.config["CHATS"]

        if chat_id in auto_read_chats:
            auto_read_chats.remove(chat_id)
            self.config["CHATS"] = auto_read_chats
            await message.edit(f"✅Чат '{chat_title}' удален из списка авточиталки.")
        else:
            await message.edit(f"❌Чат '{chat_title}' отсутствует в списке авточиталки.")

    @loader.watcher()
    async def watcher(self, message):
        chat_id = utils.get_chat_id(message)
        if chat_id in self.config["CHATS"]:
            async for msg in self.client.iter_messages(chat_id, limit=1):
                await msg.mark_read()
