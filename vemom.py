# meta developer: @werpyock0
# meta description: веном
from hikkatl.types import Message
from .. import loader, utils

@loader.tds
class VenomModule(loader.Module):
    """веном"""

    strings = {
        "name": "VenomModule",
        "description": "веном"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "enabled_chats",
                [],
                "Список ID чатов, в которых модуль активен",
                validator=loader.validators.Series(
                    loader.validators.Integer()
                ),
            ),
        )

    @loader.watcher(only_messages=True, no_commands=True)
    async def watcher(self, message: Message):
        if message.chat_id in self.config["enabled_chats"]:
            await utils.answer(message, "venom.")
            await message.delete()

    @loader.command(ru_doc="Добавить чат в список активных")
    async def addvenomchat(self, message: Message):
        """Добавить текущий чат в список активных"""
        chat_id = message.chat_id
        if chat_id not in self.config["enabled_chats"]:
            self.config["enabled_chats"].append(chat_id)
            await utils.answer(message, "Чат добавлен в список активных.")
        else:
            await utils.answer(message, "Чат уже в списке активных.")

    @loader.command(ru_doc="Удалить чат из списка активных")
    async def removevenomchat(self, message: Message):
        """Удалить текущий чат из списка активных"""
        chat_id = message.chat_id
        if chat_id in self.config["enabled_chats"]:
            self.config["enabled_chats"].remove(chat_id)
            await utils.answer(message, "Чат удален из списка активных.")
        else:
            await utils.answer(message, "Чата нет в списке активных.")
