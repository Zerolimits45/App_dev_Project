class User:

    def __init__(self,  email, password, name, count):
        self.__count = count
        self.__count += 1
        self.__user_id = self.__count
        self.__email = email
        self.__password = password
        self.__name = name

    def set_uid(self, uid):
        self.__user_id = uid

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_name(self, name):
        self.__name = name

    def get_uid(self):
        return self.__user_id

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__name

