# person
from fun import help_4_zagadka, text_to_resp, make_response, fallback, button,end_session1
from resource import fallback_answer,answer, pers_step, pers_zag,pers_sprav, quest_order
from intro import say_help


def person(event,step,place, status=None, id_zag=None):
    event['state']['session']['context']='quest'
    event['state']['session']['nav_context']=None
    intents=event['request'].get('nlu',{}).get('intents')
    step = 0 if step=='null' or step is None else step
#     spravka=event.get('state').get('session').get('spravka')
    # if step==0:
#         Выбираем ИД загадки
        # id_zag=random.choice(pers_sprav[place]['medium']) # в дальнейшем можно прописать уровень
    if step<3:
         param=text_to_resp(pers_step,place,step)
    if place is not None:
        if step==0:
            return make_response(text=param[0],tts=param[1],buttons=[
            button('Повтори', hide=True), button('Жар-птицу', hide=True),button('Я не знаю', hide=True),],step=step+1, place=place,
            status=param[2], event=event)
        elif step==1:
            if 'gift' in intents:
                return make_response(text=param[0],tts=param[1],buttons=[
                    button('Да', hide=True),button('Нет', hide=True)],step=step+2, place=place,
                                    status=param[2], event=event)
            elif 'povtor'in intents or "YANDEX.REPEAT" in intents or 'next' in intents:
                event['state']['session']['spravka']=None
                step=0
                param=text_to_resp(pers_step,place,step)
                return make_response(text=param[0],tts=param[1],buttons=[
            button('Повтори', hide=True), button('Жар-птицу', hide=True),button('Я не знаю', hide=True),],step=step+1, place=place,
            status=param[2], event=event)
            elif 'help' in intents:
                event['state']['session']['spravka']='spravka'
                return say_help()
            elif event['state']['session']['spravka']=='spravka2':
                param=text_to_resp(fallback_answer,place,1)
                return end_session1(text=param[0],tts=param[1],event=event)
            elif event['state']['session']['spravka']=='spravka':
                event['state']['session']['spravka']='spravka2'
                param=text_to_resp(fallback_answer,place,3)
                return make_response(text=param[0],tts=param[1],buttons=[
                    button('Продолжить', hide=True)], step=step, place=place,
                                    status=status, event=event)
            
            else:
                step=step+1
                param=text_to_resp(pers_step,place,step)
                return make_response(text=param[0],tts=param[1], buttons=[
                    button('Да', hide=True),button('Нет', hide=True)],step=step+1, place=place,
                                    status=param[2], event=event)
        # elif 'im_ready' in intents:
        #     appState = event['state']['application']
        #     sessionState = event['state']['session']
        #     user_location = event['session'].get('location')
        #     return  navigation(appState, sessionState, intents, user_location, event)
# Обработка ответа "да"
        elif 'help' in intents:
            event['state']['session']['spravka']='spravka'
            return say_help()
        elif 'answer_da' in intents or 'YANDEX.CONFIRM' in intents:
            if step ==4 or step ==6:
                return make_response(text='Говори!', step=step,place=place,status=status, event=event)
            else:
                if step==3:
                    param=text_to_resp(pers_zag,pers_sprav[place][0],0)
                elif step==5:
                    param=text_to_resp(pers_zag,pers_sprav[place][1],0)
                return make_response(text=param[0],tts=param[1],buttons=[
                    button('Повтори', hide=True),button('Я не знаю', hide=True),button('Я знаю', hide=True)], 
                                     step=step+1, place=place,status=param[2], event=event)
#  Обработка ответа "Нет"

        elif 'net' in intents or 'YANDEX.REJECT' in intents:
            if step==3:
                if place=='kupol':
                    return help_4_zagadka (event,999)                   
                elif place!='kupol':
                    if status == 'fallback_answer':
                        return end_session1(event=event)
                    else:
                        param=text_to_resp(fallback_answer,place,2)
                        return make_response(text=param[0],tts=param[1],buttons=[
                    button('Да', hide=True),button('Нет', hide=True)], step=step, place=place,
                                    status=param[2], event=event)
            elif step == 5:
                param=text_to_resp(pers_zag,pers_sprav[place][1],1,obj_3=True)
                return make_response(
                    text=param[0],
                    tts=param[1],
                    step=0,
                    place=getNextPlace(place),
                    status=param[2],
                    place_next=param[3], 
                    event=event,
                    context='navigation',
                    buttons=[{ 'title': "Я готов", 'hide': True }],
                    # nav_context='give_direction',
                    nav_step=0

                    )    
            elif step == 4:
                return help_4_zagadka (event,pers_sprav[place][0])
            elif step==6:
                return help_4_zagadka (event,pers_sprav[place][1])
                
