import re


class TrailerVO:
    URL_REGEX = re.compile(
        r'^(?:https?)://'
        r'(?:'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
        r'(?:[A-Z0-9_](?:[A-Z0-9-_]{0,61}[A-Z0-9_])?\.)+'
        r'[A-Z0-9_]{2,63}'
        r')'
        r'(?::\d+)?'
        r'(?:/(?:\S*))?$', re.IGNORECASE
    )

    def __init__(self, url, trailer_type=None, site_name=None, thumbnail_url=None):
        if not url:
            raise ValueError("예고편 URL은 비어있을 수 없습니다.")
        if not isinstance(url, str):
            raise TypeError("예고편 URL은 문자열이어야 합니다.")
        if len(url) > 1024:
            raise ValueError("예고편 URL은 최대 1024자까지 가능합니다.")
        if not self.URL_REGEX.match(url):
            raise ValueError(f"유효하지 않은 예고편 URL 형식입니다: {url}")

        if trailer_type is not None:
            if not isinstance(trailer_type, str):
                raise TypeError("예고편 종류는 문자열이어야 합니다.")
            if len(trailer_type) > 50:  # 예시 최대 길이
                raise ValueError("예고편 종류는 최대 50자까지 가능합니다.")

        if site_name is not None:
            if not isinstance(site_name, str):
                raise TypeError("예고편 제공 사이트 이름은 문자열이어야 합니다.")
            if len(site_name) > 50:  # 예시 최대 길이
                raise ValueError("예고편 제공 사이트 이름은 최대 50자까지 가능합니다.")

        if thumbnail_url is not None:
            if not isinstance(thumbnail_url, str):
                raise TypeError("썸네일 URL은 문자열이어야 합니다.")
            if len(thumbnail_url) > 1024:
                raise ValueError("썸네일 URL은 최대 1024자까지 가능합니다.")
            if not self.URL_REGEX.match(thumbnail_url):
                raise ValueError(f"유효하지 않은 썸네일 URL 형식입니다: {thumbnail_url}")

        self._url = url
        self._trailer_type = trailer_type
        self._site_name = site_name
        self._thumbnail_url = thumbnail_url

    @property
    def url(self):
        return self._url

    @property
    def trailer_type(self):
        return self._trailer_type

    @property
    def site_name(self):
        return self._site_name

    @property
    def thumbnail_url(self):
        return self._thumbnail_url

    def __eq__(self, other):
        if not isinstance(other, TrailerVO):
            return NotImplemented
        return self._url == other._url and \
            self._trailer_type == other._trailer_type and \
            self._site_name == other._site_name and \
            self._thumbnail_url == other._thumbnail_url

    def __hash__(self):
        return hash((self._url, self._trailer_type, self._site_name, self._thumbnail_url))

    def __str__(self):
        return self._url