from customer import Customer
import matplotlib.pyplot as plt

# S00225
# S00226
# S00716

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
        self.calculate_weights()
        fig, ax = plt.subplots()
        wedge_it = [(f'{customer.code} - {customer.description}', customer.weight) for customer in self.customer_dict.values()]
        wedges, texts, autotexts = ax.pie(
            [wedge[1] for wedge in wedge_it],
            autopct='%1.1f%%',
            shadow=True,
            explode=[0 for customer in self.customer_dict.values() ]
        )
        ax.legend(
            wedges,
            [customer[0] for customer in wedge_it],
            title='Customers'
        )
        ax.axis('equal')
        ax.set_title(f'{self.no} - {self.description}')
        plt.show()

    def do_flag_article(self, weight):
        self.calculate_weights()
        accumulated_weight = 0
        for customer in self.customer_dict.values():
            if customer.do_flag():
                accumulated_weight += customer.weight

        return accumulated_weight > weight
