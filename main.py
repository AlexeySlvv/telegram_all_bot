import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

import logging
logging.basicConfig(level=logging.INFO)  


# token
try:
    with open(".token", 'r') as t_f:
        # Bot token can be obtained via https://t.me/BotFather
        TOKEN = t_f.read()
        # All handlers should be attached to the Router (or Dispatcher)
        router = Router()
        # Initialize Bot instance with a default parse mode which will be passed to all API␣calls
        bot = Bot(TOKEN, parse_mode="HTML")
except Exception as e:
    logging.error(f"Token file error: {str(e)}")
    exit()


# users
try:
    with open(".users", 'r') as u_f:
        users_list = u_f.read().split('\n')
except Exception as e:
    logging.error(f"Users file error: {str(e)}")
    exit()


# admins
try:
    with open(".admins", 'r') as a_f:
        admins_list = a_f.read().split('\n')
except Exception as e:
    logging.error(f"Admins file error: {str(e)}")
    exit()


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    await message.answer(f"Привет всем в этом чате! )")


@router.message(Command(commands=["all"]))
async def command_all_handler(msg: Message):
    """
    This handler receive messages with `/all` command
    """
    username = f"@{msg.from_user.username}"
    if msg.text.startswith("/all") and username in admins_list:
        user_list = ' '.join(users_list)
        user_fullname = msg.from_user.full_name
        text = f"{user_list} Сообщение от <b>{user_fullname}</b>: "
        text += msg.text[len("/all"):].strip()
        await msg.answer(text)
        try:
            # проверка прав и удаление исходного сообщения
            member = await bot.get_chat_member(msg.chat.id, bot.id)
            for perm, val in member:
                if perm == "can_delete_messages":
                    if val:
                        await msg.chat.delete_message(msg.message_id)
                    break
        except TelegramBadRequest:
            logging.info("Bot needs chat admin permissions")


async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()

    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)
    
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())