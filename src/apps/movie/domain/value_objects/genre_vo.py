class GenreVO:
    def __init__(self, name: str):
        if not name:
            raise ValueError("장르 이름은 비어있을 수 없습니다.")
        if not isinstance(name, str):
            raise TypeError("장르 이름은 문자열이어야 합니다.")
        if len(name) > 50:
            raise ValueError("장르 이름은 최대 50자까지 가능합니다.")
        # VALID_GENRES 목록 검증은 현재 비활성화 상태로 가정
        self._name = name.strip()

    @property
    def name(self):
        return self._name

    def __eq__(self, other):
        if not isinstance(other, GenreVO):
            return NotImplemented
        return self._name == other._name

    def __hash__(self):
        return hash(self._name)

    def __str__(self):
        return self._name