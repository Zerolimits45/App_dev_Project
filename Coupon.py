class Coupon:
    def __init__(self, name, price, count):
        self.__count = count
        self.__count += 1
        self.__id = self.__count
        self.__name = name
        self.__price = price

    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        self.__price = price

    def set_id(self, id):
        self.__id = id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_id(self):
        return self.__id
