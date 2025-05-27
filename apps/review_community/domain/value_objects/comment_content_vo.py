

class CommentContentVO:
    def __init__(self, text):
        if text is None:
            raise ValueError("댓글 내용은 None일 수 없습니다.")
        if not isinstance(text, str):
            raise TypeError("댓글 내용은 문자열이어야 합니다.")
        
        stripped_text = text.strip()
        if not stripped_text:
            raise ValueError("댓글 내용은 비어있을 수 없습니다.")
        
        # 계약: 최대 500자 (이전 UC-09 설계 기준)
        if len(stripped_text) > 500:
            raise ValueError("댓글 내용은 최대 500자까지 가능합니다.")
        
            
        self._text = stripped_text

    @property
    def text(self):
        return self._text

    def __eq__(self, other):
        if not isinstance(other, CommentContentVO):
            return NotImplemented
        return self._text == other._text

    def __hash__(self):
        return hash(self._text)

    def __str__(self):
        return self._text