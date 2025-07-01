import re


class PosterImageVO:
    # 웹 URL(http, https)만 허용하도록 수정
    URL_REGEX = re.compile(
        r'^https?://'  # http:// or https:// 만 허용
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def __init__(self, url: str):
        if not url:
            raise ValueError("포스터 이미지 URL은 비어있을 수 없습니다.")
        if not isinstance(url, str):
            raise TypeError("포스터 이미지 URL은 문자열이어야 합니다.")
        if len(url) > 1024:
            raise ValueError("포스터 이미지 URL은 최대 1024자까지 가능합니다.")

        if not self.URL_REGEX.match(url):
            raise ValueError("유효하지 않은 URL 형식입니다.")

        self._url = url

    @property
    def url(self):
        return self._url

    def __eq__(self, other):
        if not isinstance(other, PosterImageVO):
            return NotImplemented
        return self._url == other._url

    def __hash__(self):
        return hash(self._url)

    def __str__(self):
        return self._url