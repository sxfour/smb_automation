# SMBAutoScanner + Masscan + PostgreSQL (новая версия с интеграцией) v2.1
![tumblr_d44e3aebf46e73976eec4d927268a961_ca96b743_500](https://github.com/sxfour/smb_automation/assets/112577182/92cc76ff-1144-4f88-8007-98ee0c659b56)
# Проверено на (Debian 11, Kali Linux)
- Используется масскан для 445 портов. Код считывает через пайп каждый сканируемый хост программы и отправляет SQL запрос на запись в бд.
- Создание двух SQL Запросов -> 1. Совместимый диалект - Папки на хосте (без проверки аутентификации) -> 2. Совместимый диалект - уязвимые папки на хосте (с успешной аутентификацией).
  
# Пример работы на удалённой машине
https://github.com/sxfour/smb_automation/assets/112577182/ede939d4-5599-45cd-8184-64e75d77b650

# Пример записей бд в pgAdmin4
https://github.com/sxfour/smb_automation/assets/112577182/e98f3004-dfe3-4698-ba93-c1f3c54e8570

# Установка Linux
Install packages with pip: -r requirements.txt
- pip install -r requirements.txt
  
# Smb_automation (старая версия)
Код предназначен для открытых самба протоколов, добавлен график для выявления тенденции работающих версий диалектов в виде bars, сопоставление этой информации поможет понять, какие версии работают в блоках хостов и на какие делать ориентир в первую очередь. На данный момент это один из первых проектов масс-сканирования, он является очень сырым, некоторые except логируются и большинство действий логируется для выявления ошибок.
Постараюсь обьяснить что для запуска вам понадобится:
- Работащий список (с 445 портами),в любом виде, для примера оставил в коде.

![изображение](https://user-images.githubusercontent.com/112577182/204134300-5fb1cb97-b4ff-44b8-8364-4f664d091d4e.png)

Этапы работы: 
1. Диалекты и график (1 поток). 
2. Дампы всех открытых папок на втором уровне вложенности(максимально возможное пространство потоков (1500), default). 
3. Дампы всех открытых папок первого уровня(максимально возможное пространство потоков (1500), default).
Важно!!! Количество работающих потоков напрямую зависит от кол-во хостов в списке адресов, файле и тд. Это стандартная настройка потоков.

- Проверено на Python 3.10
- Перед началом установите некоторые импорты (pysmb, smbprotocol, threading, uuid) это самые важные, остальные посмотрите в коде, в части import

![изображение](https://user-images.githubusercontent.com/112577182/204134738-f93fea6f-5e18-4ec1-ac9b-27813fa666ce.png)

- Запустить можем любым удобным способом, для примера (sh) python3 main.py  для Linux
- После запуска нажмите любую клавишу чтобы начать сканирование (3-step каждый этап Click enter)

Первый этап

![изображение](https://user-images.githubusercontent.com/112577182/204135005-0f9faaa7-11e1-43cf-99e4-b8f5af2601b8.png)

Как видите при успешном соединение, нам возвращается версия диалекта (числовой формат), если видимый протокол возвращает Not supported, начинается перебор всех версий диалектов в списке.
После первого этапа вам предложат создать фигуру. Click enter.

![изображение](https://user-images.githubusercontent.com/112577182/204135234-637c5d00-0002-4987-a21f-54847f5de6a1.png)

Тут видны все версии диалектов, количество активных хостов с версией самба. В зависимости от блоков адресов, диалекты заметно меняются. Это может быть вaжным при создание mass scan

- Закрываем фигуру, Click enter.

Второй этап

![изображение](https://user-images.githubusercontent.com/112577182/204135409-3f84b4ad-d7fa-4d8a-a4d8-3c3e84f8e6ea.png)

Модуль самба протокола попытается соединиться, при успешном соединении выдаст вложенные папки с файлами.
В качестве примера используются домен, имя, пароль (User)
Важно!!! При работе могут возникнуть ошибки, в основном при работе 2-3 этапа,это связано с взаимодействием протоколов и модуля, иногда они not supported, на данный момент это 5% ошибок при выводе результата, но надеюсь я их решу.
Click enter.

Третий этап

![изображение](https://user-images.githubusercontent.com/112577182/204143970-e8bd4e5a-94d1-4bcb-b838-5974ff8ab5ca.png)

Важно!!! Дождитесь окончания работы программы, она завершится сама, при больших нагрузках (большого количества адресов)
возможны долгие таймауты

После сканирование все результаты будут сохранены в папку output
