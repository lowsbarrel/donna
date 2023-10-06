import openai, wconfig, os
import requests
from pydub import AudioSegment
from elevenlabslib import *

user = ElevenLabsUser(wconfig.ELEVENLABS_KEY)
voice = user.get_voice_by_ID("EXAVITQu4vr4xnSDxMaL")


openai.api_key = str(wconfig.OPENAI_KEY)


async def response(prompt, prefix):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prefix + prompt}],
            temperature=1.0,
        )
        return response.choices[0].message["content"]
    except Exception as e:
        print("Exception in transcribing voice: " + str(e))


async def transcribe(file):
    try:
        with open(file, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]
    except Exception as e:
        print("Exception in transcribing voice: " + str(e))

async def tts(message, textts):
    try:
        # Find correct language model
        multilingualModel = None
        for model in user.get_models():
            for language in model.supportedLanguages:
                if "en" not in language["language_id"]:
                    # Found a model that supports a non-english language
                    multilingualModel = model
                    break
        # Generate the audio
        generationData = voice.generate_audio_v2(
            textts, GenerationOptions(stability=0.4, model=multilingualModel)
        )
        # Save the audio as an .ogg file
        save_audio_bytes(
            generationData[0],
            f"voice_outputs/{message.message_id}.ogg",
            outputFormat="ogg",
        )
        tempresponse = f"voice_outputs/{message.message_id}.ogg"
        # Send the audio
        historyItem = user.get_history_item(generationData[1])
        historyItem.delete()
        # Clean up the temporary .ogg file
        return tempresponse
    except Exception as e:
        print("Exception in sending vocal response: " + str(e))
