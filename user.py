class User:

    def __init__(self,  email, password, name, count):
        self.__count = count
        self.__count += 1
        self.__user_id = self.__count
        self.__email = email
        self.__password = password
        self.__name = name
        self.__money_spent = 1000  # TESTING
        if self.__money_spent == 0:
            self.__points = 0
        else:
            self.__points = (self.__money_spent/20)*10
        self.__coupons = []

    def set_uid(self, uid):
        self.__user_id = uid

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_name(self, name):
        self.__name = name

    def set_money_spent(self, money_spent):
        self.__money_spent = money_spent

    def set_points(self, points):
        self.__points = points

    def set_coupons(self, coupon):
        self.__coupons.append(coupon)

    def get_uid(self):
        return self.__user_id

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__name

    def get_money_spent(self):
        return self.__money_spent

    def get_points(self):
        return self.__points

    def get_coupons(self):
        return self.__coupons
