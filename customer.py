from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import stats

from transaction import Transaction


class Customer:
    transactions: [Transaction]

    def __init__(self, code, description):
        self.code: str = code
        self.description: str = description
        self.transactions: [Transaction] = []
        self.weight: float = 0

        # Linear regression params
        self.slope: float = 0
        self.intersect: float = 0

        # Confidence Line Params
        self.confident_slope: float = 0
        self.confident_intersect: float = 0

    def __repr__(self):
        return f'Customer Object: {self.code} - {self.description}'

    def add_transaction(self, transaction_date: datetime, quantity: float):
        self.transactions.append(Transaction(transaction_date, quantity))

    def total_ordered_quantity(self) -> float:
        """
        Description: Calculate the total ordered quantity this customer ordered
        """
        return sum([transaction.quantity for transaction in self.transactions])

    def predict_point(self, x):
        return self.slope * x + self.intersect

    def predict_confidence_point(self, x):
        return self.confident_slope * x + self.confident_intersect

    def calculate_intervals(self) -> [int]:
        ret_lst = []
        if len(self.transactions) >= 2:
            for i in range(len(self.transactions) - 1):
                ret_lst.append((self.transactions[i + 1].transaction_date - self.transactions[i].transaction_date).days)
        return ret_lst

    def calculate_lingress(self):

        intervals = self.calculate_intervals()

        if len(intervals) > 1 :
            self.slope, self.intersect, lo_slope, up_slope = stats.theilslopes(self.calculate_intervals(),
                                                                               [i for i in
                                                                                range(len(self.transactions) - 1)],
                                                                               .99)
        elif len(intervals) == 1:
            self.slope = 1
            self.intersect = intervals[0]
            up_slope = 1
            self.confident_intersect = 2 * intervals[0]

        else:
            up_slope = 1
            self.confident_intersect = np.inf

        self.confident_slope = up_slope
        self.confident_intersect = self.intersect

    def get_next_predicted_interval(self):
        return self.predict_point(len(self.transactions))

    def get_next_prediction_max(self):
        return self.predict_confidence_point(len(self.transactions))

    def get_current_interval(self):
        return (datetime.today() - self.transactions[-1].transaction_date).days

    def get_next_predicted_date(self):
        return self.transactions[-1].transaction_date + self.get_next_predicted_interval()

    def get_next_max_date(self):
        return self.transactions[-1].transaction_date + self.get_next_predicted_interval()

    def do_flag(self) -> bool:
        self.calculate_lingress()
        return self.get_next_prediction_max() < self.get_current_interval()

    def plot_graph(self):
        self.calculate_lingress()
        fig, ax = plt.subplots()
        ax.plot(self.calculate_intervals(), '-o', label='Interval plot')
        self.calculate_lingress()
        ax.plot(self.predict_point(np.linspace(0, len(self.transactions), len(self.transactions) + 1)), 'g')
        ax.plot(self.predict_confidence_point(np.linspace(0, len(self.transactions), len(self.transactions) + 1)), 'm')

        ax.plot([len(self.transactions)], [self.get_next_predicted_interval()], 'og', label='Prediction')
        ax.plot([len(self.transactions)], [self.get_next_prediction_max()], 'om', label='Max allowed')
        ax.plot([len(self.transactions)], [self.get_current_interval()], 'or', label='Currently at')

        ax.axvline(x=len(self.transactions), color='k')
        ax.legend()
        ax.set_xlabel('Interval number')
        ax.set_ylabel('Interval length (days)')
        ax.set_title(f'{self.description}')
        plt.show()
