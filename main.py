import sys, logging, sys, io, os
sys.path.append("tools")
from tools import *
from os import getenv
from pydub import AudioSegment
from aiohttp import web
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import F
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.types import FSInputFile

# All handlers should be attached to the Router (or Dispatcher)
router = Router()
bot = Bot(wconfig.TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)

async def on_startup(bot: Bot) -> None:
    # If you have a self-signed SSL certificate, then you will need to send a public
    # certificate to Telegram
    await bot.set_webhook(f"{wconfig.BASE_WEBHOOK_URL}{wconfig.WEBHOOK_PATH}", secret_token="")

def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Register startup hook to initialize webhook
    dp.startup.register(on_startup)

    # Create aiohttp.web.Application instance
    app = web.Application()

    # Create an instance of request handler,
    # aiogram has few implementations for different cases of usage
    # In this example we use SimpleRequestHandler which is designed to handle simple cases
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token="",
    )
    # Register webhook handler on application
    webhook_requests_handler.register(app, path=wconfig.WEBHOOK_PATH)

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)

    # And finally start webserver
    web.run_app(app, host=wconfig.WEBHOOK_HOST, port=wconfig.WEBHOOK_PORT)



async def cmd_donna_dimmi(message, mode, input):
    try:
        input = ((await wstools.clear_p(input)).lower()).replace("donna dimmi", "")
        output = await waitools.response(
                input,
                "Rispondi a questa domanda iniziando con Signor Zucchiatti e dandomi del lei. La domanda è: ",
            )
        await waitools.tts(message, output)
        uploadedfile = FSInputFile(f"voice_outputs/{message.message_id}.ogg")
        await bot.send_voice(message.chat.id, uploadedfile)
        os.remove(f"voice_outputs/{message.message_id}.ogg")
    except Exception as e:
        print("Exception in command donna dimmi: " + str(e))


# Donna ricordami di command
async def cmd_donna_ricordami(message, mode, input):
    try:
        input = ((await wstools.clear_p(input)).lower()).replace("donna dimmi", "")
        output = await waitools.response(
                input,
                "Rispondi a questa domanda iniziando con Signor Zucchiatti e dandomi del lei. La domanda è: ",
            )
        await bot.send_voice(message.chat_id, waitools.tts(message, output))
    except Exception as e:
        print("Exception in command donna ricordami: " + str(e))


# Donna riassumimi command
async def cmd_donna_riassumimi(message, mode, input):
    try:
        input = ((await wstools.clear_p(input)).lower()).replace("donna dimmi", "")
        await message.answer(
            ""+await waitools.response(
                input,
                "Rispondi a questa domanda iniziando con Signor Zucchiatti e dandomi del lei. La domanda è: ",
            )
        )
    except Exception as e:
        print("Exception in command donna riassumi: " + str(e))


# Donna salva nelle note command
async def cmd_donna_salva_note(message, mode, input):
    try:
        input = ((await wstools.clear_p(input)).lower()).replace("donna dimmi", "")
        await message.answer(
            ""+await waitools.response(
                input,
                "Rispondi a questa domanda iniziando con Signor Zucchiatti e dandomi del lei. La domanda è: ",
            )
        )
    except Exception as e:
        print("Exception in command donna salva nelle note: " + str(e))


# Get command from input and execute it
async def get_command(input, message, mode):
    try:
        clean_input = await wstools.clear_p(input)
        clean_input = clean_input.lower()
        if "donna dimmi" in clean_input:
            await cmd_donna_dimmi(message, mode, input)
        elif "donna ricordami di" in clean_input:
            await cmd_donna_ricordami(message, mode, input)
        elif "donna riassumimi" in clean_input:
            await cmd_donna_riassumimi(message, mode, input)
        elif "donna salva nelle note" in clean_input:
            await cmd_donna_salva_note(message, mode, input)
        else:
            await message.answer("Error, command not recognized")
            return
    except Exception as e:
        print("Exception in command detection: " + str(e))

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

@router.message(F.voice)
async def echo_handler(message: types.Message) -> None:
    try:
        file = await bot.get_file(message.voice.file_id)
        file_path = file.file_path
        ogg_data = await bot.download_file(file_path)
        ogg_buffer = io.BytesIO(ogg_data.getvalue())
        
        # Convert it to .wav using pydub
        audio = AudioSegment.from_ogg(ogg_buffer)
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format="wav")
        
        # Reset the buffer position before reading from it
        wav_buffer.seek(0)
        
        # Save the .wav file from memory to disk
        output_path = f"voice_messages/{message.voice.file_id}.wav"
        with open(output_path, "wb") as wav_file:
            wav_file.write(wav_buffer.read())
        output = await waitools.transcribe(output_path)
        os.remove(output_path)
        await get_command(output, message, "voice")
    except Exception as e:
        # But not all the types is supported to be copied so need to handle it
        print("Error while handling voice message!"+str(e))

@router.message(F.text)
async def echo_handler(message: types.Message) -> None:
    try:
        await get_command(message.text, message, "text")
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        print("\nError while handling text message!"+str(e))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()


