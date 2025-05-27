class NickName:
    def __init__(self, name):
        if not name:
            raise ValueError("닉네임은 비어있을 수 없습니다.")
        if not (2 <= len(name) <= 15):
            raise ValueError("닉네임은 2자 이상 15자 이하이어야 합니다.")
        self.__name = name

    @property
    def name(self):
        return self.__name
    
    def __eq__(self, other):
        if not isinstance(other, NickName):
            return NotImplemented
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return self.name
