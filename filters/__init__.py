from aiogram import Dispatcher

from loader import dp
from .is_admin import AdminFilter
from .group import IsGroup
from .private import IsPrivate

from .is_admin import IsAdmin
from .is_user import IsUser


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin, event_handlers=[dp.message_handlers])
    dp.filters_factory.bind(IsUser, event_handlers=[dp.message_handlers])


if __name__ == "filters":
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsAdmin, event_handlers=[dp.message_handlers])
    dp.filters_factory.bind(IsUser, event_handlers=[dp.message_handlers])
