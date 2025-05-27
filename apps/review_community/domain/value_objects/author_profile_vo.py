class AuthorProfileVO:
    def __init__(self, account_id, nickname):
        if not isinstance(account_id, int) or account_id <= 0:
            raise ValueError("계정 ID는 0보다 큰 정수여야 합니다.")
        
        if not nickname:
            raise ValueError("닉네임은 비어있을 수 없습니다.")
        if not isinstance(nickname, str):
            raise TypeError("닉네임은 문자열이어야 합니다.")
        if not (2 <= len(nickname) <= 15):
            raise ValueError("닉네임은 2자 이상 15자 이하이어야 합니다.")

        self._account_id = account_id
        self._nickname = nickname
    
    @property
    def account_id(self): 
        return self._account_id
    
    @property
    def nickname(self): 
        return self._nickname
        
    def __eq__(self, other):
        if not isinstance(other, AuthorProfileVO): 
            return NotImplemented
        return self._account_id == other._account_id and \
               self._nickname == other._nickname

    def __hash__(self):
        return hash((self._account_id, self._nickname))

    def __str__(self):
        return self._nickname