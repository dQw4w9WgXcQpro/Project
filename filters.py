from aiogram.types import Message
import config

class IsOwnerFilter:
    def __call__(self, message: Message) -> bool:
        return message.from_user.id == config.BOT_OWNER

class IsAdminFilter:
    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def __call__(self, message: Message) -> bool:
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return (member.is_chat_admin() or member.is_chat_creator()) == self.is_admin

class MemberCanRestrictFilter:
    def __init__(self, member_can_restrict: bool):
        self.member_can_restrict = member_can_restrict

    async def __call__(self, message: Message) -> bool:
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return (member.is_chat_creator() or getattr(member, "can_restrict_members", False)) == self.member_can_restrict
