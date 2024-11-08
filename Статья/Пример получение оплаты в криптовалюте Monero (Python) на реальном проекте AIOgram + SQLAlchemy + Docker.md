## Предисловие

Чтобы люди не платили комиссию и не ловили блокировки при использование различных сервисов вроде Cryptomus или другими платежными шлюзами, лучше установите свою ноду и не переживайте о блокировках и проблемах с выводом средств. Помните: "Не ваши ключи — не ваши монеты."

В этой статье будет показано, как создать простой проект и написать скрипт на Python для получения баланса и адреса, который можно интегрировать в свои проекты для приема криптовалюты на примере XMR (Monero). Далее будет рассмотрено, как реализовать вывод монет с кошелька. Вы можете использовать это в реальных разработках — всё зависит только от вас.

## Настройка среды и первый скрипт

Мы будем использовать библиотеку `monero`, которая управляет RPC (Remote Procedure Call) кошелька Monero, но сначала необходимо скачать `monero-wallet-rpc` с их [официального сайта](https://www.getmonero.org/ru/downloads/#cli).

После загрузки и распаковки папка должна выглядеть примерно так: ![[Pasted image 20241108022233.png]]
### Создание кошелька

Для начала понадобится `monero-wallet-cli`, чтобы создать кошелек. В этой же папке введите в командной строке `cmd`, чтобы открыть консоль.
![[Pasted image 20241108022249.png]]
И введите команду: 
```
monero-wallet-cli --generate-new-wallet=my_test_monero_wallet  --testnet
```

- `monero-wallet-cli` — используемая программа (CLI — это интерфейс командной строки).
- `--generate-new-wallet` — создаем новый кошелек с указанным названием файла.
- `--testnet` — указываем, что кошелек создается для тестовой сети.

После этого вас попросят задать и подтвердить пароль для кошелька — запомните или запишите его, иначе не сможете получить доступ к файлу. Однако еще важнее сохранить **сид-фразу** из 25 слов, так как с ее помощью можно восстановить все адреса и получить доступ к средствам даже без пароля от файла.

Рекомендуется выбирать **английский язык** для генерации сид-фразы, чтобы избежать проблем, связанных с поддержкой русского языка в системной консоли.

От майнинга отказываемся это нам не интересно на данном этапе.

Вот как у вас может выглядеть вывод: ![[Pasted image 20241108022326.png]]

В папке должны появится 2 файла в нашем случае это: my_test_monero_wallet и my_test_monero_wallet.keys: ![[Pasted image 20241108022338.png]]

Для просмотра и управления кошелька через cli можно использовать эту команду:
```
monero-wallet-cli --daemon-address testnet.xmr.ditatompel.com:443 --wallet-file my_test_monero_wallet --password password --testnet --trusted-daemon
```

### Запуск RPC

Вместо управления кошельком через CLI мы будем использовать RPC. Чтобы его запустить, выполните следующую команду:
```
monero-wallet-rpc --daemon-address testnet.xmr.ditatompel.com:443 --rpc-bind-port 18082 --wallet-file my_test_monero_wallet --password password --testnet
```
- `monero-wallet-rpc` — программа, поднимающая RPC-сервер.
- `--daemon-address` — адрес узла Monero (может быть публичным или локальным).
- `--rpc-bind-port` — порт для взаимодействия через код.
- `--wallet-file` — файл нашего кошелька.
- `--password` — пароль кошелька.
- `--testnet` — указывает, что подключаемся к тестовой сети.


Вот что у нас должна вывести консоль после этой команды. Если пишет нет подключения то проверьте точно ли вы подключаетесь с параметром `--testnet` к тестовой сети и наоборот, если подключаетесь к `mainnet` сети, то не нужно указывать параметр `--testnet`:
![[Pasted image 20241108022353.png]]

Если нода умерла можно наглулить другие ноды в монеро их 3 вида Mainnet, Stagenet, Testnet. Mainnet принято считать за настоящие монеты, все остальное фантики которые ничего не стоят потому что рассчитаны на тесты и разработку, поэтому монеты в них не имеют ценности

После того как мы подключились у нас должен был создаться файл и логином и паролем от RPC в моем случае это monero-wallet-rpc.18082.login
![[explorer_RxprMBc4TN 1.png]]


### Проверка работоспособности

Для проверки работоспособности можно использовать скрипт из [документации библиотеки](https://monero-python.readthedocs.io/en/latest/quickstart.html#)
Чтобы его запустить, создайте проект Python и виртуальное окружение. В командной строке выполните:
```
python -m venv venv
```
Активируйте виртуальное окружение:
```
.\venv\Scripts\activate
```
Установите библиотеку `monero`:
```
pip install monero 
```
Создайте файл `main.py` (Название может быть любое main обычно пишут для главного файла программы как точка входа) и вставьте следующий код:
```
from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet

w = Wallet(JSONRPCWallet(port=18082, user="monero",password="password"))

print(w.height())

print(w.address())

print(w.balance())
```
Запустите скрипт:
```
python main.py
```

На выходе вы получите текущую высоту блокчейна, ваш основной (нулевой) адрес и текущий баланс. ![[Pasted image 20241108022422.png]]

Если возникли какие-то проблемы, то проверьте password и username в файле, порт подключения, и установилась ли библиотека.

Если у вас получилось, то поздравляю мы можем использовать кошелек c помощью кода, можем приступать к созданию платежного шлюза.

### Подключение базы данных и Docker

Для начала мы должны понять что нам нужно, а именно создания и запоминания адресов, получение новых транзакций, для этого нам понадобится база данных для хранения этих записей мы будем использовать связку postgresslq + sqlalchime + docker.

[Docker](https://www.docker.com/) можно скачать и установить с официального сайта, как и [pgadmin](https://www.pgadmin.org/).

Создайте файл `docker-compose.yaml` для скачивания образа и поднятия нашей базы данных.
```
version: '3.8'

services:
  db:
    container_name: db
    image: postgres:latest
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    ports:
      - '5432:5432'
    volumes:
      - db-data:/var/lib/postgresql/data # Определение тома для PostgreSQL данных

volumes:
  db-data:
```
- `version: '3.8'`— задаёт версию синтаксиса Docker Compose.
- `services`— определяет контейнеры, которые будут запускаться.
- `db`— имя сервиса, используемое в сети Docker Compose.
- `image: postgres:latest` — указывает использовать образ PostgreSQL последней версии; можно также указать конкретную версию, например, `postgres:17.0`
- `container_name: db`— задаёт имя контейнера.
- `environment`— перечисляет переменные окружения для настройки PostgreSQL:
	- `POSTGRES_USER`— имя пользователя для базы данных.
	- `POSTGRES_PASSWORD`—  пароль для пользователя базы данных.
	- `POSTGRES_DB`— имя создаваемой базы данных.
- `ports`—  сопоставляет порт контейнера с портом хоста: первое значение — это порт внутри контейнера, по умолчанию у PostgreSQL это порт 5432; второе значение — выходной порт в нашу локальную сеть. Он может быть любым по вашему желанию, но если у вас несколько контейнеров, то нельзя использовать один и тот же порт одновременно в локальной сети.
- `volumes`—сохраняет данные контейнера в хостовой системе, чтобы избежать потерь при перезапуске контейнера.
- `postgres_data`—задаёт том для хранения данных базы данных.
### Запуск контейнера PostgreSQL

Убедитесь, что Docker запущен, затем в командной строке выполните:
```
docker compose -f docker-compose.yaml up -d
```

Если всё настроено правильно, Docker создаст и запустит контейнер. Вы увидите ваш контейнер в Docker Desktop или через команду `docker ps`. На выходе должно получится такая картинка о том что все успешно создалось и запустилось:
![[Pasted image 20241108022444.png]]А в самом докере вы увидите ваш контейнер ![[Pasted image 20241108022504.png]]
### Подключение к PostgreSQL через pgAdmin
Что бы проверить работоспособность можно использовать pgAdmin.
1. Откройте pgAdmin и добавьте новый сервер: **Register -> Server...**
2. Введите имя сервера и на вкладке **Connection** укажите параметры подключения: IP-адрес (localhost), порт (5432), имя базы данных (`postgres`), имя пользователя и пароль (`postgres`).
![[Pasted image 20241108022517.png]]
3. Нажмите **Save** для завершения подключения. Вы должны увидеть базу данных `postgres`, созданную в Docker Compose. 
![[Pasted image 20241108022536.png]]

## Настройка SQLAlchemy и Alembic для асинхронной работы с базой данных

Для подключения к базе данных и работы с миграциями установим необходимые библиотеки и инициализируем `alembic` и `sqlalchemy 2.0`  для работы в асинхронном режиме из их [cookbook](https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic )
### Установка библиотек

Активируйте виртуальное окружение и установите библиотеки:

```
.\venv\Scripts\activate
pip install alembic sqlalchemy
```
### Инициализация Alembic

Инициализируем Alembic:

```
alembic init -t async alembic
```

Эта команда создаст папку `alembic` с конфигурацией. Чтобы упростить версионирование, откройте файл `alembic.ini` и отредактируйте шаблон имен файлов ревизий:
```
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s
```

## Создание тестового Telegram-бота с помощью aiogram

Для взаимодействия с базой данных через бота установим нужные библиотеки:
```
pip install aiogram pydantic pydantic-settings asyncpg uuid
```

И проверим работа способность простым примером:
1. Создайте нового бота через @BotFather, выполните команды:
    - `/start`
    - `/newbot`
2. Придумайте имя и никнейм бота с указанием на конце _bot или bot, получите токен.
![[Pasted image 20241108022611.png]]

В сообщение берем токен и переходим на бота жмем в нашем боте `/start` и возвращаемся к коду.

Чтобы проверить, правильно ли установилась библиотека, можно использовать [пример эхо-бота с официального GitHub aiogram](https://github.com/aiogram/aiogram/blob/dev-3.x/examples/echo_bot.py).
![[Pasted image 20241107231758.png]]
### Создание бота с основными функциями

Для примера создадим бота, который записывает пользователей в базу данных и предлагает пять кнопок: `profile`, `back`, `deposit`, `withdraw`, `approve`.
### Структура проекта

Создадим следующую структуру папок :
- callbacks
- data
- filters 
- handlers 
- keyboards
- utils
И файлы с чтением наших настроек проекта:
- config_reader.py
- .env 
- bot.py
### Настройка файла `config_reader.py`
```
from pydantic_settings import BaseSettings, SettingsConfigDict  
from pydantic import SecretStr  
  
class Settings(BaseSettings):  
    bot_token: SecretStr  
    sqlalchemy_url: SecretStr  
    rpc_monero_login: SecretStr  
    rpc_monero_password: SecretStr  
    rpc_monero_port: SecretStr  
  
    model_config: SettingsConfigDict = SettingsConfigDict(  
        env_file=".env",  
        env_file_encoding="utf-8"  
    )  
  
config = Settings()
```

### Подключение к базе данных  и модели пользователя:
```
from datetime import datetime

  

from sqlalchemy.dialects.postgresql import UUID

import uuid

  
  

from sqlalchemy import BigInteger, Column, Integer, String, ForeignKey, Float, LargeBinary, Boolean, DateTime, Enum, \

    UniqueConstraint, CheckConstraint, Sequence, TypeDecorator

from sqlalchemy.types import ARRAY

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from sqlalchemy.orm import relationship, declarative_base

from enum import Enum as PyEnum

from config_reader import config

  
  
  

engine = create_async_engine(config.sqlalchemy_url.get_secret_value(), echo=True)

  

async_session = async_sessionmaker(engine)

Base = declarative_base()

  
  

class User(Base):

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tg_chat_id = Column(BigInteger, unique=True, index=True, nullable=False)

    username = Column(String(255), nullable=True)

    monero = Column(BigInteger, default=0, doc="Value of transaction input")

  
  
  

async def async_main():

    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)
```

## Настройка Alembic и создание ревизий

### Настройка файла `env.py`

1. В файле `env.py` на 24 строчке установите модели и добавьте подключение к базе данных:
```
from data.database import Base

target_metadata = Base.metadata

import config_reader

config.set_main_option("sqlalchemy.url", config_reader.config.sqlalchemy_url.get_secret_value())
```

2. Создайте первую ревизию базы данных, введя в консоли команду:
```
alembic revision --autogenerate -m "F start"
```

В базе данных появятся конфиги от Alembic с версиями и т.д. Для создания таблицы `users` необходимо перейти на последнюю ревизию базы данных:
```
alembic upgrade head
```

## Построение логики бота

### Настройка `bot.py`

Создайте файл `bot.py` со следующим содержимым:
```
import asyncio

import logging

import sys

  

from aiogram import Bot, Dispatcher

from aiogram.client.default import DefaultBotProperties

  

from config_reader import config

  

from handlers import user_commands

  

async def main() -> None:

  # Initialize Bot instance with a default parse mode which will be passed to all API calls

  bot = Bot(config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode="HTML"))

  # All handlers should be attached to the Router (or Dispatcher)

  dp = Dispatcher()

  dp.include_routers(user_commands.router,

                    )

  await bot.delete_webhook(drop_pending_updates=True)

  # And the run events dispatching

  await dp.start_polling(bot)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # Получаем event loop

    loop = asyncio.get_event_loop()

    # Запускаем main()

    loop.run_until_complete(main())
```
### Настройка `user_commands.py`

Создайте файл `user_commands.py` в папке `handlers` для обработки команд пользователя:

```
from aiogram import Router, F

from aiogram.types import Message, CallbackQuery

from aiogram.filters import CommandStart

from aiogram.utils.markdown import hbold

  

from data.requests import add_user

  

from keyboards.main_menu import main_menu

  

router = Router()

  
  

@router.message(CommandStart())

@router.callback_query(F.data == "main_menu")

async def cmd_start(message: Message | CallbackQuery):

    print(message.from_user.id)

    ss = await add_user(tg_chat_id=message.from_user.id, username=message.from_user.username)

    print(ss)

    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=main_menu)
```


## Работа с базой данных

### Функции для работы с пользователями в `requests.py`

Создайте файл `requests.py` в папке `data`, который будет содержать функции для добавления пользователя и получения баланса пользователя:
```
from data.database import User, async_session

from sqlalchemy import select, and_

  

async def add_user(tg_chat_id, username):

    async with async_session() as session:

        try:

            # Проверяем, существует ли пользователь с заданным tg_chat_id

            existing_user = await session.execute(select(User).where(User.tg_chat_id == tg_chat_id))

            user = existing_user.scalar_one_or_none()

  

            if user is None:

                new_user = User(tg_chat_id=tg_chat_id, username=username)

                session.add(new_user)

                await session.commit()

                return "Пользователь добавлен в базу данных"

            else:

                # Если пользователь существует, обновляем его username

                if user.username != username:

                    user.username = username

                    await session.commit()

                    return "Имя пользователя обновлено"

                else:

                    return "Пользователь уже существует в базе данных"

        except Exception as err:

            print(err)

  
  

async def get_user_balance_monero(tg_chat_id) -> float | None:

    async with async_session() as session:

        try:

            user = await session.execute(select(User).where(User.tg_chat_id == tg_chat_id))

            user = user.scalar_one_or_none()

            if user:

                return user.monero  # возвращает баланс Monero пользователя, замените на нужное поле

            else:

                return None  # если пользователь не найден

        except Exception as err:

            print(err)
```

## Создание инлайн-клавиатур в `keyboards/inline.py`
```
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup  
from aiogram.utils.keyboard import InlineKeyboardBuilder  
  
  
  
main_menu_ikb = InlineKeyboardMarkup(  
    inline_keyboard=[  
        [  
            InlineKeyboardButton(text=f"Wallet", callback_data="wallet"),  
        ],  
    ])  
  
  
  
wallet_ikb = InlineKeyboardMarkup(  
    inline_keyboard=[  
        [  
            InlineKeyboardButton(text=f"Пополнить", callback_data="deposit"),  
            InlineKeyboardButton(text=f"Вывести", callback_data="withdraw"),  
        ],  
        [  
            InlineKeyboardButton(text=f"Адресная книга", callback_data="address_book"),  
        ],  
        [  
            InlineKeyboardButton(text=f"Коммисии и лимиты", callback_data="commissions_and_limits"),  
        ],  
        [  
            InlineKeyboardButton(text=f"Назад", callback_data="main_menu"),  
        ]  
    ])  
  
deposit_ikb = InlineKeyboardMarkup(  
    inline_keyboard=[  
        [  
            InlineKeyboardButton(text=f"Назад", callback_data="wallet"),  
        ]  
    ])
```


## Обработка навигации в `callbacks/navigation.py`

Создайте файл `navigation.py` для обработки callback-команд:
```
from aiogram import Router, F

from aiogram.types import CallbackQuery

from data.requests import get_user_balance_monero

  
  

router = Router()

  
  

@router.callback_query(F.data == "wallet")

async def wallet(call: CallbackQuery):

    balance = await get_user_balance_monero(call.from_user.id)

    print(balance)

    await call.message.edit_text(f"Ваш баланс {balance}")
```

## Получение Monero монет для тестов и тестирование RPC

Чтобы протестировать команды и подключение, нам понадобится немного тестовых токенов Monero. Найдите в интернете "faucet testnet xmr", выберите сайт, введите адрес вашего кошелька, пройдите капчу и нажмите "Submit". Пример сайта: ![[Pasted image 20241107234858.png]]

## Тестирование команд Monero с помощью RPC

В `main.py` протестируйте команды, чтобы определить, какие из них потребуются для бота:
```
from monero.wallet import Wallet  
from monero.backends.jsonrpc import JSONRPCWallet  
  
w = Wallet(JSONRPCWallet(port=18082, user="monero",password="i841csLc5BycblOwz4v3qA=="))  
  
print("Height: ", w.height())  
  
print("Address: ", w.address())  
  
print("balance: ", w.balance())  
  
# print(w.new_address())  
# print(w.addresses())  
# print(w.accounts[0].address())  
# print(w.accounts[0].new_address())  
# print(w.accounts[0].addresses())  
  
incomings = w.accounts[0].incoming(min_height=2615765)  
print(incomings)  
for incoming in incomings:  
    print(incoming.transaction.hash)  
    print(incoming.transaction.height)  
    print(incoming.amount)  
    print(incoming.local_address)
```

Разберем, что делают эти команды и зачем они нужны:

- **JSONRPCWallet** — это подключение к RPC. Параметры метода подключения:
    
    - `protocol` — http или https;
    - `timeout` — таймаут ожидания подключения;
    - `verify_ssl_certs` — подтверждение SSL-сертификатов при запросе;
    - `proxy_url` — возможность использования прокси;
    - `path` — роутер, на котором размещено API (по умолчанию `"/json_rpc"`).
    
    Основные интересующие нас параметры:
    
    - `host: str = "127.0.0.1"` — адрес подключения;
    - `port: int = 18088` — порт подключения;
    - `user: str = ""` — имя пользователя RPC;
    - `password: str = ""` — пароль RPC.
- **Wallet** — это класс, облегчающий использование типов и функций библиотеки, таких как транзакции, их создание и другие возможности.
    

Команды:

- `w.height()` — возвращает текущую высоту цепочки транзакций, что соответствует количеству уже записанных блоков.
- `w.address()` — возвращает главный адрес кошелька первого аккаунта.
- `w.balance()` — показывает общий баланс кошельков.

Кошелек Monero может содержать несколько аккаунтов и субадресов. В коде `w.accounts[0]`, `w.accounts[1]` и т.д. — это аккаунты кошелька. Удобнее использовать только нулевой аккаунт и его субадреса, если это, например, магазин или сервис, так как проверять нужно меньше кошельков. Однако, если это платформа, лучше выделить для каждого пользователя отдельный аккаунт, чтобы он мог проводить `sweep_account` (полное опустошение кошелька с учетом комиссии). Это также предотвратит блокировку средств между аккаунтами при переводах, что иногда случается с субадресами одного аккаунта.

- `w.accounts[0].new_address()` — создает новый субадрес для заданного аккаунта.
- `w.accounts[0].addresses()` — возвращает все субадреса аккаунта.
- `w.accounts[0].incoming(min_height=2615765)` — показывает все входящие транзакции для аккаунта, начиная с указанной высоты.

Атрибуты входящей транзакции:

- `incoming.transaction.hash` — хеш транзакции.
- `incoming.transaction.height` — высота транзакции.
- `incoming.amount` — сумма монет в транзакции.
- `incoming.local_address` — локальный адрес кошелька (адрес RPC), на который поступили средства.

### Адаптируем наши модели под необходимые параметры:
```
from sqlalchemy.dialects.postgresql import UUID  
import uuid  
  
from sqlalchemy import BigInteger, Integer, String, ForeignKey, Float, Boolean  
  
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker  
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column  
  
from config_reader import config  
  
engine = create_async_engine(config.sqlalchemy_url.get_secret_value(), echo=True)  
async_session = async_sessionmaker(engine)  
Base = declarative_base()  
  
  
class User(Base):  
    __tablename__ = "users"  
  
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  
    tg_chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)  
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)  
  
    monero_balance: Mapped[float] = mapped_column(Float, default=0, doc="Value of transaction input")  
    monero_addresses: Mapped[list["MoneroAddress"]] = relationship(back_populates="user", uselist=True)  
  
    monero_deposit_transaction: Mapped[list["MoneroDepositTransaction"]] = relationship(back_populates="user", uselist=True)  
    monero_withdraw_transaction: Mapped[list["MoneroWithdrawTransaction"]] = relationship(back_populates="user", uselist=True)  
  
  
class MoneroAddress(Base):  
    __tablename__ = "monero_address"  
  
    id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, primary_key=True)  
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))  
    user: Mapped["User"] = relationship(back_populates="monero_addresses", uselist=False)  
    address: Mapped[str] = mapped_column(String(100))  
    used: Mapped[bool] = mapped_column(Boolean, default=False)  
  
  
class MoneroDepositTransaction(Base):  
    __tablename__ = "monero_deposit_transaction"  
  
    id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, primary_key=True)  
    tx_hash: Mapped[str] = mapped_column(String(300), nullable=False)  
    amount: Mapped[float] = mapped_column(Float, nullable=False)  
    address_in: Mapped[str] = mapped_column(String(100))  
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))  
    user: Mapped["User"] = relationship(back_populates="monero_deposit_transaction", uselist=False)  
    height: Mapped[int] = mapped_column(BigInteger, nullable=False)  
  
  
class MoneroWithdrawTransaction(Base):  
    __tablename__ = "monero_withdraw_transaction"  
  
    id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, primary_key=True)  
    tx_hash: Mapped[str] = mapped_column(String(300), nullable=False)  
    amount: Mapped[float] = mapped_column(Float, nullable=False)  
    address_to: Mapped[str] = mapped_column(String(100))  
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))  
    user: Mapped["User"] = relationship(back_populates="monero_withdraw_transaction", uselist=False)  
  
  
async def async_main():  
    async with engine.begin() as conn:  
        await conn.run_sync(Base.metadata.create_all)
```
- В таблице `users` поле `monero_balance` имеет тип `float`, так как библиотека возвращает баланс не в минимальных атомарных единицах Monero, а в значении типа `float`. Установлено отношение «один ко многим» для быстрого получения адресов и транзакций каждого пользователя, если потребуется их отображение.
    
- В таблице `monero_address` добавлена колонка `used` типа `bool`. Следуя принципам безопасности Monero, для каждой транзакции используется уникальный субадрес, поэтому важно отслеживать, какой адрес уже использовался, и создавать новый при необходимости.
    
- В таблице `monero_deposit_transaction` указано только поле `address_in` — наш адрес, на который пришли средства, так как отправитель не отображается. Поле `height` помогает получать новые транзакции.
    
- В таблице `monero_withdraw_transaction` добавлено только поле `address_to`, чтобы отслеживать, куда были отправлены средства, источник вывода нам не требуется, поскольку он не отображается, если транзакция собирается автоматически.

Для обновления структуры базы данных выполним команды Alembic:
```
alembic revision --autogenerate -m "add monero db"
alembic upgrade head
```

После этого появится новая ревизия, и база данных будет обновлена. Изменения можно проверить через pgAdmin4.

### Инициализация кошелька и создание обработчиков

Добавим инициализацию кошелька и несколько функций в `data/requests.py`:
```
from monero.backends.jsonrpc import JSONRPCWallet  
from monero.wallet import Wallet

monero_rpc = Wallet(JSONRPCWallet(port=config.rpc_monero_port.get_secret_value(), user=config.rpc_monero_login.get_secret_value(), password=config.rpc_monero_password.get_secret_value()))
```

Не забываем что все данные переменные окружения передаются через менеджер конфигурации например, `pydantic_settings` или `python-dotenv`.
### Функция для получения актуального субадреса

Создадим функцию для получения (или создания) нового неиспользованного субадреса для пользователя:
```
async def get_address_monero(tg_chat_id):  
    async with async_session() as session:  
        try:  
            user = await session.execute(select(User).where(User.tg_chat_id == tg_chat_id))  
            user = user.scalar_one_or_none()  
            user_address = await session.execute(select(MoneroAddress).where(and_(MoneroAddress.user_id == user.id, MoneroAddress.used == False)))  
            user_address = user_address.scalars().first()  
            print(user_address)  
            if user_address:  
                return user_address.address  
            else:  
                user_address, sub_address_id = monero_rpc.accounts[0].new_address()  
                new_address = MoneroAddress(id=sub_address_id, user_id=user.id, address=str(user_address), used=False)  
                session.add(new_address)  
                await session.commit()  
                return user_address  
  
        except Exception as err:  
            print(err)
```

### Объяснение
`user = await session.execute(select(User).where(User.tg_chat_id == tg_chat_id))` — получаем текущего пользователя или подтверждаем его отсутствие. Можно добавить проверку на None. В select указывается модель, where должно указываться поле для сравнения и переменная, с которой сравниваем. session.execute — выполнение запроса.

`user = user.scalar_one_or_none()` — нужно для того, чтобы нормализовать данные для обращения с ними: одно значение или отсутствие данных.

`user_address = await session.execute(select(MoneroAddress).where(and_(MoneroAddress.user_id == user.id, MoneroAddress.used == False)))` — пробуем найти неиспользованный субадрес Monero у пользователя. Для этого используем and_, чтобы указать сразу несколько параметров.

`user_address = user_address.scalars().first()` — нормализация множества данных и берём первое попавшееся.

Далее проверяем, есть ли подходящий адрес. Если значение не найдено (оно будет None), нам нужно будет создать новый субадрес.

`user_address, sub_address_id = monero_rpc.accounts[0].new_address()` — возвращаются сразу 2 значения, и мы можем привязать sub_address_id к нашей таблице, если нам понадобится использовать адрес по номеру из кошелька в RPC.

`new_address = MoneroAddress(id=sub_address_id, user_id=user.id, address=str(user_address), used=False)` — создаём объект нового адреса.

`session.add(new_address)` — отправляем на добавление.

`await session.commit()` — коммитим в базу, то есть попытка отправки.

В итоге получаем такой файл:
```
from monero.backends.jsonrpc import JSONRPCWallet  
from monero.wallet import Wallet  
  
from config_reader import config  
from data.database import User, async_session, MoneroAddress, MoneroDepositTransaction  
from sqlalchemy import select, and_, func  
  
monero_rpc = Wallet(JSONRPCWallet(port=config.rpc_monero_port.get_secret_value(), user=config.rpc_monero_login.get_secret_value(), password=config.rpc_monero_password.get_secret_value()))  
  
async def add_user(tg_chat_id, username):  
    async with async_session() as session:  
        try:  
            # Проверяем, существует ли пользователь с заданным tg_chat_id  
            existing_user = await session.execute(select(User).where(User.tg_chat_id == tg_chat_id))  
            user = existing_user.scalar_one_or_none()  
  
            if user is None:  
                new_user = User(tg_chat_id=tg_chat_id, username=username)  
                session.add(new_user)  
                await session.commit()  
                return "Пользователь добавлен в базу данных"  
            else:  
                # Если пользователь существует, обновляем его username  
                if user.username != username:  
                    user.username = username  
                    await session.commit()  
                    return "Имя пользователя обновлено"  
                else:  
                    return "Пользователь уже существует в базе данных"  
        except Exception as err:  
            print(err)  
  
  
async def get_user_balance_monero(tg_chat_id) -> float | None:  
    async with async_session() as session:  
        try:  
            user = await session.execute(select(User).where(User.tg_chat_id == tg_chat_id))  
            user = user.scalar_one_or_none()  
            if user:  
                return user.monero_balance  # возвращает баланс Monero пользователя, замените на нужное поле  
            else:  
                return None  # если пользователь не найден  
        except Exception as err:  
            print(err)  
  
  
async def get_address_monero(tg_chat_id):  
    async with async_session() as session:  
        try:  
            user = await session.execute(select(User).where(User.tg_chat_id == tg_chat_id))  
            user = user.scalar_one_or_none()  
            user_address = await session.execute(select(MoneroAddress).where(and_(MoneroAddress.user_id == user.id, MoneroAddress.used == False)))  
            user_address = user_address.scalars().first()  
            if user_address:  
                return user_address.address  
            else:  
                user_address, sub_address_id = monero_rpc.accounts[0].new_address()  
                new_address = MoneroAddress(id=sub_address_id, user_id=user.id, address=str(user_address), used=False)  
                session.add(new_address)  
                await session.commit()  
                return user_address  
  
        except Exception as err:  
            print(err)
```

Мы модифицируем файл `handler.py`:
```
from aiogram import Router, F  
from aiogram.types import Message, CallbackQuery  
from aiogram.filters import CommandStart  
from aiogram.utils.markdown import hbold  
  
from data.requests import add_user  
  
from keyboards.inline import main_menu_ikb  
  
router = Router()  
  
  
@router.message(CommandStart())  
@router.callback_query(F.data == "main_menu")  
async def cmd_start(message: Message | CallbackQuery):  
    await add_user(tg_chat_id=message.from_user.id, username=message.from_user.username)  
    text = f"Hello, {hbold(message.from_user.full_name)}!"  
  
    if isinstance(message, CallbackQuery):  
        await message.message.edit_text(text, reply_markup=main_menu_ikb)  
        await message.answer()  
    else:  
        await message.answer(text, reply_markup=main_menu_ikb)
```

В функции мы указываем параметры `Message` и `CallbackQuery` для корректной работы клавиатуры при выполнении команды `/start` и нажатии на кнопку "main_menu" в клавиатуре. Через проверку `if isinstance(message, CallbackQuery)` создаем два разных варианта ответа.

В файле `callbacks/navigation.py` добавляем обработку пути для `deposit` и используем нашу функцию:
```
from aiogram import Router, F  
from aiogram.types import CallbackQuery  
from data.requests import get_user_balance_monero, get_address_monero  
from keyboards.inline import wallet_ikb, deposit_ikb  
  
router = Router()  
  
  
@router.callback_query(F.data == "wallet")  
async def wallet(call: CallbackQuery):  
    balance_monero = await get_user_balance_monero(call.from_user.id)  
    print(balance_monero)  
    await call.message.edit_text(f"Ваш баланс: {balance_monero}", reply_markup=wallet_ikb)  
  
  
@router.callback_query(F.data == "deposit")  
async def deposit(call: CallbackQuery):  
    address = await get_address_monero(call.from_user.id)  
    await call.message.edit_text(f"Ваш address: {address}", reply_markup=deposit_ikb)
```
Теперь можно запускать и проверять: получение баланса из базы данных работает, также работает получение адреса пользователя. ![[pgAdmin4_hooHKuiOyV.png]]

Далее создаем функцию `get_new_deposit_monero` в `data/requests.py`, чтобы начать прием транзакций:
```
async def get_new_deposit_monero():  
    async with async_session() as session:  
        try:   
            query = select(func.max(MoneroDepositTransaction.height))  
            result = await session.execute(query)  
            highest_height = result.scalar_one_or_none() or 0
  
            incomings = monero_rpc.accounts[0].incoming(min_height=highest_height)  
            for incoming in incomings:  
                hash = incoming.transaction.hash  
                height = incoming.transaction.height  
                amount = incoming.amount  
                address = str(incoming.local_address)  
  
                 
                result = await session.execute(select(MoneroDepositTransaction).where(MoneroDepositTransaction.tx_hash == hash))  
                double_check = result.scalar_one_or_none()  
  
                if double_check is None:  
                    result = await session.execute(  
                        select(MoneroAddress).where(MoneroAddress.address == address)  
                    )  
                    user_address = result.scalar_one_or_none()  
  
                    if user_address is None:   
                        continue  
  
                   
                    tx = MoneroDepositTransaction(  
                        tx_hash=hash,  
                        amount=amount,  
                        height=height,  
                        user_id=user_address.user_id,  
                        address_in=user_address.address  
                    )  
                    session.add(tx)  
  
                    result = await session.execute(  
                        select(User).where(User.id == user_address.user_id)  
                    )  
                    user = result.scalar_one_or_none()  
  
                    if user:  
                        user.monero_balance += float(amount)  
  
                    await session.commit()  
  
        except Exception as err:  
            print(err)
```

Для начала мы должны получить максимально значения высоты из сохранённых (еще нет, но будут) нами транзакций или установка в нулевое положение:
`query = select(func.max(MoneroDepositTransaction.height))`
`func.max` — это SQLAlchemy функция для получения максимального значения по таблице.


`incomings = monero_rpc.accounts[0].incoming(min_height=highest_height)` - Получаем весь список транзакции от этого уровня


`for incoming in incomings:` - Так как это список (list), мы будем использовать цикл для его обработки. Далее проверяем, есть ли уже такая транзакция. Если нет, то проверяем наличие адреса в нашей БД у пользователей и получаем id пользователя. Если нету в БД, можно обработать как донат или как-то по-другому фильтровать. Создаём объект транзакции, добавляем и прибавляем баланс пользователю, только в конце делаем `await session.commit()`, чтобы если случится ошибка, она не закоммитилась в БД только часть данных без обработки.

Далее нам надо это как-то использовать в фоне, для этого есть библиотека apscheduler, давайте добавим его в `bot.py`:

- `scheduler = AsyncIOScheduler()` - объявления его  
- `scheduler.add_job(get_new_deposit_monero, trigger="interval", seconds=60)` - для добавления задачи в работу используем нашу функцию `get_new_deposit_monero`
- `trigger="interval"` - это значит с помощью интервала каждые seconds=60
- `scheduler.start()` - стартует задачу

```
import asyncio  
import logging  
import sys  
  
from aiogram import Bot, Dispatcher  
from aiogram.client.default import DefaultBotProperties  
  
from config_reader import config  
from data.requests import get_new_deposit_monero  
  
from handlers import user_commands  
from callbacks import navigation  
from apscheduler.schedulers.asyncio import AsyncIOScheduler  
  
async def main() -> None:  
    # Initialize Bot instance with a default parse mode which will be passed to all API calls  
  
    bot = Bot(config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode="HTML"))  
    # All handlers should be attached to the Router (or Dispatcher)  
    dp = Dispatcher()  
    scheduler = AsyncIOScheduler()  
  
    scheduler.add_job(get_new_deposit_monero, trigger="interval", seconds=60)  
    scheduler.start()  
    dp.include_routers(user_commands.router,  
                       navigation.router,  
                       )  
    await bot.delete_webhook(drop_pending_updates=True)  
    # And the run events dispatching  
    await dp.start_polling(bot)  
  
  
if __name__ == "__main__":  
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)  
    # Получаем event loop  
    loop = asyncio.get_event_loop()  
    # Устанавливаем asyncio event loop для apscheduler  
    scheduler = AsyncIOScheduler()  
    scheduler.configure(loop=loop)  
    # Запускаем main()  
    loop.run_until_complete(main())
```


Можно запускать проверку балансов пользователей, пополняются, все работает. Далее переделаем проект для множества аккаунтов Monero, ведь это требуется в моем проекте. Если вам это не нужно, то далее можно сделать автовывод средств или что-то еще, что придумаете. Платежка готова.

## Переделка под множество аккаунтов Monero

Начнем с базы данных. Поэтому обновляем модели в папке `data`, файл `database.py`.

Добавляем столбцы `monero_account_id` и `monero_zero_address` в таблицу `users`:
```
class User(Base):  
    __tablename__ = "users"  
  
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  
    tg_chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)  
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)  
  
    monero_account_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)  
    monero_zero_address: Mapped[str] = mapped_column(String(95), nullable=True)  
    monero_addresses: Mapped[list["MoneroAddress"]] = relationship(back_populates="user", uselist=True)  
    monero_balance: Mapped[float] = mapped_column(Float, default=0, doc="Value of transaction input")  
    monero_deposit_transaction: Mapped[list["MoneroDepositTransaction"]] = relationship(back_populates="user", uselist=True)  
    monero_withdraw_transaction: Mapped[list["MoneroWithdrawTransaction"]] = relationship(back_populates="user", uselist=True)
```
В таблице `monero_address` добавляем `account_id` и `sub_address_id`:
```
class MoneroAddress(Base):  
    __tablename__ = "monero_address"  
  
    id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, primary_key=True)  
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))  
    user: Mapped["User"] = relationship(back_populates="monero_addresses", uselist=False)  
    address: Mapped[str] = mapped_column(String(95), nullable=False)  
    used: Mapped[bool] = mapped_column(Boolean, default=False)  
    account_id: Mapped[int] = mapped_column(Integer, nullable=False)  
    sub_address_id: Mapped[int] = mapped_column(Integer, nullable=False)
```
В таблице `monero_deposit_transaction` добавляем `account_id`:
```
class MoneroDepositTransaction(Base):  
    __tablename__ = "monero_deposit_transaction"  
  
    id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, primary_key=True)  
    tx_hash: Mapped[str] = mapped_column(String(300), nullable=False)  
    amount: Mapped[float] = mapped_column(Float, nullable=False)  
    address_in: Mapped[str] = mapped_column(String(95))  
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))  
    user: Mapped["User"] = relationship(back_populates="monero_deposit_transaction", uselist=False)  
    height: Mapped[int] = mapped_column(BigInteger, nullable=False)  
  
    account_id: Mapped[int] = mapped_column(Integer, nullable=False)
```
В таблице `monero_withdraw_transaction` добавляем `account_id`, `service_transfer_fee`, `network_transfer_fee`:
```
class MoneroWithdrawTransaction(Base):  
    __tablename__ = "monero_withdraw_transaction"  
  
    id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, primary_key=True)  
    tx_hash: Mapped[str] = mapped_column(String(300), nullable=False)  
    amount: Mapped[float] = mapped_column(Float, nullable=False)  
    address_to: Mapped[str] = mapped_column(String(95))  
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))  
    user: Mapped["User"] = relationship(back_populates="monero_withdraw_transaction", uselist=False)  
  
    account_id: Mapped[int] = mapped_column(Integer, nullable=False)  
    service_transfer_fee: Mapped[float] = mapped_column(Float, nullable=False)  
    network_transfer_fee: Mapped[float] = mapped_column(Float, nullable=False)
```

`service_transfer_fee` и `network_transfer_fee` могут нам понадобиться для накрутки нашей комиссии и отслеживания комиссии сети.

Далее изменяем наши ручки запросов в папке `data`, файл `requests.py`. Изменяем добавление пользователя в функции `add_user`:
```
async def add_user(tg_chat_id, username):

    async with async_session() as session:

        try:

            existing_user = await session.execute(select(User).where(User.tg_chat_id == tg_chat_id))

            user = existing_user.scalar_one_or_none()

  

            if user is None:

                new_user = User(tg_chat_id=tg_chat_id, username=username)

                session.add(new_user)

                await session.flush()

                new_monero_account_user = monero_rpc.new_account(label=str(new_user.id))

                new_user.monero_account_id = int(new_monero_account_user.index)

                new_user.monero_zero_address = str(new_monero_account_user.address())

                new_address = MoneroAddress(account_id=new_monero_account_user.index, sub_address_id=0, user_id=new_user.id, address=str(new_monero_account_user.address()), used=False)

                session.add(new_address)

                await session.commit()

                return "Пользователь добавлен в базу данных"

            else:

                if user.username != username:

                    user.username = username

                    await session.commit()

                    return "Имя пользователя обновлено"

                else:

                    return "Пользователь уже существует в базе данных"

        except Exception as err:

            print(err)
```

Мы все так же создаем пользователя, но добавляем его в самом начале в сессию и используем `await session.flush()`, чтобы получить сгенерированные данные, такие как UUID для столбца `id` в таблице пользователя. Это необходимо, чтобы использовать его для установки `label` в кошельке и пометить адрес в кошельке.
`new_monero_account_user = monero_rpc.new_account(label=str(new_user.id))`
Затем добавляем пользователю `monero_account_id` и `monero_zero_address`, создаем новую запись в таблице `MoneroAddress` и коммитим изменения в базу данных:

Теперь, касаемо функции `get_address_monero`, это будет функция для получения адреса Monero, которую вы можете использовать для получения информации о кошельке или адресах пользователя:
```
async def get_address_monero(tg_chat_id):  
    async with async_session() as session:  
        try:  
            user = await session.execute(select(User).where(User.tg_chat_id == tg_chat_id))  
            user = user.scalar_one_or_none()  
            user_address = await session.execute(select(MoneroAddress).where(and_(MoneroAddress.user_id == user.id, MoneroAddress.used == False)))  
            user_address = user_address.scalars().first()  
            if user_address:  
                return user_address.address  
            else:  
                user_address, sub_address_id = monero_rpc.accounts[user.monero_account_id].new_address(label=str(user.id))  
                new_address = MoneroAddress(account_id=user.monero_account_id, sub_address_id=sub_address_id, user_id=user.id, address=str(user_address), used=False)  
                session.add(new_address)  
                await session.commit()  
                return user_address  
  
        except Exception as err:  
            print(err)
```
Мы изменили способ получения адреса:
```
user_address, sub_address_id = monero_rpc.accounts[user.monero_account_id].new_address(label=str(user.id))
```
Также была доработана функция получения новых транзакций:
```
async def get_new_deposit_monero():  
    async with async_session() as session:  
        try:  
            query = select(func.max(MoneroDepositTransaction.height))  
            result = await session.execute(query)  
            highest_height = result.scalar_one_or_none() or 0  # Если None, то присваиваем 0  
            current_height = monero_rpc.height  
            num_accounts = len(monero_rpc.accounts)  
            for account_index in range(num_accounts):  
                incomings = monero_rpc.accounts[account_index].incoming(min_height=highest_height)  
                for incoming in incomings:  
                    hash = incoming.transaction.hash  
                    height = incoming.transaction.height  
                    amount = incoming.amount  
                    address = str(incoming.local_address)  
  
                    confirmations = incoming.transaction.confirmations  
                    if confirmations < 10:  
                        continue  
  
                    result = await session.execute(  
                        select(MoneroDepositTransaction).where(MoneroDepositTransaction.tx_hash == hash)  
                    )  
                    double_check = result.scalar_one_or_none()  
  
                    if double_check is None:  
                        result = await session.execute(  
                            select(MoneroAddress).where(MoneroAddress.address == address)  
                        )  
                        user_address = result.scalar_one_or_none()   
  
                        if user_address is not None:    
                            tx = MoneroDepositTransaction(  
                                tx_hash=hash,  
                                amount=amount,  
                                height=height,  
                                user_id=user_address.user_id,  
                                address_in=user_address.address,  
                                account_id=account_index  
                            )  
                            session.add(tx)  
  
                            result = await session.execute(  
                                select(User).where(User.id == user_address.user_id)  
                            )  
                            user = result.scalar_one_or_none()  
  
                            if user:  
                                user.monero_balance += float(amount)  
                                user_address.used = True  
                            await session.commit()  
  
        except Exception as err:  
            print(err)
```
Чтобы получить количество аккаунтов Monero, мы обращаемся к RPC и используем стандартную функцию подсчета `len`, так как нам возвращаются объекты:
`num_accounts = len(monero_rpc.accounts)`
Делаем это число последовательным списком и создаем цикл. Получаем входящие транзакции, обращаясь к каждому аккаунту через этот список с помощью переменной `account_index`:
`incomings = monero_rpc.accounts[account_index].incoming(min_height=highest_height)`,
Далее добавились только поля в `MoneroDepositTransaction`. Была добавлена проверка на 10 подтверждений (обще принятое количество для разблокировки), чтобы пользователи не могли использовать монеты, которые не разблокированы.

Запускаем и можем проверять, что все работает: транзакции добавляются к нам в базу.  ![[Pasted image 20241108013136.png]]

# Отправка транзакций
Следующее, к чему можно приступить, — это вывод средств. Для этого нам понадобится свой демон, чтобы делать broadcast (отправлять транзакции в блокчейн). Нам нужен `monerod`, он поддерживает синхронизацию с блокчейном Monero через P2P-сеть и подтверждает его правильность. Лучше всего использовать собственный полный узел для бизнеса, но так как мы только разрабатываем, можно воспользоваться обрезанной, несинхронизированной нодой в тестнете, чтобы не перегружать жесткий диск. Открываем CMD и используем следующую команду для запуска:
```
monerod.exe --testnet --prune-blockchain --bootstrap-daemon-address auto --no-sync
```
- `monerod.exe` — утилита демон
- `--testnet` — тестовая сеть Monero с фантиками
- `--prune-blockchain` — означает, что 2/3 блокчейна будет отрезано после скачивания, если не хотите хранить полный блокчейн после синхронизации
- `--no-sync` — обозначает, что мы не будем качать блокчейн вообще
- `--bootstrap-daemon-address auto` — разрешает использовать начальный узел синхронизации и перенаправлять RPC-запросы, кошелёк будет обрабатывать их автоматически, т.е. сможем использовать кошелек без синхронизации нашей ноды

В реальном проекте не рекомендуется применять `no-sync` и `bootstrap-daemon-address`, но если очень нужно, то такая возможность есть.

Далее создадим роутер и добавим в бота FSM State из aiogram для того, чтобы сделать состояния ожидания ввода пользователем для заполнения полей формы на вывод. В папке `utils` создаем файл `states.py` и объявляем класс, группу состояний, назовем как для формы поля и кнопки:
```
from aiogram.fsm.state import StatesGroup, State  
  
  
class WithdrawForm(StatesGroup):  
    address = State()  
    amount = State()  
    approve = State()  
  
    withdraw_fee = State()  
    allin = State()
```

Создаем кнопки и callback и прописываем логику. Для этого создаем отдельный файл в папке `callbacks/withdraw.py` и добавляем первый callback с состоянием ожидания ввода адреса Monero:
```
@router.callback_query(F.data == "withdraw")  
async def form_withdraw(call: CallbackQuery, state: FSMContext):  
    await state.set_state(WithdrawForm.address)  
    await call.message.edit_text(  
        "Введите адрес Monero в сети Monero:"  
    )
```
Нам нужен message handler для приема этого сообщения с состоянием `WithdrawForm.address`:
```
@router.message(WithdrawForm.address)  
async def form_address(message: Message, state: FSMContext):  
    # if is_valid_monero_address(message.text):  
    balance = await get_user_balance_monero(message.from_user.id)  
    print("Строка соответствует регулярному выражению.")  
    await state.update_data(address=message.text)  
    await state.set_state(WithdrawForm.amount)  
    await message.answer(f"Ваш текущий баланс: {balance} XMR\n"  
                         f"Адрес куда: {message.text}\n"  
                         f"\n"  
                         f"Введите сумму вывода:", reply_markup=all_ikb)  
    # else:  
    #     print("Строка не соответствует регулярному выражению.")    #     await message.answer(f"Ошибочка, вы ввели не корректный адрес...\n"    #                          f"\n"    #                          f"Введите адрес Monero в сети Monero:")
```

В хендлере используется валидация адреса, чтобы пользователь случайно не отправил средства на некорректный адрес или в другую сеть. Был взят шаблон с криптовалютного форума, где учитываются различные варианты адресов Monero:

- Адреса длиной 95 символов, начинающиеся с 4 или 8.
- Интегрированные адреса длиной 106 и 136 символов.
- Полные адреса длиной 256 символов.

Пример шаблона для проверки:
```
pattern = r'^(?:[48][0-9AB]|8[0-9AB]|4[1-9A-HJ-NP-Za-km-z]{12}(?:[1-9A-HJ-NP-Za-km-z]{30})?)[1-9A-HJ-NP-Za-km-z]{93}$'  
  
# Функция для проверки адреса  
def is_valid_monero_address(address):  
    return bool(re.match(pattern, address))
```

Однако, так как мы работаем в тестовой сети, данное условие не подходит: в тестовой сети адреса начинаются с 9 или B, а в основной сети — с 4 или 8 и имеют длину 95 символов. Поэтому в данном случае регулярное выражение не будет корректно работать, и временно отключаем эту проверку.

Далее нам нужно принять сумму и проверить корректность введенного числа. Для этого создадим фильтр в папке `filters`, файл `is_digit_or_float.py`:
```
class CheckForDigit(BaseFilter):  
    async def __call__(self, message: Message) -> bool:  
        print(f"фильтр message: {message.text}")  
  
        # Проверка с использованием регулярного выражения для чисел  
        if bool(re.fullmatch(r'^\d+(\.\d+)?$', message.text)):  
            # Преобразуем строку в число  
            try:  
                value = float(message.text)  
                if value > 0:  
                    return True  
                else:  
                    await message.answer(text="Введите число больше 0.")  
                    return False  
            except ValueError:  
                # Если преобразование не удается, возвращаем False  
                await message.answer(text="Произошла ошибка при обработке числа.")  
                return False  
  
        await message.answer(text="Введите целое или дробное число (например, 15 или 200.20), больше 0.")  
        return False
```
Также нужно учитывать комиссию за вывод. Обычно она ставится вручную как фиксированная или рассчитывается после создания транзакции, но перед её отправкой в сеть (broadcast), поскольку в Monero невозможно заранее точно вычислить комиссию. Если пользователю нужно вывести всю сумму с учётом комиссии, для этого используется другая команда.

Пример логики для обработки транзакции с учётом комиссии может выглядеть примерно так:

1. Пользователь вводит сумму.
2. Если нужно вывести всю сумму, учитываем комиссию.
3. Отправляем транзакцию на broadcast.
У нас должен получиться примерно такой код:
```
@router.message(WithdrawForm.amount, CheckForDigit())  
@router.callback_query(F.data == "all")  
async def form_amount(message: Message | CallbackQuery, state: FSMContext):  
    withdraw_fee = 0.1  
    await state.update_data(withdraw_fee=withdraw_fee)  
    data = await state.get_data()  
  
  
    balance = await get_user_balance_monero(message.from_user.id)  
    if isinstance(message, Message):  
        await state.update_data(allin=False)  
        user_amount = float(message.text)  
        total_amount = user_amount + withdraw_fee  
        if balance > total_amount:  
            print(data['address'])  
            print("Строка соответствует регулярному выражению.")  
            await state.update_data(amount=total_amount)  
            await message.answer(f"Адрес куда: {data['address']}\n"  
                                 f"Сумма {message.text}\n"  
                                 f"\n"  
                                 f"Подтвердить перевод ?",  
                                 reply_markup=approve_cancel_ikb)  
            await state.set_state(WithdrawForm.approve)  
        else:  
            await message.answer(f"Не достаточно средств\n"  
                                 f"Ваш текущий баланс: {balance}\n"  
                                 f"Комиссия: {withdraw_fee}\n"  
                                 f"Максимум на вывод: {balance - withdraw_fee}\n"  
                                 f"\n"  
                                 f"Введите сумму на вывод:")  
  
    else:  
        total_amount = balance - withdraw_fee  
        if balance > total_amount:  
            await state.update_data(amount=total_amount)  
            await state.update_data(allin=True)  
            await message.edit(f"Адрес куда: {data['address']}\n"  
                                 f"Сумма {total_amount}\n"  
                                 f"\n"  
                                 f"Подтвердить перевод ?",  
                                 reply_markup=approve_cancel_ikb)  
            await state.set_state(WithdrawForm.approve)  
        else:  
            await message.answer(f"Не достаточно средств\n"  
                                 f"Ваш текущий баланс: {balance}\n"  
                                 f"Комиссия: {withdraw_fee}\n"  
                                 f"Максимум на вывод: {balance - withdraw_fee}\n"  
                                 f"\n"  
                                 f"Введите сумму на вывод:")
```
Далее создаем роутер на обработку кнопок и выход из FSM состояния:
```
@router.callback_query(WithdrawForm.approve)  
async def form_approve(call: CallbackQuery, state: FSMContext):  
    if call.data == "approve":  
        print("Транзакция отправляется")  
  
        data = await state.get_data()  
        txid = await withdraw_send_to_wallet_monero(service_transfer_fee=data["withdraw_fee"],to_address=data["address"],  
                                                    amount=data["amount"],  
                                                    allin=data["allin"],  
                                                    tg_chat_id=call.from_user.id)  
        await state.clear()  
        if txid:  
            await call.message.answer(f"Транзакция успешно отправлена\n"  
                                      f"TXID: <code>{txid}</code>\n",  
                                      reply_markup=deposit_ikb)  
        else:  
            await call.message.answer(f"Произошла ошибка\n")  
    elif call.data == "cancel":  
        print("Транзакция отменена")  
        await call.message.answer(f"Транзакция отменена\n",  
                                  reply_markup=deposit_ikb)  
        await state.clear()  
    else:  
        print("хз что там еще может быть но мне так нравится")
```

Напишем нашу функцию `withdraw_send_to_wallet_monero` для переводов:

```
async def withdraw_send_to_wallet_monero(service_transfer_fee: float, to_address:str,  
                                           amount: float,  
                                           allin: bool,  
                                           tg_chat_id:str) -> bool | str:  
    async with async_session() as session:  
        try:  
            existing_user = await session.execute(select(User).where(User.tg_chat_id == tg_chat_id))  
            user = existing_user.scalar_one_or_none()  
            txs = monero_rpc.accounts[user.monero_account_id].transfer(  
                address=to_address,  
                amount=Decimal(amount), priority=config.transaction_priority_monero, relay=False, unlock_time=0)  
            print(txs[0])  
            print(txs[0].fee)  
            total_amount_transaction = amount+service_transfer_fee+float(txs[0].fee)  
            if user.monero_balance > total_amount_transaction:  
                result = daemon.send_transaction(txs[0], relay=True)  
                print(result)  
                if result["status"] == "OK":  
                    print(txs[0].hash)  
                    user_tx = MoneroWithdrawTransaction(service_transfer_fee=service_transfer_fee, network_transfer_fee=float(txs[0].fee), tx_hash=str(txs[0].hash),  
                                    amount=amount,  
                                    address_to=to_address,  
                                    user_id=user.id, account_id=user.monero_account_id)  
                    session.add(user_tx)  
                    user.monero_balance -= total_amount_transaction  
  
                    await session.commit()  
                    return str(txs[0].hash)  
  
                else:  
                    return False  
            else:  
                return False # тут можно выводить что недостаточно баланса  
            # if allin: # если вы работаете без коммисии сверху для полного вывода баланса пользователя            #     monero_rpc.accounts[user.monero_account_id].sweep_all(address=str, priority=config.transaction_priority_monero, relay=False, unlock_time=0)  
        except Exception as err:  
            print(err)
```

Мы должны получить пользователя из базы данных, чтобы взять номер аккаунта кошелька Monero и использовать его в переводе. Для подготовки транзакции используется следующая команда:
`txs = monero_rpc.accounts[user.monero_account_id].transfer(address=to_address, amount=Decimal(amount), priority=config.transaction_priority_monero, relay=False, unlock_time=0)`
- `address` — адрес, на который переводятся монеты.
- `amount` — сумма перевода, которая в этой библиотеке указывается в целых монеро.
- `priority` — приоритет перевода от 1 до 4 (4 — самый быстрый) или встроенные константы в `monero.const`, например `PRIO_PRIORITY`.
- `unlock_time` — количество блоков до разблокировки. Это значение всегда должно быть 0, чтобы средства не замораживались до определенного блока.
- `relay` — если значение `False`, транзакция не отправляется сразу, а только кодируются выходы, и она собирается перед отправкой. Это позволяет узнать вес, хэш и рассчитать комиссию для проверки.

Так как транзакция уже собрана, мы можем обращаться к ней как к объекту `transaction` и получать доступные данные:
- `txs[0].fee` - комиссия
- `txs[0].hash` - хеш сумма транзакции

При желании можно рассчитать комиссию Monero и отклонить транзакцию, если у пользователя недостаточно средств. В данном случае мы просто выполним broadcast транзакции в сеть:
`result = daemon.send_transaction(txs[0], relay=True)`
Отправляем нашу транзакцию демону со значением `relay=True`, чтобы она распространялась по сети. Затем:
1. Изменяем баланс пользователя в базе данных.
2. Добавляем запись о транзакции в таблицу.
3. Выводим пользователю хэш транзакции для проверки: `return str(txs[0].hash)`

Теперь можно проверять работоспособность.
Нажатие `/start` ![[Pasted image 20241108015441.png]]
Нажатие на `Wallet` ![[Pasted image 20241108015633.png]]
### Проверка пополнения

Нажатие на `Пополнить` ![[Pasted image 20241108015747.png]]
Пополняем баланс кошелька через кран тестовых монет [Rino](https://tools.rino.io/faucet/testnet/)
![[Pasted image 20241108020022.png]]
Так же видим что в RPC монеты пришли ![[Pasted image 20241108020045.png]]
Мы можем проверить транзакцию в блокчейне через [xmrchain ]( https://testnet.xmrchain.com/), но для этого нам понадобится `txid`, адрес аккаунта куда отправлены монеты и секретный ключ.
Секретный ключ получается из cli кошелька:
```
monero-wallet-cli --daemon-address testnet.xmr.ditatompel.com:443 --wallet-file my_test_monero_wallet --password password --testnet --trusted-daemon
```
Переключаемся на нужный аккаунт (в примере аккаунт №42):
```
account switch 42
```

Получаем `viewkey`:
```
viewkey
```

После ввода пароля кошелька отображается приватный ключ, необходимый для просмотра:
![[Pasted image 20241108020258.png]]

Так выглядит в обозреватели отправленная мне транзакция абсолютно бесполезно, но показать надо что тут есть как в биткоине посмотреть
![[Pasted image 20241108020415.png]]

Убеждаемся, что баланс в системе обновился:
![[Pasted image 20241108020428.png]]

Нажимаем еще раз на `пополнение` и проверяем, что для нас создан новый адрес для пополнения: ![[Pasted image 20241108020526.png]]
### Проверка вывода средств

Проверяем кнопку `Вывести` вводим адрес (на тестовые кошельки валидация не работает):
![[Pasted image 20241108020835.png]]

Вводим сумму жмем подтвердить и ждем монеты на другой стороне: ![[Pasted image 20241108021030.png]]

Все так же можем проверить нашу транзакцию по `txid` если у нас будет ключ для просмотра
![[Pasted image 20241108021059.png]]
### Релиз
Чтобы подготовить систему к релизу, устанавливаем пароль на RPC, чтобы исключить его случайное изменение, с помощью `--rpc-login`. Также, для повышения безопасности, убираем параметр `--testnet` и можем изменить порт.
```
monero-wallet-rpc --rpc-bind-port 18082 --wallet-file my_no_test_monero_wallet --password password --rpc-login monero:password
```
Создаем обычный кошелек через CLI (без `--testnet`):
```
monero-wallet-cli --generate-new-wallet=my_no_test_monero_wallet
```

Запускаем `monerod` и полностью синхронизируем блокчейн, оставив параметр `--prune-blockchain`, чтобы хранить только необходимую часть блокчейна для хеширования данных. Это позволяет экономить место на диске, так как хранение полного блокчейна не обязательно.

Желательно избегать использования `--bootstrap-daemon-address auto`, поскольку в сети Monero присутствуют вредоносные ноды, которые могут отслеживать отправленные транзакции через IP-адрес пользователя.
```
monerod.exe --prune-blockchain --bootstrap-daemon-address auto
```
### Заключение

В этой статье мы рассмотрели, как настроить бота для пополнения и вывода средств пользователями. Даже из этих исходников вы можете создать магазин в телеграмме, p2p биржу или же скам проект все зависит от вас, но теперь вы можете не платить комиссии сторонним сервисам и держать ключи у себя, ведь, как говорится, "не ваши ключи — не ваши монеты."

Всё это можно интегрировать в `docker-compose` и собрать в Docker-образы для удобного развертывания и переноса проекта. У каждого пользователя могут быть свои настройки, поэтому рекомендуется ознакомиться с курсом по Docker, чтобы правильно собрать проект под свои потребности.

В будущих статьях мы можем рассмотреть интеграцию с другими криптовалютами, если вам будет интересно, а этот проект будет закончен за кадром можете следить за обновлениями на GitHub там же вы найдете исходный код.

**Исходники на GitHub**: [Example Monero Payment System](https://github.com/gilfoyle-1488/Exapmle-Monero-Payment-System)  
**Сделано [gilfoyle](https://xss.is/members/389726/) специально для форума XSS.IS**