# VoiceAssistantBot
При построении телеграмм бота использовалась модель преобразования голоса в текст от vosk, последующее наложение пунктуации моделью от silero и вычленение именованных сущностей с помощью библиотеки Natasha. 
Бот полностью работоспособный, способен выполнять поставленную задачу, но с некоторыми оговорками: 
1) требуется дать доступ на отправку сообщений сотрудникам только руководителю (не успел сделать)
2) можно попробовать подключить другие модели или дообучить текущие
3) нужна коррекция выделения именных сущностей, так как в этом черновом варианте данная опция может неправильно работать в случае нахождения в базе данных двух и более лиц с одинаковыми именами или фамилиями

Также не забудьте подставить необходимые модели и средства для работы с ними в папку models и файл с токеном бота в папку token (что конретно сделать, написано в соответствующих файлах в репозитории)
