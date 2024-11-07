from decimal import Decimal

from monero.backends.jsonrpc import JSONRPCWallet
from monero.const import PRIO_PRIORITY
from monero.daemon import Daemon
from monero.wallet import Wallet

from config_reader import config
from data.database import User, async_session, MoneroAddress, MoneroDepositTransaction, MoneroWithdrawTransaction
from sqlalchemy import select, and_, func

daemon = Daemon(host=config.demon_monero_host.get_secret_value(),
                port=config.demon_monero_port.get_secret_value(),
                user=config.demon_monero_user.get_secret_value(),
                password=config.demon_monero_password.get_secret_value())

monero_rpc = Wallet(JSONRPCWallet(port=config.rpc_monero_port.get_secret_value(), user=config.rpc_monero_login.get_secret_value(), password=config.rpc_monero_password.get_secret_value()))


async def add_user(tg_chat_id, username):
    async with async_session() as session:
        try:
            # Проверяем, существует ли пользователь с заданным tg_chat_id
            existing_user = await session.execute(select(User).where(User.tg_chat_id == tg_chat_id))
            user = existing_user.scalar_one_or_none()

            if user is None:
                new_user = User(tg_chat_id=tg_chat_id, username=username)  # создание юзера для получения ID в системе
                # Добавляем new_user в сессию и коммитим, чтобы получить id
                session.add(new_user)
                await session.flush()  # Выполняем, чтобы получить сгенерированный id без полной фиксации транзакции
                new_monero_account_user = monero_rpc.new_account(label=str(new_user.id))  # Добавляем label как UID в системе

                new_user.monero_account_id = int(new_monero_account_user.index)  # здесь добавляем не обновляя базу данные к юзеру индекс
                new_user.monero_zero_address = str(new_monero_account_user.address())  # здесь добавляем не обновляя базу данные к юзеру zero адрес аккаунта

                new_address = MoneroAddress(account_id=new_monero_account_user.index, sub_address_id=0, user_id=new_user.id, address=str(new_monero_account_user.address()), used=False) # добавляем в бд наш zero адрес

                session.add(new_address)
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
                user_address, sub_address_id = monero_rpc.accounts[user.monero_account_id].new_address(label=str(user.id))
                new_address = MoneroAddress(account_id=user.monero_account_id, sub_address_id=sub_address_id, user_id=user.id, address=str(user_address), used=False)
                session.add(new_address)
                await session.commit()
                return user_address

        except Exception as err:
            print(err)


async def get_all_addresses_user_monero(tg_chat_id):
    pass


async def get_new_deposit_monero():
    async with async_session() as session:
        try:
            # Получаем максимальное значение height
            query = select(func.max(MoneroDepositTransaction.height))
            result = await session.execute(query)
            highest_height = result.scalar_one_or_none() or 0  # Если None, то присваиваем 0

            # Получаем количество аккаунтов в нашем RPC кошельке
            num_accounts = len(monero_rpc.accounts)
            for account_index in range(num_accounts):
                # Получаем входящие транзакции
                incomings = monero_rpc.accounts[account_index].incoming(min_height=highest_height)
                for incoming in incomings:
                    hash = incoming.transaction.hash
                    height = incoming.transaction.height
                    amount = incoming.amount
                    address = str(incoming.local_address)

                    # Проверяем, что у транзакции достаточно подтверждений
                    confirmations = incoming.transaction.confirmations
                    if confirmations < 10:
                        # Если подтверждений меньше 10, пропускаем обработку
                        continue

                    # Проверяем наличие транзакции по хэшу
                    result = await session.execute(
                        select(MoneroDepositTransaction).where(MoneroDepositTransaction.tx_hash == hash)
                    )
                    double_check = result.scalar_one_or_none()  # Получаем единственное значение или None

                    if double_check is None:
                        # Проверяем, существует ли адрес
                        result = await session.execute(
                            select(MoneroAddress).where(MoneroAddress.address == address)
                        )
                        user_address = result.scalar_one_or_none()  # Получаем единственное значение или None

                        if user_address is not None:  # Если адрес не найден, пропускаем
                            # Создаем новую запись транзакции
                            tx = MoneroDepositTransaction(
                                tx_hash=hash,
                                amount=amount,
                                height=height,
                                user_id=user_address.user_id,
                                address_in=user_address.address,
                                account_id=account_index
                            )
                            session.add(tx)

                            # Обновляем баланс пользователя
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
            # if allin: # если вы работаете без коммисии сверху для полного вывода баланса пользователя
            #     monero_rpc.accounts[user.monero_account_id].sweep_all(address=str, priority=config.transaction_priority_monero, relay=False, unlock_time=0)

        except Exception as err:
            print(err)