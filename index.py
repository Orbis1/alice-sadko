# Fake 
from fun import fallback
from person import person
import navigation as n
import game

def handler(event, context):


   
    # print (event)
    # intents = event['request'].get('nlu',{}).get('intents')
    # text = {'Куку тест функции'}
    # Перенести
    # step=event.get('state').get('application').get('step')
    # status=event.get('state').get('application').get('status')

    # session
    new_session = event['session']['new']
    user_location = event['session'].get('location')

    # state
    appState = event['state']['application']
    sessionState = event['state']['session']

    # request
    request = event['request']

    # skill logic
    def worker(request, sessionState, appState):
        intents = request.get('nlu',{}).get('intents', {})
        command = request['command']
        context = sessionState.get('context')
        geo_asked = sessionState.get('geo_asked', False)

        if new_session: return n.welcome(state=sessionState, context='welcome')

        if user_location is None:
            if geo_asked==False:
                return n.ask_geo(state=sessionState)
            else:
                 # начало игры без геолокации
                return game.start(request, sessionState, appState,  with_geo=False)
        else:
            # начало игры c геолокацией
            return game.start(request, sessionState, appState, with_geo=True)

        if 'YANDEX.CONFIRM' in intents:
            if context=='welcome': return n.say('Переход к запросу навигации')

        if 'YANDEX.REJECT' in intents:
            if context=='welcome': return n.say('Выход из квеста')

        if 'help' in intents:
            return n.say_help()

        return n.fallback(command)

    # skill answer
    response = worker(request, sessionState, appState)

    return {
        'response': response,
        'session_state': sessionState,
        'application_state': appState,
        'version': event['version']
    }

    




