from datetime import date

class ReleaseDateVO:
    def __init__(self, release_date: date):
        if not isinstance(release_date, date):
            raise TypeError("개봉일은 유효한 date 객체여야 합니다.")
        self._release_date = release_date

    @property
    def release_date(self):
        return self._release_date

    def formatted(self, fmt: str = "%Y년 %m월 %d일") -> str:
        return self._release_date.strftime(fmt)

    def __eq__(self, other):
        if not isinstance(other, ReleaseDateVO):
            return NotImplemented
        return self._release_date == other._release_date

    def __hash__(self):
        return hash(self._release_date)

    def __str__(self):
        return self.formatted()