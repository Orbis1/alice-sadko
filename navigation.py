from fun import make_only_response
from math import sin, cos, sqrt, atan2, radians
from sights import sights
import phrases as ph

def bye():
  return make_only_response(
    text='Пока-пока',
    end_session=True
  )

def welcome(state, appStateClear=False, appState=False):
  state['context'] = 'welcome'
  if appStateClear:
    for key in appState:
      appState[key]='null'
  return make_only_response(
    text=ph.hi['txt'],
    buttons=ph.hi['buttons']
  )

def say(txt="wawa"):
  return make_only_response(
    text=txt
  )

def say_help():
  txt=ph.help_['txt']
  return make_only_response(
    text=txt
  )

def ask_geo(state):
  state['geo_asked'] = True; 
  state['context'] = 'ask_geo'; 
  return make_only_response(
    text = ph.needgeo['txt'],
    tts = ph.needgeo['tts'],
    directives = True,
  )

def continue_game(state):
  state['context'] = 'continue_game'; 
  return make_only_response(
    text = 'У вас есть сохранённый прогресс. Продолжить?',
    buttons=ph.hi['buttons']
  )

def fallback(command):
  txt='Вы молвили {}. Команда не распознана. Поробуйте ещё раз'.format(command)
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
      if 300 <= distance < 500: 
        return around_kremlin(appState, sessionState)
      if distance > 500:
        return somewhere(appState, sessionState)
      

def within_kremlin(appState, sessionState):
  txt = 'Вы на территории Новгодоского Кремля. Рассказать про Кремль?'
  sessionState['context'] = 'within_kremlin'
  return make_only_response(
    text=txt,
    buttons=ph.hi['buttons']
  )

def around_kremlin(appState, sessionState):
  txt = 'Вы рядом с Новгородским Кремлём. Подойдите к Кремлёвским воротам и скажите "Я возле ворот"'
  sessionState['context'] = 'around_kremlin'
  return make_only_response(
    text=txt,
    buttons=[{ 'title': "Я возле ворот", 'hide': True }]
  )

def somewhere(appState, sessionState):
  txt = 'Вы очень далеко от Новгородского Кремля. Продолжить в режиме повествования?'
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

def quest_begin(appState, sessionState):
  sessionState['context'] = 'quest_begin'
  appState['step'] = 0
  appState['place'] = 'kupol'
  to_target = sights['kupol']['to_tip_name'] 
  txt = 'Покатился клубок к {}. Следуй за ним. Как дойдешь - скажи "Я на месте". А пока идём могу тебе про это место рассказать. Интересно?'.format(to_target)
  return make_only_response(
    text=txt,
    buttons=ph.quest['buttons']
  )

def quest_(appState, sessionState):
  sessionState['context'] = 'quest_begin'
  step = appState['step']
  appState['target'] = 'kupol'
  to_target = sights['kupol']['to_tip_name'] 
  txt = 'Покатился клубок к {}. Следуй за ним. Как дойдешь - скажи "Я на месте". А пока идём могу тебе про это место рассказать. Интересно?'.format(to_target)
  return make_only_response(
    text=txt,
    buttons=ph.quest['buttons']
  )



  