from fun import big_image
hi = {
  'txt': '''Милости просим в нашу квест-сказку. Тут ты сможешь вместе с новгородским молодцем Садко\
  выполнить несколько заданий и заодно по Кремлю прогуляться.

Сперва-наперво запомни следующие правила, они тебе помогут:
  👇  Скажи "Повтори", если не расслышал, что тебе рассказали 
  ❌  Скажи "Хватит", коль устал ты в дороге и закончить хочешь
  ✨  Скажи "Помощь", чтобы прослушать правила еще раз.

Ты готов отправиться в путь?''',
  'tts': '''<speaker audio="dialogs-upload/ba73ad37-33af-4bea-8c8d-b6689c2febdd/2ce9e269-a82f-460d-a0cf-0bf40c4ebb35.opus">''',
  'buttons': [
      { 'title': "Да", 'hide': True },
      { 'title': "Нет", 'hide': True },
    ]
  }


quest = {
  'buttons': [
      { 'title': "Я готов", 'hide': False },
      { 'title': "Да", 'hide': True },
      { 'title': "Нет", 'hide': True},
    ]
  }

intro = {
  'buttons': [
      { 'title': "Повтори", 'hide': True },
      { 'title': "Да", 'hide': True },
      { 'title': "Нет", 'hide': True },
    ]
  }

needgeo_first = {
  'txt': 'Дабы не потеряться в тридевятом царстве возьми с собой один из волшебных клубков с геолокацией.',
  'tts': '<speaker audio="dialogs-upload/ba73ad37-33af-4bea-8c8d-b6689c2febdd/b9c53210-ce19-4b01-ba9b-ad99c8290ca4.opus">',
   'card': big_image(image_ids='''937455/7058de6afdae6f13c4b8''',description='Дабы не потеряться в тридевятом царстве возьми с собой один из волшебных клубков с геолокацией.')
}
needgeo = {
  'txt': 'Дабы не потеряться в тридевятом царстве возьми с собой один из волшебных клубков с геолокацией.',
  'tts': '<speaker audio="dialogs-upload/ba73ad37-33af-4bea-8c8d-b6689c2febdd/19fcba37-2e9e-468c-924f-86f2153a0a3f.opus">'
}
help_ = {
  'txt': '''Запомни следующие правила, они тебе помогут:
  👇   Скажи "Повтори", если не расслышал, что тебе рассказали 
  ❌  Скажи "Хватит", коль устал ты в дороге и закончить хочешь
  ✨  Скажи "Помощь", чтобы прослушать правила еще раз.
  Для выхода из справки скажи "Продолжить"''',
  'tts': '''Запомни следующие правила, они тебе помогут:
  Скажи Повтори, если не расслышал, что тебе рассказали. 
  Скажи Хватит, коль устал ты в дороге и закончить хочешь
  Скажи Помощь, чтобы прослушать правила еще раз'.
  Для выхода из справки, скажи: Продолжить.''',
	}

start = {
  'txt': 'Вступление',
  'tts': 'Вступление',
}



