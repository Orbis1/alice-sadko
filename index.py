# Fake 
from fun import fallback
from person import person

def handler(event, context):
   
    print (event)
    intents = event['request'].get('nlu',{}).get('intents')
    text = {'Куку тест функции'}
    # Перенести
    step=event.get('state').get('application').get('step')
    status=event.get('state').get('application').get('status')
    
    if event['session']['new']:
        place_first='kupol'
        step=0
        return person(event,step,place_first)

    elif step >0:
        place_early=event.get('state').get('application').get('place_seen')
        return person(event,step,place_early, status=status)
    else:
        return fallback(event)