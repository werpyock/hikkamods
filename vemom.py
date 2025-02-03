# meta developer: @werpyock0
# meta description: сразу включается. везде Веном пишет лучше не устанавливать

from hikkatl.types import Message
from .. import loader, utils

@loader.tds
class VenomModule(loader.Module):
    strings = {
        "name": "Venomod",
        "description": "везде веном"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "status",
                True,
                "Enable or disable the module",
                validator=loader.validators.Boolean(),
            ),
        )

    @loader.watcher(
        only_messages=True,
        no_commands=True,
    )
    async def watcher(self, message: Message):
        if not self.config["status"]:
            return
        if message.chat_id:
            await utils.answer(message, "venom.")
            await message.delete()

    @loader.command(ru_doc="Включить/выключить модуль")
    async def togglevenom(self, message: Message):
        self.config["status"] = not self.config["status"]
        status = "enabled" if self.config["status"] else "disabled"
        await utils.answer(message, f"Module is now {status}.")
