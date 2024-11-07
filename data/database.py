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
    tg_chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)

    monero_account_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)
    monero_zero_address: Mapped[str] = mapped_column(String(95), nullable=True)
    monero_addresses: Mapped[list["MoneroAddress"]] = relationship(back_populates="user", uselist=True)
    monero_balance: Mapped[float] = mapped_column(Float, default=0, doc="Value of transaction input")
    monero_deposit_transaction: Mapped[list["MoneroDepositTransaction"]] = relationship(back_populates="user", uselist=True)
    monero_withdraw_transaction: Mapped[list["MoneroWithdrawTransaction"]] = relationship(back_populates="user", uselist=True)




class MoneroAddress(Base):
    __tablename__ = "monero_address"

    id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="monero_addresses", uselist=False)
    address: Mapped[str] = mapped_column(String(95), nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, default=False)
    account_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_address_id: Mapped[int] = mapped_column(Integer, nullable=False)


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

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
