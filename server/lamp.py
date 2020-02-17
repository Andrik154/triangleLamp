from __future__ import unicode_literals
# -*- coding: UTF-8 -*-

import json
import logging
from copy import copy

from flask import Flask, request

app=Flask(__name__)

if __name__=='__main__':
    app.run(debug=False, ssl_context=('../../etc/letsencrypt/live/andrik154.xyz/fullchain.pem','../../etc/letsencrypt/live/andrik154.xyz/privkey.pem'),threaded=True)

logging.basicConfig(level=logging.DEBUG)
### vars ###
colors={
    'красный':0xe31902,
    'красную':0xe31902,
    'красное':0xe31902,
    'рыжий':0xfc7703,
    'рыжую':0xfc7703,
    'рыжее':0xfc7703,
    'оражевый':0xfc7703,
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

lampMessage={
    "id":"01",
    "effect":"None",
    "color":0xFFFFFF,
    "brightness":"None"
}
brightness=0.7
suggests = [{
            "title": "Включи красный свет",
            "hide":True
},
            {
                "title": "Включи радугу",
                "hide":True
            },
            {
                "title": "Увеличь яркость",
                "hide":True
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

    if req['session']['new']:
        res['response']['text']='Добро пожаловать! Этот навык может управлять умной лампой Triangle. Вы можете: \n - Включать и выключать лампу \n - Включать эффекты (доступно: радуга) \n - Изменять цвет и яркость.'
        res['response']['buttons']=suggests
        return
    
    ou=req['request']['original_utterance'].lower()
    messageId=(req['session']['session_id']+'_'+str(req['session']['message_id']))
    c=False
    if ('помощь' in ou) or ('что ты умеешь' in ou):
        res['response']['text']='Этот навык может управлять умной лампой Triangle. Вы можете: \n - Включать и выключать лампу ("Включи/выключи лампу") \n - Включать эффекты ("Включи радугу") \n - Изменять цвет и яркость ("Включи синий свет", "Увеличь яркость") \n Приятного использования!'
        res['response']['buttons']=suggests
        return
    if 'включи' in ou:
        if ('переливание' in ou) or ('радугу' in ou) or ('радуга' in ou):
            lampMessage['effect']='rainbow'
            res['response']['text']='Включаю радугу 🌈'
            res['response']['tts']='Включаю радугу'
            turnOn(False, messageId, 'rainbow')
            return
        for i in ['лампу',
            'свет',
            'освещение',
            'подсветку']:
            if i in ou:
                for color in colors.keys():
                    if color in ou:
                        c=colors[color]
                        turnOn(c, messageId,False)
                        res['response']['text']=f'Включаю {color} {i} 😉'
                        res['response']['tts']=f'Включаю {color} {i}!'
                        return
                turnOn(c,messageId,False)
                res['response']['text']=f'Включаю {i} 😉'
                res['response']['tts']=f'Включаю {i}!'
                return 
        for color in colors.keys():
            if color in ou:
                c=colors[color]
                turnOn(c, messageId,False)
                res['response']['text']=f'Включаю 😉'
                res['response']['tts']=f'Включаю'
                return
        res['response']['text']='Я не очень вас поняла. Может, попробуем еще раз?'
        res['response']['tts']='Я не очень вас поняла. Может, попробуем еще раз?'
        res['response']['buttons']=suggests
        return
    if any(i in ou for i in ('выключи','выключай','отключи','отключай','выруби','вырубай')):
        c=0x000000
        turnOn(c,messageId,False)
        res['response']['text']=f'Выключаю лампу'
        res['response']['tts']=f'Выключаю лампу'
        return


    #u mean up, d mean down
    if 'яркость' in ou:
        if any(i in ou for i in ('повысь','увеличь','добавь')):
            res['response']['text']='Увеличиваю яркость'
            res['response']['tts']='Увеличиваю яркость'

            turnOn(c,messageId,False,brightness='u')
            return
        if any(i in ou for i in ('понизь','уменьши','убавь')):
            res['response']['text']='Уменьшаю яркость'
            res['response']['tts']='Уменьшаю яркость'
            turnOn(c,messageId,False,brightness='d')
            return

    if 'спасибо' in ou:
        res['response']['text']='Вам спасибо <3'
        res['response']['tts']='Вам спасибо'
        return
    
    res['response']['text']='Я не очень вас поняла. Может, попробуем еще раз?'
    res['response']['tts']='Я не очень вас поняла. Может, попробуем еще раз?'
    res['response']['buttons']=suggests
    return


def turnOn(c,messageId,effect,**args):
    lampMessage['id']=messageId
    lampMessage['brightness']="None"
    lampMessage['effect']="None"
    lampMessage['color']=c
    if brightness=='u' or brightness=='d':
        if brightness=='u':
            lampMessage['brightness']="u"
        if brightness=='d':
            lampMessage['brightness']="d"
        return
    if (effect !="None"):
        lampMessage['effect']='rainbow'
        return
        
    lampMessage['color']=c
    return

