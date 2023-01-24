class Feedback:
    def __init__(self,  email, phonenumber, name, message, reason, count):
        self.__count = count
        self.__count += 1
        self.__user_id = self.__count
        self.__email = email
        self.__phonenumber = phonenumber
        self.__name = name
        self.__message = message
        self.__reason = reason

    def set_uid(self, uid):
        self.__user_id = uid

    def set_email(self, email):
        self.__email = email

    def set_password(self, phonenumber):
        self.__phonenumber = phonenumber

    def set_name(self, name):
        self.__name = name

    def set_message(self, message):
        self.__name = message

    def set_reason(self, reason):
        self.__reason = reason

    def get_uid(self):
        return self.__user_id

    def get_email(self):
        return self.__email

    def get_phonenumber(self):
        return self.__phonenumber

    def get_name(self):
        return self.__name

    def get_message(self):
        return self.__message

    def get_reason(self):
        return self.__reason
