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
3. Чтобы найти данную поломку следует посмотреть job deploy(так как он и ломается). Ошибка выводится в этапе "сервис", но там не показывается настоящая причина поломки. Причину поломки удалось найти в этапе "диагностика", где вывелась ошибка "no such file or directory".
4. Под находятся в состояние "CrashLoopBackOff"

### 2.3.2 Secret
1. [Красный прогон](https://github.com/Stolide-anseed/Homework_1/actions/runs/37507756620) 
2. [Зелённый прогон](https://github.com/Stolide-anseed/Homework_1/actions/runs/37508652956) 
3. красный job deploy. Ломается на шаге сервис. Решить данную проблему, не заглядывая в diff, можно, если обратить внимание на в  "диагностике" и "подтягиваем секреты" по разному указаны секреты
4. Под находятся в состояние "CreateContainerConfigError"

### 2.3.3 Resources
1. [Красный прогон]() 
2. [Зелённый прогон]() 
3. Ломается на 

## 3 Вопросы:
1. 