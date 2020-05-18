from customer import Customer
import matplotlib.pyplot as plt

class Article:
    def __init__(self, no: str, description: str):
        self.no: str = no
        self.description: str = description
        self.customer_dict: {str: Customer} = {}

    def __repr__(self):
        return f'{self.no} - {self.description}'

    def get_customer(self, customer_code: str) -> Customer:
        return self.customer_dict.get(customer_code)

    def customer_exists(self, customer_code) -> bool:
        return customer_code in self.customer_dict.keys()

    def add_customer(self, customer: Customer):
        self.customer_dict[customer.code] = customer

    def calculate_weights(self):
        total = sum([customer.total_ordered_quantity() for customer in self.customer_dict.values()])
        for customer in self.customer_dict.values():
            customer.weight = customer.total_ordered_quantity() / total

    def create_weight_plot(self):
        fig, ax = plt.subplots()
        ax.pie([customer.weight for customer in self.customer_dict.values()])
        plt.show()