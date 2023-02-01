# Microservice pattern

### TODO:

- Добавить комментарии
- Добавить fanout exchange routing пример
- Добавить больше примеров сервисов


### Start

```
docker-compose up --build
```

open new terminal

```
cd client
python3 main.py
```

open new terminal

```
cd service1
python3 main.py
```

open new terminal

```
cd service2
python3 main.py
```

### Usage

Go to `http://localhost:8000/docs`

Make request to any endpoint and look in terminal

### Requirements to start

- docker-compose 1.26.0
- docker 20.10.9