# Обработка повторов            
                
        elif 'povtor'in intents or "YANDEX.REPEAT" in intents or 'next' in intents:
            event['state']['session']['spravka']=None
            if status=='help_not_end' or status=='help_end':
                if step==3: return help_4_zagadka (event,999,povtor=True)
                if step==4: return help_4_zagadka (event,pers_sprav[place][0],povtor=True)
                if step==6: return help_4_zagadka (event,pers_sprav[place][1],povtor=True)
            else:
                if step==3:
                    step=1
                    param=text_to_resp(pers_step,place,step) #step=1
                    buttons=[button('Да', hide=True),button('Нет', hide=True)]
                    step=step+2
                if step==4: 
                    param=text_to_resp(pers_zag,pers_sprav[place][0],0)
                    buttons=[button('Повтори', hide=True),button('Я не знаю', hide=True),button('Я знаю', hide=True)]
                if step==5:
                    param=text_to_resp(pers_zag,pers_sprav[place][0],1)
                    buttons=[button('Да', hide=True),button('Нет', hide=True)]
                if step==6:
                    param=text_to_resp(pers_zag,pers_sprav[place][1],0)
                    buttons=[button('Повтори', hide=True),button('Я не знаю', hide=True),button('Я знаю', hide=True)]
                return make_response(text=param[0],tts=param[1],buttons=buttons,
                                     step=step, place=place,status=param[2], event=event)
# обработка правильных ответов
        elif answer[place][pers_sprav[place][0]] in intents and step==4:
                param=text_to_resp(pers_zag,pers_sprav[place][0],1)
                return make_response(text=param[0],tts=param[1],buttons=[
                    button('Да', hide=True),button('Нет', hide=True)], step=step+1, place=place,
                                    status=param[2], event=event)
        elif answer[place][pers_sprav[place][1]] in intents and step==6:
                param=text_to_resp(pers_zag,pers_sprav[place][1],1,obj_3=True)
                return make_response(
                    text=param[0],
                    tts=param[1],
                    step=0, place=getNextPlace(place),
                    status=param[2],
                    place_next=param[3], 
                    event=event,
                    context='navigation',
                    buttons=[{ 'title': "Я готов", 'hide': True }],
                    # nav_context='give_direction'
                    nav_step=0
                )
#  обработка других ответов по справке
        elif event['state']['session']['spravka']=='spravka2':
            param=text_to_resp(fallback_answer,place,1)
            return end_session1(text=param[0],tts=param[1],event=event)
        elif event['state']['session']['spravka']=='spravka':
            event['state']['session']['spravka']='spravka2'
            param=text_to_resp(fallback_answer,place,3)
            return make_response(text=param[0],tts=param[1],buttons=[
                    button('Продолжить', hide=True)], step=step, place=place,
                                    status=status, event=event)
# Обработка else

        else:
            if step==3 or step==5:
                if status == 'fallback_answer':
                    param=text_to_resp(fallback_answer,place,1)
                    return end_session1(text=param[0],tts=param[1],event=event)
                else:
                    param=text_to_resp(fallback_answer,place,0)
                    return make_response(text=param[0],tts=param[1],buttons=[
                    button('Да', hide=True),button('Нет', hide=True)], step=step, place=place,
                                    status=param[2], event=event)
            else:
                if step==4:
                    return help_4_zagadka (event,pers_sprav[place][0])
                if step==6:
                    return help_4_zagadka (event,pers_sprav[place][1])
                return fallback(event)
            return fallback(event)
        return fallback(event)

def getNextPlace(place):
    place_next=''
    place_index = quest_order.index(place)
    if place_index+1 <= len(quest_order)-1:
        # переход к следующему объекту
        place_next=quest_order[place_index+1]
    else:
        # все объекты закончились
        place_next='end'
    return place_next
