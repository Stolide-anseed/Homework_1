# Домашнее задание 2

## 2.1 Пайплайн для своего сервисе:
1. [Зелённый прогон](https://github.com/Stolide-anseed/Homework_1/actions/runs/37466773600)
2. [Ссылка на страницу пакета образом](https://github.com/Stolide-anseed/Homework_1/pkgs/container/homework_1)

## 2.2 ветка и pull request
1. [Красный прогон](https://github.com/Stolide-anseed/Homework_1/actions/runs/37489970200)
2. [Зелённый прогон](https://github.com/Stolide-anseed/Homework_1/actions/runs/37490418906)

## 2.3 Три красных прогона с диагнозом
### 2.3.1 Configmap:
1. [Красный прогон](https://github.com/Stolide-anseed/Homework_1/actions/runs/37495859688) 
2. [Зелённый прогон](https://github.com/Stolide-anseed/Homework_1/actions/runs/37506632678) 
3. Чтобы найти данную поломку следует посмотреть job deploy(так как он и ломается). Ошибка выводится в этапе "сервис". Причину поломки показывается в этапе "диагностика", где вывелась ошибка "no such file or directory".
4. Под находятся в состояние "CrashLoopBackOff"

### 2.3.2 Secret
1. [Красный прогон](https://github.com/Stolide-anseed/Homework_1/actions/runs/37507756620) 
2. [Зелённый прогон](https://github.com/Stolide-anseed/Homework_1/actions/runs/37508652956) 
3. Красный job deploy. Ломается на шаге сервис. Решить данную проблему, не заглядывая в diff, можно, если обратить внимание в  "диагностике" и "подтягиваем секреты" по разному указаны секреты
4. Под находятся в состояние "CreateContainerConfigError"

### 2.3.3 Resources
1. [Красный прогон](https://github.com/Stolide-anseed/Homework_1/actions/runs/37511785785) 
2. [Зелённый прогон](https://github.com/Stolide-anseed/Homework_1/actions/runs/37512640281) 
3. Красный job deploy. Ломается на шаге сервер, и ошибку обнаружить можно в нём же. Посмотреть и обнаружить "Invalid value: '992...07': must be less"
4. Поды впринципе не создались

## 3 Вопросы:
1. Сравниваю [первый прогон](https://github.com/Stolide-anseed/Homework_1/actions/runs/37296875390/job/111720399671):1m 10s  [второй прогон](https://github.com/Stolide-anseed/Homework_1/actions/runs/37331864607/job/111837011384): 34s . Вот эти слои использовали кэш от первого прогона: COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv,  WORKDIR /app, COPY pyproject.toml uv.lock ./ , RUN uv sync --frozen --no-install-project. Pyproject.toml, uv.lock и предыдущие инструкции не изменились, поэтому Docker повторно использовал слой установки зависимостей.
2. Это Поды первой версии Deployment, созданные командой kubectl apply -f k8s/. В манифесте указан образ mobile-service:1.1, которого нет в свежем kind-кластере. Kubernetes пытается скачать его и получает ImagePullBackOff. Следующая команда kubectl set image заменяет образ на загруженный в кластер ghcr.io/…:sha-…. Deployment создаёт новые поды, дожидается их готовности и удаляет старые. Поэтому прогон и зелённый.
3. Путь пароля примерно такой: из GitHub secrets(Sercets and variables), CI его получает через ${{ secrets.DB_PASSWORD }} и передаёт в переменную, команда "kubectl create secret" записывает пароль в mobile-secrets, а уже поды PostgreSQL берёт ключ POSTGRES_PASSWORD из этого Secret. В КонфигМап хранить нельзя, так как предназначен для обычных и открытых настроек. Для хранения тайной информации можно использовать GitHub Secrets
4. Оснавная проблема такого сценария, то что не смотря на job tests, job build всё равно завершиться успешно. Что приведёт к выкату версии с ошибкой. Это самый не приятный сценарий
5. Отвечает вот эта строка "if: github.ref == 'refs/heads/main'", она не позволяет запускаться build and deploy вне ветки main. Сделана, так чтобы не загружать лишний раз второстепенные ветки и публиковать один главный образ на main
6. "pg_advisory_xact_lock" нужен, чтобы две реплики приложения не создавали таблицу одновременно. При запуске с пустой базой оба пода вызывают "init()", и без блокировки возможна гонка и ошибка создания таблицы. С блокировкой один под выполняет инициализацию, а второй ждёт завершения его транзакции
7. Порядок такой: Ресурсы -> Secrets -> Путь к модели. Так как в начале мы создаём образ(выделяется память) -> подтягиваем секреты -> и потом только запускаем smoke тест

## 4. Звёздочки:
### Ускорение:
1. Сравнение с кэшом и без:

|              | tests | build | deploy |
|--------------|-------|-------|--------|
| [без кэша](https://github.com/Stolide-anseed/Homework_1/actions/runs/37614783246/attempts/1) | 39 s  | 63 s  | 105 s  |
| [с кэшом](https://github.com/Stolide-anseed/Homework_1/actions/runs/37614783246)  | 35 s  | 21 s  | 114 s  |

Из таблицы можем заметить, что очень сильно ускорилась job'a build, благодоря использованию кэша. Job'ы deploy и tests отличаются из-за погрешности и на них видимо никак не повлиял наличия кэша

### Диагностика богаче


