class User:

    def __init__(self,  email, password, first_name, last_name, gender, address, count):
        self.__count = count
        self.__count += 1
        self.__user_id = self.__count
        self.__email = email
        self.__password = password
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__address = address

    def set_uid(self, uid):
        self.__user_id = uid

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender

    def set_address(self, address):
        self.__address = address

    def get_uid(self):
        return self.__user_id

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    def get_address(self):
        return self.__address
