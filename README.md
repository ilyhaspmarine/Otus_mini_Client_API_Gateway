# Домашнее задание №6
## Backend for frontends. Apigateway

### Вариант 1 (С КОДОМ)

#### Добавить в приложение аутентификацию и регистрацию пользователей.

### Здесь у нас API Gateway. Реализует 3 сценария:
- Создание нового пользователя и профиля (запрос на client/register)
- Аутентификация пользователя с генерацией JWT (запрос на client/login)
- Получение данных профиля (GET-запрос на profile/users)
- Изменение данных профиля (PUT-запрос на profile/users)

### ПОДГОТОВКА
#### в /etc/hosts прописываем
```
127.0.0.1 arch.homework 
```

#### Запускаем docker
любым вариантом, у меня docker desktop с виртуализацией VT-d

#### Запускаем minikube
```
minikube start --driver=docker
```

#### NGINX
Считам, что с прошлой домашки никуда не ушел из кластеа

### СТАВИМ ПРИЛОЖЕНИЕ
#### Сперва генерируем ключи для сервиса аутентификации (см. репозиторий ниже)
```
https://github.com/ilyhaspmarine/Otus_mini_auth
```
##### Забираем сгенерированный для аутентификации оттуда файлик etc/keys/jwt-public.pem - это открытый ключ для валидации JWT нашим Gateway
##### ВАЖНО: файлик должен быть один и тот же (с одинаковым ключом)


#### Создаем namespace под gateway
```
kubectl create namespace client
```

#### "Внешняя" поставка секретов в кластер
##### Секрет с ключом для валидации токенов
```
kubectl create secret generic jwt-validation-key --from-file=public.pem=./etc/keys/jwt-public.pem -n client
```

#### Ставимся и ждем, пока установка закончится
```
helm install <имя_релиза> client-api -n client --create-namespace
```

#### Включаем (и не закрываем терминал)
```
minikube tunnel
```

#### Проверяем health-check (в новом окне терминала)
```
curl http://arch.homework/client/health/
```


### КАК УДАЛИТЬ ПРИЛОЖЕНИЕ
#### Сносим чарт и БД
```
helm uninstall <имя релиза> -n client
```

#### Сносим секреты
```
kubectl delete secret jwt-validation-key -n client
```

### Готово!