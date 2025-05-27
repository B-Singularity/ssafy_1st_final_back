

class PlotVO:
    def __init__(self, text):
        if text is not None:
            if not isinstance(text, str):
                raise TypeError("줄거리는 문자열이어야 합니다.")
            if len(text) > 4000:
                raise ValueError("줄거리는 최대 4000자까지 가능합니다.")
        self._text = text

    @property
    def text(self):
        return self._text

    def __eq__(self, other):
        if not isinstance(other, PlotVO):
            return NotImplemented
        return self._text == other._text

    def __hash__(self):
        return hash(self._text)

    def __str__(self):
        return self._text if self._text is not None else ""