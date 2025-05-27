class RuntimeVO:
    def __init__(self, minutes: int):
        if not isinstance(minutes, int) or minutes < 0:
            raise ValueError("상영 시간은 0 이상의 정수여야 합니다.")
        self._minutes = minutes

    @property
    def minutes(self):
        return self._minutes

    def formatted_duration(self) -> str:
        hours = self._minutes // 60
        mins = self._minutes % 60
        if hours > 0:
            return f"{hours}시간 {mins}분"
        return f"{mins}분"

    def __eq__(self, other):
        if not isinstance(other, RuntimeVO):
            return NotImplemented
        return self._minutes == other._minutes

    def __hash__(self):
        return hash(self._minutes)

    def __str__(self):
        return self.formatted_duration()