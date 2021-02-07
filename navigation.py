from person import person
from fun import big_image, make_only_response
from resource import quest_order, find_object
from intro import get_distance_to_object
from sights import sights
from intro import say_help, fallback
import math


def give_direction(data, sessionState, appState):
  # Контент для ответа
  txt = data[0]
  tts = data[1]
  card = big_image(image_ids=data[2], description=txt) if data[2] is not None else None

  buttons = [
    { 'title': "Повтори", 'hide': True },
    { 'title': "Да", 'hide': True },
    { 'title': "Нет", 'hide': True },
  ]

  # Работа со стейтом
  sessionState['nav_context'] = 'give_direction'

  nav_step = sessionState.get('nav_step')
  if nav_step is None or nav_step=='null':
    sessionState['nav_step'] = 1
  else:
    sessionState['nav_step'] += 1
  

  return make_only_response(
    text=txt,
    tts=tts,
    buttons=buttons,
    card=card
  )

def tell_story(data, sessionState, appState):
  # Контент для ответа
  txt = data[0]
  tts = data[1]
  card = big_image(image_ids=data[2], description=txt) if data[2] is not None else None
  buttons = [
    { 'title': "Да", 'hide': True },
    { 'title': "Нет", 'hide': True },
  ]

  # Работа со стейтом
  sessionState['nav_context'] = 'tell_story'

  nav_step = sessionState.get('nav_step')
  if nav_step is None or nav_step=='null':
    sessionState['nav_step'] = 1
  else:
    sessionState['nav_step'] += 1
  
  return make_only_response(
    text=txt,
    tts=tts,
    buttons=buttons,
    card=card
  )

def give_direction_last(data, sessionState, appState, add_text=None, dist=None ):
  # Контент для ответа
  add=''
  if dist is not None:
    add = 'Осталось пройти немного: {} метр(а) \n'.format(math.trunc(dist)) 

  if add_text is not None:
    txt = add + add_text[0] + '\n' + data[0]
    tts = add + add_text[1] + '\n' + data[1]
    sessionState['status']='full_story'
  else:
    txt = add + data[0]
    tts = add + data[1]
    sessionState['status']=None  
  
  card = big_image(image_ids=data[2], description=txt) if data[2] is not None else None

  buttons = [
    { 'title': "Где я?", 'hide': True },
    { 'title': "Я готов", 'hide': True },
    { 'title': "Повтори", 'hide': True },
  ]

  # Работа со стейтом
  sessionState['nav_context'] = 'give_direction_last'

  nav_step = sessionState.get('nav_step')
  if nav_step is None or nav_step=='null':
    sessionState['nav_step'] = 1
  else:
    sessionState['nav_step'] += 1
  
  return make_only_response(
    text=txt,
    tts=tts,
    buttons=buttons,
    card=card
  )

def switch_to_pers(data, sessionState, appState):
  # Контент для ответа
  txt = data[0]
  tts = data[1]
  
  card = big_image(image_ids=data[2], description=txt) if data[2] is not None else None
  buttons = [
    { 'title': "Где я?", 'hide': False },
    { 'title': "Я готов", 'hide': False },
    { 'title': "Повтори", 'hide': False },
  ]

  # Работа со стейтом
  sessionState['nav_context'] = 'give_direction_last'
  sessionState['context'] = 'quest'

  nav_step = sessionState.get('nav_step')
  if nav_step is None or nav_step=='null':
    sessionState['nav_step'] = 1
  else:
    sessionState['nav_step'] += 1
  
  return make_only_response(
    text=txt,
    tts=tts,
    buttons=buttons,
    card=card
  )

def navigation(appState, sessionState, intents, user_location, event={}):
  # Запоминаем ключевые данные из state
  step = sessionState.get('nav_step', 0)
  step = 0 if step == 'null' else step
  place_seen = appState.get('place_seen')
  place = quest_order[0] if place_seen is None or place_seen=='null' else place_seen
  nav_context = sessionState.get('nav_context')
  story_mode = sessionState.get('story_mode', False)

  sessionState['context'] = 'navigation'
  appState['place_seen'] = place

  data = find_object[place]

  # Сказать полюзователю куда идти
  if step == 0 and (nav_context is None or nav_context == 'null'):
    return give_direction(data[0], sessionState, appState)
  
  # Рассказать про место, куда он идёт
  elif nav_context == 'give_direction':
    if 'answer_da' in intents or 'YANDEX.CONFIRM' in intents:
      return tell_story(data[1], sessionState, appState)
    elif 'net' in intents or 'YANDEX.REJECT' in intents:
      return give_direction_last(data[3], sessionState, appState)
    elif 'povtor'in intents or "YANDEX.REPEAT" in intents or 'next' in intents:
      return give_direction(data[0], sessionState, appState)
    elif 'help'in intents:
      return say_help()
    else:
      return fallback(event.get('request', 'no event').get('command', 'no command'))

  # Историческая справка, про то куда он идёт
  elif nav_context == 'tell_story':
    if 'answer_da' in intents or 'YANDEX.CONFIRM' in intents:
      return give_direction_last(data[3], sessionState, appState, add_text=data[2])
    elif 'net' in intents or 'YANDEX.REJECT' in intents:
      return give_direction_last(data[3], sessionState, appState)
    elif 'povtor'in intents or "YANDEX.REPEAT" in intents or 'next' in intents:
      return tell_story(data[1], sessionState, appState)
    elif 'help'in intents:
      return say_help()
    else:
      return fallback(event.get('request', 'no event').get('command', 'no command'))

  elif 'povtor'in intents or "YANDEX.REPEAT" in intents or 'next' in intents:
    if sessionState['status'] == 'full_story':
      return give_direction_last(data[3], sessionState, appState, add_text=data[2])
    else:
      return give_direction_last(data[3], sessionState, appState)
  elif 'help'in intents:
      return say_help()

  # обработка "Где я?"
  elif 'where_am_i' in intents or 'i_am_here' in intents:
    print('user_location', user_location)
    if user_location is not None and user_location['accuracy'] < 66 and story_mode==False:
    # если геолокация есть и погрешность не больше 50 метров мы не в режиме истории
      target = sights[place]
      distance = get_distance_to_object(user_location, target['location'])
      print('Расстояние до {name} составялет {distance}'.format(name=target, distance=distance))
      if distance > 30:
        return give_direction_last(data[4], sessionState, appState, dist=distance)
      if distance <= 30:
        return give_direction_last(data[5], sessionState, appState)
    else:
      if story_mode==True:
      # если мы в режиме истории, то переходим к следующему объекту
        return give_direction_last(data[5], sessionState, appState)
      else:
      # если геолокации нет или слишком большая погредшность, то даём подсказку
        return give_direction_last(data[4], sessionState, appState)
     

  # обработка "Я готов"
  elif 'im_ready' in intents:
    return person(event=event, step=appState['step'], place=appState['place_seen'], status=appState.get('status'))
  
  else:
    return fallback(event.get('request', 'no event').get('command', 'no command'))




