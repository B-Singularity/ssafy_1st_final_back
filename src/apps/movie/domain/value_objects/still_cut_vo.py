import re

class StillCutVO:
    URL_REGEX = re.compile(
        r'^(?:https?)://'  # Scheme: http or https
        r'(?:'  # Start of host alternatives
        r'localhost'  # Literal localhost
        r'|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'  # IPv4 address
        r'|'
        # Domain name: allowing alphanumeric, underscore, hyphen.
        # Labels separated by dots, ending with a TLD of 2-63 alphanumeric/underscore/hyphen chars.
        r'(?:[A-Z0-9_](?:[A-Z0-9-_]{0,61}[A-Z0-9_])?\.)+'
        r'[A-Z0-9_]{2,63}'
        r')'  # End of host alternatives
        r'(?::\d+)?'  # Optional port
        r'(?:/(?:\S*))?$'  # Optional path (starts with /, then any non-whitespace, or empty path)
        , re.IGNORECASE
    )

    def __init__(self, image_url, caption=None, display_order=0):
        if not image_url:
            raise ValueError("스틸컷 이미지 URL은 비어있을 수 없습니다.")
        if not isinstance(image_url, str):
            raise TypeError("스틸컷 이미지 URL은 문자열이어야 합니다.")
        if len(image_url) > 1024:
            raise ValueError("스틸컷 이미지 URL은 최대 1024자까지 가능합니다.")

        if not self.URL_REGEX.match(image_url):
            raise ValueError(f"유효하지 않은 스틸컷 이미지 URL 형식입니다: {image_url}")

        if caption is not None:
            if not isinstance(caption, str):
                raise TypeError("스틸컷 캡션은 문자열이어야 합니다.")
            if len(caption) > 255:
                raise ValueError("스틸컷 캡션은 최대 255자까지 가능합니다.")

        if not isinstance(display_order, int) or display_order < 0:
            raise ValueError("스틸컷 표시 순서는 0 이상의 정수여야 합니다.")

        self._image_url = image_url
        self._caption = caption
        self._display_order = display_order

    @property
    def image_url(self):
        return self._image_url

    @property
    def caption(self):
        return self._caption

    @property
    def display_order(self):
        return self._display_order

    def __eq__(self, other):
        if not isinstance(other, StillCutVO):
            return NotImplemented
        return self._image_url == other._image_url and \
            self._caption == other._caption and \
            self._display_order == other._display_order

    def __hash__(self):
        return hash((self._image_url, self._caption, self._display_order))

    def __str__(self):
        return self._image_url