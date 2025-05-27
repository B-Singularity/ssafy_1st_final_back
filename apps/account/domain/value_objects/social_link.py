class SocialLink:
    PROVIDER_CHOICES = ['google']

    def __init__(self, provider_name: str, social_id: str):
        if not isinstance(provider_name, str):
            raise TypeError(f"provider_name은 문자열이어야 합니다. 전달된 타입: {type(provider_name)}")
        if provider_name not in self.PROVIDER_CHOICES:
            raise ValueError(f"지원하지 않는 소셜 정보 제공자입니다: {provider_name}")

        if not social_id:  # social_id가 비어있는지 확인
            raise ValueError("소셜 ID는 비어있을 수 없습니다.")
        if not isinstance(social_id, str):  # social_id가 문자열 타입인지 확인 <--- 이 검사가 누락되었을 수 있습니다.
            raise TypeError(f"social_id는 문자열이어야 합니다. 전달된 타입: {type(social_id)}")

        self._provider_name = provider_name
        self._social_id = social_id

    @property
    def provider_name(self):
        return self._provider_name

    @property
    def social_id(self):
        return self._social_id

    def __eq__(self, other):
        if not isinstance(other, SocialLink):
            return NotImplemented
        return self.provider_name == other.provider_name and \
            self.social_id == other.social_id

    def __hash__(self):
        return hash((self.provider_name, self.social_id))