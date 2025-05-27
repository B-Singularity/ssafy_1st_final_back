class DirectorVO:
    def __init__(self, name, external_id=None):
        if not name:
            raise ValueError("감독 이름은 비어있을 수 없습니다.")
        if not isinstance(name, str) or len(name) > 100:
            raise ValueError("감독 이름은 유효한 문자열이어야 하며 최대 100자입니다.")

        if external_id is not None:
            if not isinstance(external_id, str):
                raise TypeError("외부 ID는 문자열이어야 합니다.")
            if len(external_id) > 100:
                raise ValueError("외부 ID는 최대 100자까지 가능합니다.")

        self._name = name
        self._external_id = external_id

    @property
    def name(self):
        return self._name

    @property
    def external_id(self):
        return self._external_id

    def __eq__(self, other):
        if not isinstance(other, DirectorVO):
            return NotImplemented
        return self._name == other._name and \
            self._external_id == other._external_id

    def __hash__(self):
        return hash((self._name, self._external_id))

    def __str__(self):
        return self._name