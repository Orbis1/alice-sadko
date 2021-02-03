from fun import make_only_response
import phrases as ph

def welcome(state, context):
  state['context'] = context
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
  return make_only_response(
    text = ph.needgeo['txt'],
    tts = ph.needgeo['tts'],
    directives = { 'request_geolocation': {} },
  )

def fallback(command):
  txt='Вы молвили {}. Команда не распознана. Поробуйте ещё раз'.format(command)
  return make_only_response(
    text = txt,
  )