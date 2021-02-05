# Fake 
from fun import fallback
from person import person
import navigation as n

def handler(event, context):

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
    def worker(request, sessionState, appState, event):
        intents = request.get('nlu',{}).get('intents', {})
        command = request.get('command')
        context = sessionState.get('context')
        geo_asked = sessionState.get('geo_asked', False)
        story_mode = sessionState.get('story_mode')

        if new_session==True: 
            if appState.get('place')!='null' and appState.get('place') is not None:
                return n.continue_game(sessionState)
            else:
                return n.welcome(state=sessionState)

        if context=='continue_game':
            if 'YANDEX.CONFIRM' in intents:
                return person(event=event, step=0, place=appState['place'], status=appState.get('status'))
            if 'YANDEX.REJECT' in intents:
                return n.welcome(state=sessionState, appStateClear=True, appState=appState)      

        if context=='welcome':
            if 'YANDEX.CONFIRM' in intents:
                # запрос геолокации
                if user_location is None and geo_asked==False:
                    return n.ask_geo(state=sessionState)
                if user_location is not None:
                    return n.how_far_from_kremlin(sessionState=sessionState, appState=appState, user_location=user_location)
            if 'YANDEX.REJECT' in intents:
                    return n.bye()

        # запрос геолокации
        if user_location is None and geo_asked==False and context!='quest_begin':
            return n.ask_geo(state=sessionState)

        # начало. где находится пользоваетль
        if context=='ask_geo':
            return n.how_far_from_kremlin(sessionState=sessionState, appState=appState, user_location=user_location)

        if context=='within_kremlin':
            return n.say('Начать экскурсию')

        if context=='around_kremlin':
            return n.say('Подойти к воротам')

        if context=='somewhere':
            if 'YANDEX.CONFIRM' in intents:
                return n.quest_begin(sessionState=sessionState, appState=appState)
            if 'YANDEX.REJECT' in intents:
                return n.bye()

        if context=='quest_begin':
            return person(event=event, step=appState['step'], place=appState['place'], status=appState.get('status'))

        if 'help' in intents:
            return n.say_help()

        return n.fallback(command)

    # skill answer
    response = worker(request, sessionState, appState, event)

    webhook_response={
        'response': response,
        'session_state': sessionState,
        'application_state': appState,
        'version': event['version']
    }
    print('>>>webhook_response: ', webhook_response, appId)

    return webhook_response
