__version__ = (1, 3, 2)
# meta developer: @werpyock0
from hikka import loader, utils
import asyncio
import shlex

class WSpamMod(loader.Module):
    """Гибкий спам-модуль."""

    strings = {
        "name": "WSpamMod",
        "no_args": "❌ Пожалуйста, укажите текст для спама.",
        "invalid_count": "❌ Некорректное количество сообщений.",
        "invalid_delay": "❌ Некорректная задержка.",
        "spamming": "✅ Начинаю спам...",
        "stopped": "🛑 Все спам-задачи остановлены.",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "DEFAULT_TEXT", "Привет, мир!", "Текст по умолчанию для спама",
            "DEFAULT_COUNT", 10, "Количество сообщений по умолчанию",
            "DEFAULT_DELAY", 1.0, "Задержка между сообщениями по умолчанию (в секундах)",
            "SPAM_ANNOUNCE_MODE", 0, "Режим уведомлений о спаме:\n"
                                     "-1 — не изменять сообщение с командой и не показывать сообщение\n"
                                     "0 — не изменять сообщение с командой\n"
                                     "1 — удалять сообщение о начале спама\n"
                                     "2 — показывать сообщение о начале спама"
        )
        self.spam_tasks = set()

    async def spamcmd(self, message):
        """Запуск спама. Использование: .spam "текст" [кол-во сообщений] [задержка]"""
        await self._start_spam(message, delete_after_send=False)

    async def dspamcmd(self, message):
        """Запуск спама с удалением сообщений. Использование: .dspam "текст" [кол-во сообщений] [задержка]"""
        await self._start_spam(message, delete_after_send=True)

    async def _start_spam(self, message, delete_after_send):
        args = utils.get_args_raw(message)
        if not args:
            text, count, delay = self.config["DEFAULT_TEXT"], self.config["DEFAULT_COUNT"], self.config["DEFAULT_DELAY"]
        else:
            try:
                parsed_args = shlex.split(args)
            except ValueError:
                return await message.edit(self.strings["no_args"])
            text = parsed_args[0] if len(parsed_args) > 0 else self.config["DEFAULT_TEXT"]
            try:
                count = int(parsed_args[1]) if len(parsed_args) > 1 else self.config["DEFAULT_COUNT"]
                if count <= 0:
                    raise ValueError
            except ValueError:
                return await message.edit(self.strings["invalid_count"])
            try:
                delay = float(parsed_args[2]) if len(parsed_args) > 2 else self.config["DEFAULT_DELAY"]
                if delay < 0:
                    raise ValueError
            except ValueError:
                return await message.edit(self.strings["invalid_delay"])

        announce_mode = self.config["SPAM_ANNOUNCE_MODE"]
        if announce_mode == 2:
            await message.edit(self.strings["spamming"])
        elif announce_mode == 1:
            await message.delete()
        elif announce_mode == -1:
            pass

        async def spam_task():
            for _ in range(count):
                sent_message = await message.respond(text)
                if delete_after_send:
                    await sent_message.delete()
                await asyncio.sleep(delay)

        task = asyncio.create_task(spam_task())
        self.spam_tasks.add(task)
        task.add_done_callback(self.spam_tasks.discard)

    async def stopspamcmd(self, message):
        """Останавливает все активные задачи .spam"""
        await self._stop_spam(message)

    async def stopdspamcmd(self, message):
        """Останавливает все активные задачи .dspam"""
        await self._stop_spam(message)

    async def _stop_spam(self, message):
        for task in self.spam_tasks:
            task.cancel()
        self.spam_tasks.clear()
        await message.edit(self.strings["stopped"])
