from fun import make_only_response
from math import sin, cos, sqrt, atan2, radians
from sights import sights
import phrases as ph

# developer
# def clear_user_state(state):
  


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

def fallback(command):
  txt='Вы молвили {}. Команда не распознана. Поробуйте ещё раз'.format(command)
  return make_only_response(
    text = txt,
  )

# with location
def how_far_from_kremlin(state, user_location):
  if user_location is not None and user_location['accuracy'] < 100:
      target = sights['one_k_year']
      distance = get_distance_to_object(user_location, target['location'])
      print('Расстояние до {name} составялет {distance}'.format(name=target['name'], distance=distance))
    
      if distance < 300:
        return within_kremlin(state) 
      if 300 <= distance < 500: 
        return around_kremlin(state)
      if distance > 500:
        return somewhere(state)
      

def within_kremlin(state):
  txt = 'Вы на территории Новгодоского Кремля. Рассказать про Кремль?'
  state['context'] = 'within_kremlin'
  return make_only_response(
    text=txt,
    buttons=ph.hi['buttons']
  )

def around_kremlin(state):
  txt = 'Вы рядом с Новгородским Кремлём. Подойдите к Кремлёвским воротам и скажите "Я возле ворот"'
  state['context'] = 'around_kremlin'
  return make_only_response(
    text=txt,
    buttons=[{ 'title': "Я возле ворот", 'hide': True }]
  )

def somewhere(state):
  txt = 'Вы очень далеко от Новгородского Кремля. Продолжить в режиме повествования?'
  state['context'] = 'somewhere'
  state['story_mode'] = True
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


  