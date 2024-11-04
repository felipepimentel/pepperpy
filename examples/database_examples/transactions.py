import asyncio

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pepperpy.core.types import ModuleConfig
from pepperpy.database import DatabaseModule
from pepperpy.database.models import BaseModel


class Account(BaseModel):
    """Bank account model"""

    __tablename__ = "accounts"

    owner: Mapped[str] = mapped_column(String(100))
    balance: Mapped[float] = mapped_column(default=0.0)
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="account")


class Transaction(BaseModel):
    """Transaction model"""

    __tablename__ = "transactions"

    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    amount: Mapped[float]
    description: Mapped[str] = mapped_column(String(200))
    account: Mapped[Account] = relationship(back_populates="transactions")


async def transfer_money(
    db: DatabaseModule, from_id: int, to_id: int, amount: float
) -> None:
    async with db.session() as session:
        # Start transaction
        async with session.begin():
            # Get accounts
            from_account = await session.get(Account, from_id)
            to_account = await session.get(Account, to_id)

            if not from_account or not to_account:
                raise ValueError("Account not found")

            if from_account.balance < amount:
                raise ValueError("Insufficient funds")

            # Update balances
            from_account.balance -= amount
            to_account.balance += amount

            # Record transactions
            session.add(
                Transaction(
                    account=from_account,
                    amount=-amount,
                    description=f"Transfer to account {to_id}",
                )
            )

            session.add(
                Transaction(
                    account=to_account,
                    amount=amount,
                    description=f"Transfer from account {from_id}",
                )
            )

            # Transaction will be automatically committed if no errors occur


async def main() -> None:
    config = ModuleConfig(
        name="database",
        settings={
            "backend": "postgresql",
            "connection": {"url": "postgresql://user:pass@localhost/db"},
        },
    )

    db = DatabaseModule(config)
    await db.setup()

    try:
        await db.create_all()

        # Create test accounts
        async with db.session() as session:
            account1 = Account(owner="John Doe", balance=1000.0)
            account2 = Account(owner="Jane Doe", balance=500.0)
            session.add_all([account1, account2])
            await session.commit()

        # Perform transfer
        await transfer_money(db, account1.id, account2.id, 300.0)

        # Check results
        async with db.session() as session:
            accounts = await session.execute(db.query(Account).build())
            for account in accounts.scalars():
                print(f"Account {account.owner}: ${account.balance:.2f}")

    finally:
        await db.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
