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
    

    def add_social_link(self, new_social_link):
        if new_social_link not in self._social_links:
            self._social_links.append(new_social_link)

    def update_nickname(self, new_nickname, is_nickname_unique_checker):
        if self._nickname == new_nickname:
            return
        if not is_nickname_unique_checker(new_nickname, self.account_id):
            raise ValueError(f"닉네임 '{new_nickname.name}'은 이미 사용 중입니다.")
        self._nickname = new_nickname

    def record_login(self, login_time: datetime):
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