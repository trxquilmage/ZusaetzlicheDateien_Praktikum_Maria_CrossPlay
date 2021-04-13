from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os, aiohttp, asyncio, json, socket, binascii

TCP_IP = '127.0.0.1'
TCP_PORT = 60600
BUFFER_SIZE = 1024
rasa_url = 'http://localhost:5005/webhooks/rest/webhook'

def sendToUnity(textToParse):
# send to unity server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    binarymsg = bytearray(textToParse[:BUFFER_SIZE],"utf8")
    s.send(binarymsg)
    # data = s.recv(BUFFER_SIZE) // dont comment back in, i dont remember what this was for, so i dont want to delete it
    s.close()

class ActionExampleClass(Action):
    def name(self) -> Text:
         return "action_example_class"
    def run(self, dispatcher, tracker:Tracker, domain:"DomainDict") -> List[Dict[Text, Any]]:
        message = "Das ist eine Beispiel-Nachricht, die an Unity gesendet wird"
        sendToUnity(message)
        return []

