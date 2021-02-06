from person import person
from fun import fallback, make_only_response
from resource import quest_order, find_object
from intro import get_distance_to_object
from sights import sights
from intro import say_help


def give_direction(data, sessionState, appState):
  # Контент для ответа
  txt = data[0]
  tts = data[1]
  # картинка??
  buttons = [
    { 'title': "Повтори", 'hide': False },
    { 'title': "Да", 'hide': False },
    { 'title': "Нет", 'hide': False },
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
    # tts=tts,
    buttons=buttons
  )

def tell_story(data, sessionState, appState):
  # Контент для ответа
  txt = data[0]
  tts = data[1]
  # картинка??
  buttons = [
    { 'title': "Да", 'hide': False },
    { 'title': "Нет", 'hide': False },
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
    # tts=tts,
    buttons=buttons
  )

def give_direction_last(data, sessionState, appState, add_text=None):
  # Контент для ответа
  if add_text is not None:
    txt = add_text[0] + '\n' + data[0]
    tts = add_text[1] + '\n' + data[1]
  else:
    txt = data[0]
    tts = data[1]
  
  # картинка??
  buttons = [
    { 'title': "Где я?", 'hide': False },
    { 'title': "Я на месте", 'hide': False },
    { 'title': "Повтори", 'hide': False },
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
    # tts=tts,
    buttons=buttons
  )

def switch_to_pers(data, sessionState, appState):
  # Контент для ответа
  txt = data[0]
  tts = data[1]
  
  # картинка??
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
    # tts=tts,
    buttons=buttons
  )

def navigation(appState, sessionState, intents, user_location, event={}):
  # Запоминаем ключевые данные из state
  step = sessionState.get('nav_step', 0)
  place_seen = appState.get('place_seen')
  place = quest_order[0] if place_seen is None or place_seen=='null' else place_seen
  nav_context = sessionState.get('nav_context')
  story_mode = sessionState.get('story_mode')

  sessionState['context'] = 'navigation'
  appState['place_seen'] = place

  data = find_object[place]

  # Сказать полюзователю куда идти
  if step == 0:
    return give_direction(data[0], sessionState, appState)
  
  # Рассказать про место, куда он идёт
  elif nav_context == 'give_direction':
    if 'answer_da' in intents or 'YANDEX.CONFIRM' in intents:
        return tell_story(data[1], sessionState, appState)
    elif 'net' in intents or 'YANDEX.REJECT' in intents:
        return give_direction_last(data[3], sessionState, appState)
    # elif 'help' in intents:
    #   return help(nav_context)
    #   return give_direction(data[0], sessionState, appState)
    # else:
    #   return fallback(2step)

  # Историческая справка, про то куда он идёт
  elif nav_context == 'tell_story':
    if 'YANDEX.CONFIRM' in intents:
      return give_direction_last(data[3], sessionState, appState, add_text=data[2])
    elif 'YANDEX.REJECT' in intents:
      return give_direction_last(data[3], sessionState, appState)
    elif 'povtor' in intents:
      return tell_story(data[1], sessionState, appState)

  # обработка "Где я?"
  elif 'where_am_i' in intents:
    if user_location is not None and user_location['accuracy'] < 50 and story_mode==False:
    # если геолокация есть и погрешность не больше 50 метров мы не в режиме истории
      target = sights[place]
      distance = get_distance_to_object(user_location, target['location'])
      if distance > 50:
        return give_direction_last(data[4], sessionState, appState)
      if distance < 50:
        return give_direction_last(data[5], sessionState, appState)
    else:
      if story_mode==True:
      # если мы в режиме истории, то переходим к следующему объекту
        return give_direction_last(data[5], sessionState, appState)
      else:
      # если геолокации нет или слишком большая погредшность, то даём подсказку
        return give_direction_last(data[4], sessionState, appState)
    

  # обработка "Я на месте"
  elif 'i_am_here' in intents:
    return person(event=event, step=appState['step'], place=appState['place_seen'], status=appState.get('status'))
  
  else:
    return fallback(event)




