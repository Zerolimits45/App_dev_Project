class Product:
    count_id = 0
    def __init__(self, name, price, description, brand, quantity, image):
        Product.count_id += 1
        self.__name = name
        self.__price = price
        self.__description = description
        self.__brand = brand
        self.__quantity = quantity
        self.__image = image

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_description(self):
        return self.__description

    def get_brand(self):
        return self.__brand

    def get_quantity(self):
        return self.__quantity

    def get_image(self):
        return self.__image

    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        self.__price = price

    def set_description(self, description):
        self.__description = description

    def set_brand(self, brand):
        self.__brand = brand

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_image(self, image):
        self.__image = image
