event = {'meta': {'locale': 'ru-RU', 'timezone': 'UTC', 'client_id': 'ru.yandex.searchplugin/7.16 (none none; android 4.4.2)', 'interfaces': {'screen': {}, 'payments': {}, 'account_linking': {}, 'geolocation_sharing': {}}}, 'session': {'message_id': 0, 'session_id': 'a88a2a70-1215-413c-9d71-9fe355738455', 'skill_id': 'ca5036ee-1029-4a07-960c-8cf27f1258a3', 'application': {'application_id': '48D4B4B7078B8F72846AF67DACB63DADF2FA73D1C19AC1D068BF3676BB357507'}, 'user_id': '48D4B4B7078B8F72846AF67DACB63DADF2FA73D1C19AC1D068BF3676BB357507', 'new': True}, 'request': {'command': 'ping', 'original_utterance': 'ping', 'nlu': {'tokens': [], 'entities': [], 'intents': {}}, 'markup': {'dangerous_context': False}, 'type': 'SimpleUtterance'}, 'version': '1.0'}

appState = event.get('state', {}).get('application')

print(type(event))
print(type(event.get('state', {})))
print(type(event.get('state', {}).get('application')))
print(appState)