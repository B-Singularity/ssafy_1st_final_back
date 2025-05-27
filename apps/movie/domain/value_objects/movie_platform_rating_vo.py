class MoviePlatformRatingVO:
    def __init__(self, platform_name, score):
        if not platform_name:
            raise ValueError("평가 플랫폼 이름은 비어있을 수 없습니다.")
        if not isinstance(platform_name, str) or len(platform_name) > 100:
            raise ValueError("평가 플랫폼 이름은 유효한 문자열이어야 하며 최대 100자입니다.")

        if not isinstance(score, (int, float)):
            raise TypeError("평점은 숫자(정수 또는 실수)여야 합니다.")
        if not (0.0 <= score <= 10.0):
            raise ValueError("평점은 0.0에서 10.0 사이의 값이어야 합니다.")

        self._platform_name = platform_name
        self._score = float(score)

    @property
    def platform_name(self):
        return self._platform_name

    @property
    def score(self):
        return self._score

    def __eq__(self, other):
        if not isinstance(other, MoviePlatformRatingVO):
            return NotImplemented
        return self._platform_name == other._platform_name and \
            self._score == other._score

    def __hash__(self):
        return hash((self._platform_name, self._score))

    def __str__(self):
        return f"{self._platform_name}: {self._score:.1f}/10"