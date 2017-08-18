from textwrap import indent

class SmsOut:
    @staticmethod
    def send(to_num, from_num, body):
        print("To: {}  From: {}".format(to_num, from_num))
        print(indent(body, '  '))

