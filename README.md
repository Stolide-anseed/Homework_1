## Ключевые команды:

1. uv - запускает проверочный вариант для показательного запуска:
``` Bash 
 curl ‐X POST localhost:8000/v1/predict ‐H "Content‐Type: application/json" ‐d @test.json
```


3.  Pytest - запускает проверку 8 тестов:
``` Bash
uv run pytest
```
![Результат pytest](<image_for_readme/Pasted image 20260930164846.png>)

2. Docker compose:
``` PowerShell
docker compose up -d --build
```
![Docker Compose](<image_for_readme/Pasted image 20260930165049.png>)


3. Kind - создаёт кластер "hw":
``` Bash
kind create cluster --name hw
```


4. Kubectl - показывает кластеры для работы и немного их характеристик(Ready 0/1, status, age):
```
kubectl get pods
```
![Состояние Pod](<image_for_readme/Pasted image 20260930170401.png>)


## Скриншоты для проверки:
### SELECT из таблицы логов 

![Записи в таблице predictions](<image_for_readme/Pasted image 20260930170322.png>)
### port-forward:
1. Обычный интерфейс k9s:
![Интерфейс k9s](<image_for_readme/Pasted image 20260930171038.png>)

2. подключенный port:
![Подключённый порт](<image_for_readme/Pasted image 20260930171348.png>)
3. Команда для проверки работы kubernets:
``` bash
curl ‐X POST localhost:8080/v1/predict ‐H "Content‐Type: application/json" ‐d @test.json
```
![Ответ на запрос к модели](<image_for_readme/Pasted image 20260930171329.png>)

4. Показываю, что кластеры работают с командой выше
![Работа кластера](<image_for_readme/Pasted image 20260930171444.png>)

## Журнал ошибок:
1. Не запускалась команда "uv run pytest". Причиной этой ошибки было опечатка в pyproject.toml [dependecy-groups] место [dependency-groups]. Решение: просто убрал опечатку и "uv run pytest" заработал
2. Тесты останавливались на fixture 'client' not found , так как не было conftest.py. После его написания проверка на тестах заработала
3. Pod’ы оставались Pending, а также Ready = 0. Происходило, так как в deployment.yaml и service.yaml была указана старая версия mobile-service:1.0, заместо основной mobile-service:1.1
