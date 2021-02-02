from fun import help_4_zagadka, text_to_resp, make_response, fallback, button,image_gallery,end_session1
from resource import answer, pers_step, pers_help, pers_zag,pers_sprav


def person (event,step,place, status=None):
#     print(step)
    intents  = event['request'].get('nlu',{}).get('intents')
    if step<3:
         param=text_to_resp(pers_step,place,step)
    if place is not None:
        if step==0:
            return make_response(text=param[0],tts=param[1],buttons=[
            button('Жар-птицу', hide=True)],step=step+1, place=place,
            status=param[2])
        elif step==1:
            if 'gift' in intents:
                return make_response(text=param[0],tts=param[1],buttons=[
                    button('Да', hide=True),button('Нет', hide=True)],step=step+2, place=place,
                                    status=param[2])
            else:
                step=step+1
                param=text_to_resp(pers_step,place,step)
                return make_response(text=param[0],tts=param[1], buttons=[
                    button('Да', hide=True),button('Нет', hide=True)],step=step+1, place=place,
                                    status=param[3])
        elif step == 3:
            if 'answer_da' in intents or 'YANDEX.CONFIRM' in intents:
                param=text_to_resp(pers_zag,pers_sprav[place][0],0)
                return make_response(text=param[0],tts=param[1],buttons=[
                    button('Повтори', hide=True),button('Я не знаю', hide=True)], 
                                     step=step+1, place=place,status=param[2])
            elif ('net' in intents or 'YANDEX.REJECT' in intents) and place=='kupol':
                return help_4_zagadka (event,999)

            elif ('net' in intents or 'YANDEX.REJECT' in intents) and place!='kupol':
                return end_session()        
            else:
                return fallback(event)
# Блок обработки "я готов"            

        elif step==4:
#             print('я тут на шаге4')
            if answer[place][0] in intents:
                param=text_to_resp(pers_zag,pers_sprav[place][0],1)
           
                return make_response(text=param[0],tts=param[1],buttons=[
                    button('Да', hide=True),button('Нет', hide=True)], step=step+1, place=place,
                                    status=param[2])
            elif 'povtor'in intents or "YANDEX.REPEAT" in intents:
                if status=='help_not_end' or status=='help_end':
                    return help_4_zagadka (event,pers_sprav[place][0],povtor=True)
                else:
                    param=text_to_resp(pers_zag,pers_sprav[place][0],0)
                    return make_response(text=param[0],tts=param[1],buttons=[
                    button('Повтори', hide=True),button('Я не знаю', hide=True)],
                                     step=step, place=place,status=param[2])
#             elif 'net' in intents or 'YANDEX.REJECT' in intents:  
            else:
                return help_4_zagadka (event,pers_sprav[place][0]) 
        elif step==5:
            if 'answer_da' in intents or 'YANDEX.CONFIRM' in intents:
                param=text_to_resp(pers_zag,pers_sprav[place][1],0)
                return make_response(text=param[0],tts=param[1],buttons=[
                    button('Повтори', hide=True),button('Я не знаю', hide=True)], 
                                     step=step+1, place=place,status=param[2])
            elif ('net' in intents or 'YANDEX.REJECT' in intents):
                param=text_to_resp(pers_end,place,obj_3=True,obj_4=True)
                return end_session1()
            elif 'povtor'in intents or "YANDEX.REPEAT" in intents:
                param=text_to_resp(pers_zag,pers_sprav[place][0],1)
                return make_response(text=param[0],tts=param[1],buttons=[
                    button('Повтори', hide=True),button('Я не знаю', hide=True)],
                                     step=step+1, place=place,status=param[2])
            return end_session1()
        elif step==6:
            if answer[place][1] in intents:
                param=text_to_resp(pers_zag,pers_sprav[place][1],1,obj_3=True)
           
                return make_response(text=param[0],tts=param[1],buttons=[
                    button('Да', hide=True),button('Нет', hide=True)], step=1, place=place,
                                    status=param[2],place_next=param[3])
            elif 'povtor'in intents or "YANDEX.REPEAT" in intents:
                if status=='help_not_end' or status=='help_end':
                    return help_4_zagadka (event,pers_sprav[place][1],povtor=True)
                else:
                    param=text_to_resp(pers_zag,pers_sprav[place][1],0)

                    return make_response(text=param[0],tts=param[1],buttons=[
                    button('Повтори', hide=True),button('Я не знаю', hide=True)],
                                     step=step, place=place,status=param[2])
#             elif 'net' in intents or 'YANDEX.REJECT' in intents:  - Это перепрыг с шага 4
            else:
                print('я тут шаг 6')
                return help_4_zagadka (event,pers_sprav[place][1])             
        else:
            return fallback(event)