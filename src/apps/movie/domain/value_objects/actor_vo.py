class ActorVO:
    def __init__(self, name, role_name=None, external_id=None):
        if not name:
            raise ValueError("배우 이름은 비어있을 수 없습니다.")
        if not isinstance(name, str) or len(name) > 100:
            raise ValueError("배우 이름은 유효한 문자열이어야 하며 최대 100자입니다.")

        if role_name is not None:
            if not isinstance(role_name, str):
                raise TypeError("배역명은 문자열이어야 합니다.")
            if len(role_name) > 100:
                raise ValueError("배역명은 최대 100자까지 가능합니다.")

        if external_id is not None:
            if not isinstance(external_id, str):
                raise TypeError("외부 ID는 문자열이어야 합니다.")
            if len(external_id) > 100:
                raise ValueError("외부 ID는 최대 100자까지 가능합니다.")

        self._name = name
        self._role_name = role_name
        self._external_id = external_id

    @property
    def name(self):
        return self._name

    @property
    def role_name(self):
        return self._role_name

    @property
    def external_id(self):
        return self._external_id

    def __eq__(self, other):
        if not isinstance(other, ActorVO):
            return NotImplemented
        return self._name == other._name and \
            self._role_name == other._role_name and \
            self._external_id == other._external_id

    def __hash__(self):
        return hash((self._name, self._role_name, self._external_id))

    def __str__(self):
        if self._role_name:
            return f"{self._name} (배역: {self._role_name})"
        return self._name

    