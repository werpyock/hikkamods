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
__version__ = (1, 0, 0)
# meta developer: @terrasa120
from hikkatl.types import Message
from .. import loader, utils

@loader.tds
class DSendMod(loader.Module):
    """Отправляет и удаляет, хз."""
    strings = {"name": "DSend"}
    @loader.command(ru_doc="Отправить и удалить")
    async def dsend(self, m: Message):
        args = utils.get_args_raw(m)
        if not args:
            await m.edit("❌Укажи текст.")
            return
        send = await m.client.send_message(m.chat_id, args)
        await m.delete()
        await send.delete()
