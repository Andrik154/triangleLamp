#andrik154

from __future__ import unicode_literals
# -*- coding: UTF-8 -*-

import json
import logging
import random
from copy import copy

from flask import Flask, request

app=Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

### vars ###
colors={
    'красный':0xe31902,
    'красную':0xe31902,
    'красное':0xe31902,
    'рыжий':0xfc7703,
    'рыжую':0xfc7703,
    'рыжее':0xfc7703,
    'оранжевый':0xfc7703,
    'оранжевую':0xfc7703,
    'оранжевое':0xfc7703,
    'желтый':0xffb700,
    'желтую':0xffb700,
    'желтое':0xffb700,
    'жёлтый':0xffb700,
    'жёлтую':0xffb700,
    'жёлтое':0xffb700,
    'зеленый':0x43c91e,
    'зеленую':0x43c91e,
    'зеленое':0x43c91e,#fc7703 #0xffb700
    'зелёный':0x43c91e,
    'зёленую':0x43c91e,
    'зёленое':0x43c91e,
    'голубой':0x1cccd9,
    'голубую':0x1cccd9,
    'голубое':0x1cccd9,
    'синий':0x1520bf,
    'синюю':0x1520bf,
    'синее':0x1520bf,
    'розовый':0xfc038c,
    'розовую':0xfc038c,
    'розовое':0xfc038c,
    'фиолетовый':0x8300c4,
    'фиолетовую':0x8300c4,
    'фиолетовое':0x8300c4,
    'бирюзовый':0x00bdc4,
    'бирюзовую':0x00bdc4,
    'бирюзовое':0x00bdc4,
    'белый':0xFFFFFF,
    'белую':0xFFFFFF,
    'белое':0xFFFFFF,
}

step=20
maxBrightness=200
minBrightness=20
defaultBrightness=100
brightness=copy(defaultBrightness)

lampMessage={
    "id":"01",
    "effect":"None",
    "color":0xFFFFFF,
    "brightness":100
}

suggests = [{
            "title": "Включи красный свет",
            "hide":True
            },
            {
                "title": "Включи радугу 🌈",
                "hide":True
            },
            {
                "title": "Увеличь яркость",
                "hide":True
            },
            {
                "title": "Включи голубую подсветку",
                "hide": True
            },
            {
                "title": "А включи фиолетовый",
                "hide": True
            },
            {   "title":"Выключи лампу",
                "hide": True
            },
            {
                "title": "Понизь яркость",
                "hide": True
            },
            {
                "title": "Я хочу включить синий",
                "hide": True
            }
]



