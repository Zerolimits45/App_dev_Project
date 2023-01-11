class Coupon:
    def __init__(self, name, price, effect, count):
        self.__count = count
        self.__count += 1
        self.__id = self.__count
        self.__name = name
        self.__price = price
        self.__effect = effect/100

    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        self.__price = price

    def set_id(self, id):
        self.__id = id

    def set_effect(self, effect):
        self.__effect = effect

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_id(self):
        return self.__id

    def get_effect(self):
        return self.__effect
