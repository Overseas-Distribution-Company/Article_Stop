from datetime import datetime

from transaction import Transaction


class Customer:

    def __init__(self, code, description):
        self.code: str = code
        self.description: str = description
        self.transactions : [Transaction] = []

    def add_transaction(self, transaction_date: datetime, quantity: float):
        self.transactions.append(Transaction(transaction_date, quantity))

    def __repr__(self):
        return f'Customer Object: {self.code} - {self.description}'