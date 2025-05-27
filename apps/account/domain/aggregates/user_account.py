from datetime import datetime
import uuid

class UserAccount:
    def __init__(self,
                 account_id,
                 email,
                 nickname,
                 social_links, 
                 created_at,
                 last_login_at=None): 
        
        
        self._account_id = account_id
        self._email = email
        self._nickname = nickname
        self._social_links = list(social_links) 
        self._created_at = created_at
        self._last_login_at = last_login_at
    

    @classmethod
    def register_or_login(cls,
                          account_id_generator,
                          google_social_link,
                          provided_email,
                          initial_nickname,
                          existing_account=None):
        if existing_account:
            existing_account.record_login(datetime.now())
            return existing_account
        else:
            account_id = account_id_generator()
            now = datetime.now()

            user = cls(
                account_id=account_id,
                email=provided_email,
                nickname=initial_nickname,
                social_links=[google_social_link], 
                created_at=now, 
                last_login_at=now
            )
            return user
    
    def update_nickname(self, new_nickname, nickname_uniqueness_checker):
        if self._nickname == new_nickname: 
            return
        if not nickname_uniqueness_checker(new_nickname): 
            raise ValueError(f"닉네임 '{new_nickname.name}'은 이미 사용 중입니다.")
        self._nickname = new_nickname

    def record_login(self, login_time):
        self._last_login_at = login_time

    
    def __eq__(self, other):
        return isinstance(other, UserAccount) and self._account_id == other._account_id
    
    def __hash__(self):
        return hash(self._account_id)
    
    @property
    def account_id(self): 
        return self._account_id

    @property
    def email(self): 
        return self._email

    @property
    def nickname(self): 
        return self._nickname
        
    @property
    def social_links(self): 
        return list(self._social_links)

    @property
    def created_at(self):
        return self._created_at

    @property
    def last_login_at(self):
        return self._last_login_at