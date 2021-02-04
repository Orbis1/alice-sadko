from fun import make_only_response
from math import sin, cos, sqrt, atan2, radians
from sights import sights
import phrases as ph

# developer
def clear_app_state(aState, sState):
  for key in aState:
    aState[key]='null'
  sState['context'] = 'clear_app_state'
  return make_only_response(
    text='appState clear',
  )


def bye():
  return make_only_response(
    text='Пока-пока',
    end_session=True
  )


def welcome(state):
  state['context'] = 'welcome'
  return make_only_response(
    text=ph.hi['txt'],
    buttons=ph.hi['buttons']
  )

def say(txt="wawa"):
  print(txt)
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
def how_far_from_kremlin(aState, sState, user_location):
  if user_location is not None and user_location['accuracy'] < 100:
      target = sights['one_k_year']
      distance = get_distance_to_object(user_location, target['location'])
      print('Расстояние до {name} составялет {distance}'.format(name=target['name'], distance=distance))
    
      if distance < 300:
        return within_kremlin(aState, sState) 
      if 300 <= distance < 500: 
        return around_kremlin(aState, sState)
      if distance > 500:
        return somewhere(aState, sState)
      

def within_kremlin(aState, sState):
  txt = 'Вы на территории Новгодоского Кремля. Рассказать про Кремль?'
  sState['context'] = 'within_kremlin'
  return make_only_response(
    text=txt,
    buttons=ph.hi['buttons']
  )

def around_kremlin(aState, sState):
  txt = 'Вы рядом с Новгородским Кремлём. Подойдите к Кремлёвским воротам и скажите "Я возле ворот"'
  sState['context'] = 'around_kremlin'
  return make_only_response(
    text=txt,
    buttons=[{ 'title': "Я возле ворот", 'hide': True }]
  )

def somewhere(aState, sState):
  txt = 'Вы очень далеко от Новгородского Кремля. Продолжить в режиме повествования?'
  sState['context'] = 'somewhere'
  sState['story_mode'] = True
  aState['step'] = 0
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

def one_k_year_story(state):
  txt = 'Купол этот не простой...Идём к Кащею?'
  state['context'] = 'one_k_year_story'
  return make_only_response(
    text=txt,
    buttons=ph.hi['buttons']
  )