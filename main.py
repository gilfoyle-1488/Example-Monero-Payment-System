from decimal import Decimal

from monero.const import PRIO_NORMAL, PRIO_PRIORITY
from monero.backends.jsonrpc import JSONRPCDaemon
from monero.daemon import Daemon

from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet

w = Wallet(JSONRPCWallet(port=18082, user="monero",password="password"))

q=w.accounts[41].incoming(min_height=0, unconfirmed=False, confirmed=True)
s=w.confirmations(q[0])
print(q,s)
# print(monero_rpc.accounts)
# for account_index in monero_rpc.accounts:
#     # Получаем входящие транзакции
#     incomings = monero_rpc.accounts[account_index].incoming(min_height=0)
#     print(incomings)
#     for incoming in incomings:
#         print(incoming.local_address)


# num_accounts = len(w.accounts)
# print(num_accounts)
# print(w.accounts[40].incoming())
# result1 = w.new_account(label="Tg_id=1") # Возвращает обьект аккаунт
# print(result1.index)
# print(result1.label)


# print(result1.addresses())
# user_address1, sub_address_id1 = w.accounts[result1.index].new_address()
# user_address2, sub_address_id2 = w.accounts[result1.index].new_address()
# print(user_address1, sub_address_id1)
# print(user_address2, sub_address_id2)
# result2 = w.new_account(label="Tg_id=2")
# print(result2.index)
# print(result2.label)
# user_address1, sub_address_id1 = w.accounts[result2.index].new_address()
# user_address2, sub_address_id2 = w.accounts[result2.index].new_address()
# print(user_address1, sub_address_id1)
# print(user_address2, sub_address_id2)

#
# print("Height: ", w.height())
#
# print("Address: ", w.address())
#
# print("balance: ", w.balance())
#
# # print(w.new_address())
# # print(w.addresses())
# # print(w.accounts[0].address())
# # print(w.accounts[0].new_address())
# # print(w.accounts[0].addresses())
#
# incomings = w.accounts[0].incoming(min_height=2615765)
# print(incomings)
# # for incoming in incomings:
# #     print(incoming.transaction.hash)
# #     print(incoming.transaction.height)
# #     print(incoming.amount)
# #     print(incoming.local_address)
#
# txs = w.accounts[0].transfer(
#     address='BdNEqq4qvyK3TTVak5BdGQ4zV64LUyAttbffSdUG1ysj5zDms9Vf8ABDKMbmKXyZ73TLNWBPCmBG3Ze85b7XUyJn7bCCCDu',
#     amount=Decimal('0.1'), priority=PRIO_PRIORITY, relay=False)
# print(txs[0])
# print(f"Type: {type(txs[0].fee)}")
# print("Fee: ", txs[0].fee)

# s = w.accounts[0].sweep_all(address="BYTsdhQUNY6Lm6LTsU1MaYiWhctHbuJYKbJRyuVHBnS6g1cDGTtBykCUUtJpeMmEth9Q21w6Eis7qLn7ujV8usHx9zTaD3n", priority=PRIO_PRIORITY)

#
#
# daemon = Daemon(host="127.0.0.1",port=28081,user="monero",password="/0KG3BrwZxDUtc5tKTPrFA==")
#
# result = daemon.send_transaction(txs[0], relay=True)
# print(result)
#
# print(result)
# print(result["status"])
#
# outgoing = w.accounts[0].outgoing(min_height=2615765)
# print(outgoing[0].amount)

# print(w.balances())
# s=w.sweep_all(address="BYTsdhQUNY6Lm6LTsU1MaYiWhctHbuJYKbJRyuVHBnS6g1cDGTtBykCUUtJpeMmEth9Q21w6Eis7qLn7ujV8usHx9zTaD3n", priority=PRIO_PRIORITY)
# print(s)