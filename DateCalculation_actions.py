# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
import datetime
import pytz 

# abgabedatum muss bis jetzt jedes Jahr neu manuell eingetragen werden
abgabedatum = {
            'year' : 2021,
            'month' : 6,
            'day' : 15
        }
# sucht sich das heutige Datum
currDate = datetime.datetime.now(pytz.timezone('CET'))
currentDate = {
            'year' : currDate.year,
            'month' : currDate.month,
            'day' : currDate.day
        }
# speichert die Länge aller Monate in einer Liste (0 = 0, damit die Indexe stimmen)
monthLengths =  [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

class ActionGetDate(Action):

    def name(self) -> Text:
        return "action_get_date"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        txt = "Der Abgabetermin ist dieses Jahr am " + str(abgabedatum['day']) + "." + str(abgabedatum['month']) + "." + str(abgabedatum['year']) + ". Heute ist in Berlin der "
        txt = txt + str(currentDate['day']) + "." + str(currentDate['month']) + "." + str(currentDate['year']) + ". "

        # wenn dieses Jahr das Abgabedatum schon vorbei ist
        if currentDate['day'] > abgabedatum['day'] and currentDate['month'] > abgabedatum['month'] or currentDate['month'] > abgabedatum['month'] or currentDate['year'] > abgabedatum['year']:
            txt = txt + "Das heißt, dass der diesjährige Abgabetermin bereits verstrichen ist. Das neue Thema wird im Februar angekündigt und die nächste Abgabe findet voraussichtlich im Juni " + str(abgabedatum['year']+1) + " statt."
        
        # wenn dieses Jahr das Abgabedatum noch nicht vorbei ist:
        else:
            daysLeft = monthLengths[currentDate['month']] - currentDate['day'] # the days left this month
            month = currentDate['month'] + 1
            while month != abgabedatum['month']: # the days left in every full month until the deadline
                print(str(month))
                daysLeft = daysLeft + monthLengths[month]
                month = month + 1
            daysLeft = daysLeft + abgabedatum['day'] # the days left in june
            txt = txt + "Das heißt es bleiben noch " + str(daysLeft) + " Tag(e) bis zur Abgabe."
        dispatcher.utter_message(txt)
        return []

