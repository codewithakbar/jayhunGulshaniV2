from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from data.config import ADMINS


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        member = await message.chat.get_member(message.from_user.id)
        return member.is_chat_admin()


class IsAdmin(BoundFilter):

    async def check(self, message: Message):
        return message.from_user.id in ADMINS
