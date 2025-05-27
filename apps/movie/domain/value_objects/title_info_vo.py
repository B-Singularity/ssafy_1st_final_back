

class TitleInfoVO:
    def __init__(self, korean_title, original_title = None):
        if not korean_title:
            raise ValueError("한국어 영화 제목은 비어있을 수 없습니다.")
        if len(korean_title) > 255:
            raise ValueError("한국어 영화 제목은 최대 255자까지 가능합니다.")

        if original_title is not None:
            if not isinstance(original_title, str):
                raise TypeError("원제는 문자열이어야 합니다.")
            if len(original_title) > 255:
                raise ValueError("원제는 최대 255자까지 가능합니다.")

        self._korean_title = korean_title
        self._original_title = original_title

    @property
    def korean_title(self):
        return self._korean_title

    @property
    def original_title(self):
        return self._original_title

    def __eq__(self, other):
        if not isinstance(other, TitleInfoVO):
            return NotImplemented
        return self.korean_title == other.korean_title and \
            self.original_title == other.original_title

    def __hash__(self):
        return hash((self.korean_title, self.original_title))

    def __str__(self):
        if self._original_title and self._korean_title != self._original_title:
            return f"{self._korean_title} ({self._original_title})"
        return self._korean_title