##############
### routes ###
@app.route('/req',methods=['POST'])
def get():
    response = {
        "version":request.json['version'],
        "session":request.json['session'],
        "response":{
            "buttons":[],
            "end_session": False
        }
    }

    handler(request.json, response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

@app.route('/lampreq')
def send():
    response=copy(lampMessage)
    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


################
### handlers ###
def handler(req,res):
    global brightness
    global maxBrightness
    global minBrightness
    global defaultBrightness
    global step
    #Shuffle suggests
    random.shuffle(suggests)
    ou=req['request']['original_utterance'].lower()
    res['response']['buttons']=suggests[:3]
    #if new session = greeting
    if req['session']['new'] and not (('включи' or 'поставь') in ou):
        res['response']['text']='Добро пожаловать! Этот навык может управлять умной лампой Triangle. Вы можете: \n - Включать и выключать лампу \n - Включать эффекты (доступно: радуга, переливание) \n - Изменять цвет и яркость.'
        res['response']['buttons']=suggests[:3]
        return

    #if session already started = handling
    #brightness=lampMessage["brightness"]
    #ou=req['request']['original_utterance'].lower()
    messageId=(req['session']['session_id']+'_'+str(req['session']['message_id']))
    c=lampMessage['color']
    if ('помощь' in ou) or ('что ты умеешь' in ou):
        res['response']['text']='Этот навык может управлять умной лампой Triangle. Вы можете: \n - Включать и выключать лампу ("Включи/выключи лампу") \n - Включать эффекты ("Включи радугу") \n - Изменять цвет и яркость ("Включи синий свет", "Увеличь яркость") \n Приятного использования!'
        res['response']['buttons']=suggests[:3]
        return
    if ('переливание' in ou):
        #lampMessage['effect']='fusion'
        res['response']['text']='Запускаю переливание!'
        res['response']['tts']='Запускаю переливание!'
        turnOn(c,messageId,'fusion',brightness)
        return
    if ('включи' in ou) and not ('яркость' in ou):
        if ('радугу' in ou) or ('радуга' in ou):
            #lampMessage['effect']='rainbow'
            res['response']['text']='Включаю радугу 🌈'
            res['response']['tts']='Включаю радугу'
            turnOn(c, messageId, "rainbow",brightness)
            return
        for i in ['лампу',
            'подсветку',
            'освещение',
            'свет']:
            if i in ou:
                for color in colors.keys():
                    if color in ou:
                        c=colors[color]
                        res['response']['text']=f'Включаю {color} {i} 😉'
                        res['response']['tts']=f'Включаю {color} {i}!'
                        turnOn(c, messageId,"std",brightness)
                        return
                res['response']['text']=f'Включаю {i} 😉'
                res['response']['tts']=f'Включаю {i}!'
                turnOn(c,messageId, lampMessage['effect'], brightness)
                return
        for color in colors.keys():
            if color in ou:
                c=colors[color]
                res['response']['text']=f'Включаю {color} 😉'
                res['response']['tts']=f'Включаю {color}'
                turnOn(c, messageId,"std",brightness)
                return

        #if no entries after detecting "включи"
        res['response']['text']='Я не очень вас поняла. Может, попробуем еще раз?'
        res['response']['tts']='Я не очень вас поняла. Может, попробуем еще раз?'
        res['response']['buttons']=suggests
        return   
    if any(i in ou for i in ('выключи','выключай','отключи','отключай','выруби','вырубай')):
        c=lampMessage['color']
        turnOn(c,messageId,lampMessage['effect'],0)
        res['response']['text']=f'Выключаю лампу'
        res['response']['tts']=f'Выключаю лампу'
        return


    #Brightness things
    if 'яркость' in ou:

        #Increase brightness
        if any(i in ou for i in ('повысь','увеличь','добавь')):
            if brightness+step>maxBrightness:
                res['response']['text']='Уже достигнут максимальный уровень яркости'
                res['response']['tts']='Уже достигнут максимальный уровень яркости'
                brightness+=0
            else:
                res['response']['text']='Увеличиваю яркость'
                res['response']['tts']='Увеличиваю яркость'
                brightness+=step

            turnOn(c,messageId,lampMessage["effect"],brightness)
            return

        #Decrease brightness
        if any(i in ou for i in ('понизь','уменьши','убавь')):
            if brightness-step<minBrightness:
                res['response']['text']='Мы достигли минимальной яркости'
                res['response']['tts']='Мы достигли минимальной яркости'
                brightness-=0
            else:
                res['response']['text']='Уменьшаю яркость'
                res['response']['tts']='Уменьшаю яркость'
                brightness-=step

            turnOn(c,messageId,lampMessage["effect"],brightness)
            return
        if any(i in ou for i in('процентов', 'процент', '%')):
            for i in req['request']['nlu']['entities']:
                if i['type']=='YANDEX.NUMBER':
                    n=int(i['value'])
                    brightness=int(((n/100)*maxBrightness))
                    res['response']['text']='Яркость на '+str(n)+' процентов'
                    res['response']['tts']='Яркость на '+str(n)+' процентов'
                    turnOn(c,messageId,lampMessage["effect"],brightness)
                    return

    #thanksgiving
    if 'спасибо' in ou:
        res['response']['text']='Вам спасибо <3'
        res['response']['tts']='Вам спасибо'
        return

    #if no entries occured
    res['response']['text']='Я не очень вас поняла. Может, попробуем еще раз?'
    res['response']['tts']='Я не очень вас поняла. Может, попробуем еще раз?'
    res['response']['buttons']=suggests
    return


#Setting all the data
def turnOn(c,messageId,effect,brightness):
    lampMessage['id']=messageId
    lampMessage['brightness']=brightness
    lampMessage['effect']=effect
    lampMessage['color']=c
    return

#Starting prorgam
if __name__=='__main__':
    app.run(debug=False, ssl_context=('../../etc/letsencrypt/live/andrik154.xyz/fullchain.pem','../../etc/letsencrypt/live/andrik154.xyz/privkey.pem'),host='andrik154.xyz')
