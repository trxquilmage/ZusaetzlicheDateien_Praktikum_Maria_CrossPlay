#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import os
import aiohttp
import asyncio
import json
import socket
import binascii

rasa_url = 'http://localhost:5005/webhooks/rest/webhook' 
if not os.path.exists("model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

import pyaudio

model = Model("model")
rec = KaldiRecognizer(model, 16000)

#sends the Input to Rasa
async def sendToRasa(textToParse):

    async with aiohttp.ClientSession() as session:
        async with session.post(rasa_url, json={'sender':'user','message':textToParse}) as response:
            html = await response.text()
            print("Body:", html, "...")
            

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

while True:
    data = stream.read(10000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        resultText = json.loads(rec.Result())['text']

        #remove umlaute because rasa doesnt like them 
        resultText = resultText.replace("ä","ae")
        resultText = resultText.replace("ö","oe")
        resultText = resultText.replace("ü","ue")
        resultText = resultText.replace("ß","ss")
        
        print("Vosk says: ",resultText)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(sendToRasa(resultText))
    #else:
        #print(rec.PartialResult())

print(rec.FinalResult())

