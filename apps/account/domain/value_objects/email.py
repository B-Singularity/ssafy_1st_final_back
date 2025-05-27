import re

class Email:
    def __init__(self, address):
        if not address:
            raise ValueError("이메일 주소는 비어있을 수 없습니다.")

        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(email_regex, address):
            raise ValueError("유효하지 않은 이메일 형식입니다.")

        if len(address) > 254:
            raise ValueError("이메일 주소는 최대 254자까지 가능합니다.")
        self.__address = address
    
    @property
    def address(self):
        return self.__address
    
    def __eq__(self, other):
        if not isinstance(other, Email):
            return NotImplemented
        return self.address == other.address
    
    def __hash__(self):
        return hash(self.address)
    
    def __str__(self):
        return self.address