class Transaction:

    def __init__(self, transaction_date, quantity):
        self.transaction_date = transaction_date
        self.quantity = quantity

    def __repr__(self):
        return f'Transaction object: Date: {self.transaction_date} - Quantity: {self.quantity}'
