from fun import make_only_response
from resource import quest_order, find_object

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
    { 'title': "Я на месте?", 'hide': False },
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

def navigation(appState, sessionState, intents, user_location):
  # Запоминаем ключевые данные из state
  step = sessionState.get('nav_step', 0)
  place_seen = appState.get('place_seen')
  place = quest_order[0] if place_seen is None or place_seen=='null' else place_seen
  nav_context = sessionState.get('nav_context')

  sessionState['context'] = 'navigation'

  data = find_object[place]

  # Сказать полюзователю куда идти
  if step == 0:
    return give_direction(data[0], sessionState, appState)
  
  # Рассказать про место, куда он идёт
  if nav_context == 'give_direction':
    if 'YANDEX.CONFIRM' in intents:
        return tell_story(data[1], sessionState, appState)
    if 'YANDEX.REJECT' in intents:
        return give_direction_last(data[3], sessionState, appState)

  # Историческая справка, про то куда он идёт
  if nav_context == 'tell_story':
    if 'YANDEX.CONFIRM' in intents:
      return give_direction_last(data[3], sessionState, appState, add_text=data[2])
    if 'YANDEX.REJECT' in intents:
      return give_direction_last(data[3], sessionState, appState)


  # обработка "Где я?"

  # обработка "Я на месте"

  
  return make_only_response(
    text='жопа-жопа-жопа-жопа',
  )

  


