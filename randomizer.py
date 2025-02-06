__version__ = (1, 0, 2)
# meta developer: @werpyock0
from .. import loader, utils
import random

@loader.tds
class RandomNumberGeneratorMod(loader.Module):
    """Модуль для генерации случайного числа"""
    strings = {"name": "RandomizerMod"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "min_value", None, lambda: "Минимальное значение диапазона",
            "max_value", None, lambda: "Максимальное значение диапазона"
        )

    async def rndcmd(self, message):
        """Генерирует случайное число. Использование: .rnd <минимальное число> <максимальное число> (если не будет аргументов буду использовать значения из конфига)"""
        args = utils.get_args(message)

        if len(args) == 2:
            try:
                min_value = int(args[0])
                max_value = int(args[1])
            except ValueError:
                await message.edit("🚫Пожалуйста, введите два целых числа.")
                return
        else:
            min_value = self.config["min_value"]
            max_value = self.config["max_value"]

        if min_value is None or max_value is None:
            await message.edit("🚫Необходимо указать диапазон чисел в аргументах команды или в конфигурации модуля.")
            return

        if min_value > max_value:
            await message.edit("🚫Минимальное значение не может быть больше максимального.")
            return

        random_number = random.randint(min_value, max_value)
        await message.edit(f"✅Случайное число между <code>{min_value}</code> и <code>{max_value}</code>: <code>{random_number}</code>")
