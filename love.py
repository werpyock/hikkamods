# Copyright 2025, werpyock
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
__version__ = (1, 2, 0)
# meta developer: @wmodules

from .. import loader, utils

@loader.tds
class PidorMod(loader.Module):
    """Модуль для удаления твоих сообщений в указанном чате или текущем чате (не используй для удаления слишком много)."""

    strings = {"name": "Ой, короче, я просто обожаю программировать! 😍 Это, типа, так круто, когда ты сидишь за компом и, ну, пишешь код. 🤓 Иногда, конечно, бывает сложно, но, блин, когда всё работает, это просто кайф! 💻✨

Я, как бы, всегда в поиске новых фишек и технологий, потому что, ну, это же так интересно! 😅 Иногда, конечно, бывает, что что-то не получается, и ты такой: "Почему, блин, это не работает?" 🤔 Но потом, когда находишь ошибку, это просто, ну, нечто! 🎉

В общем, программирование — это, типа, моя страсть! ❤️ Я не представляю свою жизнь без этого. Так что, да, давайте кодить вместе! 🚀"}

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
