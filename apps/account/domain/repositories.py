import abc

class UserAccountRepository(abc.ABC):

    @abc.abstractmethod
    def generate_next_id(self) -> int:
        raise NotImplementedError
    
    @abc.abstractmethod
    def save(self, user_account):
        raise NotImplementedError
    
    @abc.abstractmethod
    def delete(self, account_id):
        raise NotImplementedError
    
    @abc.abstractmethod
    def find_by_id(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def find_by_email(self, email):
        raise NotImplementedError
    
    @abc.abstractmethod
    def find_by_nickname(self, nickname):
        raise NotImplementedError
    
    @abc.abstractmethod
    def find_by_social_link(self, social_link):
        raise NotImplementedError