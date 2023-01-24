class Order:
    def __init__(self, id, customer_name, total, status, address, count):
        self.id = id
        self.customer_name = customer_name
        self.total = total
        self.status = status
        self.count = count
        self.count += 1
        self.order_id = self.count
        self.address = address
        self.items = []

    def get_id(self):
        return self.id

    def get_customer_name(self):
        return self.customer_name

    def get_total(self):
        return self.total

    def get_status(self):
        return self.status

    def get_order_id(self):
        return self.order_id

    def get_address(self):
        return self.address

    def get_items(self):
        return self.items

    def set_id(self, id):
        self.id = id

    def set_customer_name(self, customer_name):
        self.customer_name = customer_name

    def set_total(self, total):
        self.total = total

    def set_status(self, status):
        self.status = status

    def set_order_id(self, order_id):
        self.order_id = order_id

    def set_address(self, address):
        self.address = address

    def set_items(self, items):
        self.items = items
