Для запуска бота на проверку работоспособности бота есть два варианта:

1. Путь меньшего сопротивления

Написать https://t.me/lizzzarrrd, чтобы добавила вас в Test Users в Google Cloud и подняла сервер и контейнер с ботом. После этих простых действий можно будет пользоваться

2. Развернуть все с самого начала

В `docker-compose.yml` должно быть следующее поле:

```
ports:
  - "8080:8080"
 ```

После запуска контейнера можно проверить, что все будет работать. Должно вывести `ok`

```
curl http://localhost:8080/health
```

Установить ngrok

Запустить. Здесь вернется ссылка переадресации
```
ngrok http 8080
```



Теперь в `.env` нужно прописать
```
GOOGLE_REDIRECT_URI=ссылка которую отдал ngrok/google/callback
```


 В Google Console нужно создать новый проект. 
 Зайти APIs & Services и создать Credentials OAuth client ID с Application type "Web Application". В `.env` добавить поля `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`

И обязательно в APIs & Service -> Library подключить Google Calendar API

В Audience нужно добавить Test users 

