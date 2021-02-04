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
    appId = event['session']['application'].get('application_id', None)
    print('>>>event: ', event, appId)

    # state
    appState = event['state']['application']
    sessionState = event['state']['session']
    print('>>>sessionState: ', sessionState, appId)
    print('>>>appState: ', appState, appId)

    # request
    request = event['request']
    print('>>>request: ', request, appId)

    # skill logic
    def worker(request, sessionState, appState):
        intents = request.get('nlu',{}).get('intents', {})
        command = request.get('command')
        context = sessionState.get('context')
        geo_asked = sessionState.get('geo_asked', False)
        story_mode = sessionState.get('story_mode')

        print('Обработка новой сессии')
        if new_session==True: 
            if story_mode==True or appState.get('step'):
                return n.continue_game(sessionState)
            else:
                return n.welcome(state=sessionState)


        if context=='continue_game':
            if 'YANDEX.CONFIRM' in intents:
                return person(event, appState.get('step'), 'kupol')
            if 'YANDEX.REJECT' in intents:
                return n.clear_app_state(appState, sessionState)       

        if context=='welcome':
            print('YANDEX.CONFIRM' in intents, )
            if 'YANDEX.CONFIRM' in intents:
                # запрос геолокации
                if user_location is None and geo_asked==False:
                    return n.ask_geo(state=sessionState)
                if user_location is not None:
                    return n.how_far_from_kremlin(sState=sessionState, aState=appState, user_location=user_location)
            if 'YANDEX.REJECT' in intents:
                    return n.bye()

        # запрос геолокации
        if user_location is None and geo_asked==False:
            return n.ask_geo(state=sessionState)

        # начало. где находится пользоваетль
        if context=='ask_geo':
            return n.how_far_from_kremlin(sState=sessionState, aState=appState, user_location=user_location)

        if context=='within_kremlin':
            return n.say('Начать экскурсию')

        if context=='around_kremlin':
            return n.say('Подойти к воротам')

        if context=='somewhere':
            if 'YANDEX.CONFIRM' in intents:
                return person(event, appState.get('step'), 'kupol')
            if 'YANDEX.REJECT' in intents:
                return n.bye()

        # Если есть данные в appState
        # if story_mode==True:
        #     if context=='somewhere':
        #         if 'YANDEX.CONFIRM' in intents:
        #             return person(event, appState.get('step'), 'kupol')
        #         if 'YANDEX.REJECT' in intents:
        #             return n.bye()
        #     else:
        #         return person(event, appState.get('step'), 'kupol')

        if 'help' in intents:
            return n.say_help()

        return n.fallback(command)

    # skill answer
    response = worker(request, sessionState, appState)
    print('>>>response: ', response, appId)

    return {
        'response': response,
        'session_state': sessionState,
        'application_state': appState,
        'version': event['version']
    }
