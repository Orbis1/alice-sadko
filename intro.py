from fun import make_only_response, button
from math import sin, cos, sqrt, atan2, radians
from sights import sights
import phrases as ph
from resource import quest_order

def bye(txt='Скоро сказка сказывается, да не скоро дело делается. Возвращайся! Я и Садко будем ждать тебя'):
  return make_only_response(
    text=txt,
    end_session=True
  )

def end_game(gift):
  txt='И тут как ниоткуда появился ларец перед Садко. Открыл садко ларец, а там - {}. Вот и сказочки конец, а кто слушал - молодец.'.format(gift)
  tts='<speaker audio="dialogs-upload/ca5036ee-1029-4a07-960c-8cf27f1258a3/107591dc-b7d4-462b-8ccd-0ad938ad796a.opus">' + 'И тут как ниоткуда появился ларец перед Садко. Открыл садко ларец, а там sil <[200]> {}. Вот и сказочки конец, а кто слушал - молодец.'.format(gift) + '<speaker audio="dialogs-upload/ca5036ee-1029-4a07-960c-8cf27f1258a3/2fdf95a6-bcbf-4419-945d-31337770b577.opus">'
  return make_only_response(
    text=txt,
    tts=tts,
    end_session=True
  )

def welcome(state, appStateClear=False, appState=False):
    state['context'] = 'welcome'
    state['spravka']=None
    if appStateClear:
      for key in appState:
        appState[key]='null'
      state['geo_asked']=False
      state['spravka']=None
    return make_only_response(
    text=ph.hi['txt'],
    tts=ph.hi['tts'],
    buttons=ph.hi['buttons']
  )

def say(txt="wawa"):
  return make_only_response(
    text=txt
  )

def say_help():
  txt=ph.help_['txt']
  tts=ph.help_['tts']
  return make_only_response(
    text=txt,
    tts=tts,
    buttons=[button('Продолжить', hide=True),]
  )

def ask_geo(state,card=None): #Карточка только для первого входа
    state['geo_asked'] = True; 
    state['context'] = 'ask_geo'
    if card is not None:
        return  make_only_response(    
            text = ph.needgeo_first['txt'],
            tts = ph.needgeo_first['tts'],
            card=ph.needgeo_first['card'],
            directives = True
        )
    else:
        return make_only_response(
        text = ph.needgeo['txt'],
        tts = ph.needgeo['tts'],
        directives = True,
  )
def continue_game(state):
  state['context'] = 'continue_game'
  state['spravka']=None 
  return make_only_response(
    text = 'У вас есть сохранённый прогресс. Продолжить?',
    buttons=ph.hi['buttons']
  )

def fallback(command):
  txt='Мне слова заморские почуделись: "{}". Не разумею, что нужно. Попробуй ещё по другому молвить али кликни помощь'.format(command)
  return make_only_response(
    text = txt,
  )

# with location
def how_far_from_kremlin(appState, sessionState, user_location):
   
    if user_location is not None and user_location['accuracy'] < 100:
        target = sights['kupol']
        distance = get_distance_to_object(user_location, target['location'])
        print('Расстояние до {name} составялет {distance}'.format(name=target['name'], distance=distance))
    
        if distance < 300:
            return within_kremlin(appState, sessionState) 
        elif 300 <= distance < 1000: 
            return around_kremlin(appState, sessionState)
        elif distance >= 1000:
            return somewhere(appState, sessionState)
    else:
      return somewhere(appState, sessionState)
      

def within_kremlin(appState, sessionState):
  txt = 'Вы находитесь на территории Новгородского Кремля. Рассказать про Кремль?'
  sessionState['context'] = 'within_kremlin'
  return make_only_response(
    text=txt,
    buttons=ph.hi['buttons']
  )

def around_kremlin(appState, sessionState):
  txt = 'Вы рядом с Новгородским Кремлём. Подойдите к Кремлёвским воротам и скажите "Я готов"'
  sessionState['context'] = 'around_kremlin'
  return make_only_response(
    text=txt,
    buttons=[{ 'title': "Я готов", 'hide': True }]
  )

def somewhere(appState, sessionState):
  txt = 'Далеко ты от кремля Новгородского. Далее продолжать буду в режиме повествования. Хорошо?'
  sessionState['context'] = 'somewhere'
  sessionState['story_mode'] = True
  appState['step'] = 0
  return make_only_response(
    text=txt,
    buttons=ph.hi['buttons']
  )

def get_distance_to_object(user_location, target_location):
  # approximate radius of earth in km
  R = 6373.0

  lat1 = radians(user_location['lat'])
  lon1 = radians(user_location['lon'])
  lat2 = radians(target_location['lat'])
  lon2 = radians(target_location['lon'])

  dlon = lon2 - lon1
  dlat = lat2 - lat1

  a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  c = 2 * atan2(sqrt(a), sqrt(1 - a))

  distance = R * c * 1000

  return distance

# def get_url_map(user_location, target_location):
#   lat1 = user_location['lat']
#   lon1 = user_location['lon']
#   lat2 = target_location['lat']
#   lon2 = target_location['lon']
#   url = 'https://yandex.ru/maps/?rtext={lat1},{lon1}~{lat2},{lon2}&rtt=mt'.format(lat1=lat1,)
#   return url

# story

def begin(state):
  txt = 'Жил был Сдако... Рассказать про купол?'
  state['context'] = 'begin'
  return make_only_response(
    text=txt,
    buttons=ph.hi['buttons']
  )

def kupol_story(state):
  txt = 'Купол этот не простой...Идём к Кащею?'
  state['context'] = 'kupol_story'
  return make_only_response(
    text=txt,
    buttons=ph.hi['buttons']
  )

def quest(appState, sessionState):
  sessionState['context'] = 'quest'
  appState['step'] = 0
  appState['place_seen'] = 'kupol'
  to_target = sights['kupol']['to_tip_name'] 
  txt = 'Покатился клубок к {}. Следуй за ним. Как дойдешь - скажи "Я на месте". А пока идём могу тебе про это место рассказать. Интересно?'.format(to_target)
  return make_only_response(
    text=txt,
    buttons=ph.quest['buttons']
  )




  
