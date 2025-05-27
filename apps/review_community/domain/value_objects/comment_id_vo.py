import uuid

class CommentIdVO:
    def __init__(self, value):
        if not value:
            raise ValueError("댓글 ID 값은 비어있을 수 없습니다.")
        if not isinstance(value, str):
            raise TypeError("댓글 ID 값은 문자열이어야 합니다.")
        
        try:
            parsed_uuid = uuid.UUID(value)
        except ValueError: # UUID 문자열 형식 자체가 잘못된 경우
            raise ValueError(f"유효하지 않은 UUID 문자열 형식입니다: '{value}'")

        if parsed_uuid.version != 4: # 파싱 성공 후 버전 확인
            raise ValueError("댓글 ID는 UUID 버전 4 형식이어야 합니다.")
            
        self._value = value

    @property
    def value(self):
        return self._value

    @classmethod
    def generate(cls):
        return cls(str(uuid.uuid4()))

    def __eq__(self, other):
        if not isinstance(other, CommentIdVO):
            return NotImplemented
        return self._value == other._value

    def __hash__(self):
        return hash(self._value)

    def __str__(self):
        return self._value