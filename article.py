from customer import Customer


class Article:
    def __init__(self,no: str,description: str):
        self.no: str = no
        self.description: str = description
        self.customer_dict: {str: Customer} = {}


    def __repr__(self):
        return f'{self.no} - {self.description}'

    def get_customer(self, customer_code:str) -> Customer:
        return self.customer_dict.get(customer_code)

    def customer_exists(self,customer_code) -> bool:
        return customer_code in self.customer_dict.keys()

    def add_customer(self, customer: Customer):
        self.customer_dict[customer.code] = customer
