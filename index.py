# Fake 
from fun import fallback
from person import person
import navigation as n

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
        geo_asked = appState.get('geo_asked', False)

        if new_session: return n.welcome(state=sessionState, context='welcome')

        # if user_location is None:
        #     if geo_asked!=True:
        #         return n.ask_geo(appState)
        #     else:
        #         return n.say('уйбуй')

        if 'YANDEX.CONFIRM' in intents:
            if context=='welcome': return n.say('Переход к запросу навигации')

        if 'YANDEX.REJECT' in intents:
            if context=='welcome': return n.say('Выход из квеста')

        if 'help' in intents:
            return n.say_help()

        return n.fallback

    # skill answer
    response = worker(request, sessionState, appState)

    return {
        'response': response,
        'session_state': sessionState,
        'application_state': appState,
        'version': event['version']
    }






    # if user_location is None and geo_asked=True:
    #     #

    # if context == 'ask_geo' and geo_type == "Geolocation.Allowed":
    #     # пользователь дал разрешение на использование гео-локации
    #     geo_asked = True
    #     geo_allowed = True

    # if context == 'ask_geo' and geo_type == "Geolocation.Rejected":
    #     # пользователь не дал разрешение на использование гео-локации




    # elif step >0:
        # place_early=event.get('state').get('application').get('place_seen')
        # return person(event,step,place_early, status=status)
    # else:
        # return fallback(event)


