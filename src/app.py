import json
import datetime
from enum import Enum
import telegram
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from flask import Flask, request
app = Flask(__name__)

class Severity(Enum):
    Critical = 'Critical'

def lanorduan():
    now = datetime.datetime.now()
    return now.weekday() in [0,1,2,3,4] and now.hour in range(9,17)

@app.route('/', methods=['POST'])
def notifikazioa():
    data = json.loads(request.data)
    severity = data.get('ALERT_SEVERITY')
    if severity ==  Severity.Critical.name or lanorduan():
        mezua = f"""ALARMA!!! 
                Gailua: {data.get('DEVICE')}
                Metrikak: {data.get('METRICS')}
                Xehetasunak: {data.get('ALERT_URL')}
                """
        bot = telegram.Bot(os.environ.get("TELEGRAM_TOKEN"))
        bot.sendMessage(
            chat_id=os.environ.get("TELEGRAM_CHATID"),
            text=mezua
        )       
    return "", 204
 
app.run(host='0.0.0.0')

