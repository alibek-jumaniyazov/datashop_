from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot, Update
from telegram.ext import Filters, MessageHandler, CallbackContext, Updater
from telegram.utils.request import Request



def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:

            error_message = f"Xatoliq yuzaga keldi: {e}"
            print(error_message)
            raise e

    return inner


@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    reply_text = "Sizning ID = {}\n\n{}".format(chat_id, text)
    update.message.reply_text(
        text=reply_text,
    )
    

class Command(BaseCommand):

    help = 'Telegram bot'

    def handle(self, *args, **kwargs):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.BOT_TOKEN,
        )

        # bot.send_message(text="Hello BOT!", chat_id=settings.BOT_CHAT_ID)
        print(bot.get_me())

        updater = Updater(
            bot=bot,
            use_context=True,
        )

        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)

        updater.start_polling()
        updater.idle()



