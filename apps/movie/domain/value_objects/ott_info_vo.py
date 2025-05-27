import re


class OTTInfoVO:
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

    def __init__(self, platform_name, watch_url=None, logo_image_url=None, availability_note=None):
        if not platform_name:
            raise ValueError("OTT 플랫폼 이름은 비어있을 수 없습니다.")
        if not isinstance(platform_name, str) or len(platform_name) > 100:
            raise ValueError("OTT 플랫폼 이름은 유효한 문자열이어야 하며 최대 100자입니다.")

        if watch_url is not None:
            if not isinstance(watch_url, str):
                raise TypeError("시청 URL은 문자열이어야 합니다.")
            if len(watch_url) > 1024:
                raise ValueError("시청 URL은 최대 1024자까지 가능합니다.")
            if not self.URL_REGEX.match(watch_url):
                raise ValueError(f"유효하지 않은 시청 URL 형식입니다: {watch_url}")

        if logo_image_url is not None:
            if not isinstance(logo_image_url, str):
                raise TypeError("플랫폼 로고 URL은 문자열이어야 합니다.")
            if len(logo_image_url) > 1024:
                raise ValueError("플랫폼 로고 URL은 최대 1024자까지 가능합니다.")
            if not self.URL_REGEX.match(logo_image_url):
                raise ValueError(f"유효하지 않은 플랫폼 로고 URL 형식입니다: {logo_image_url}")

        if availability_note is not None:
            if not isinstance(availability_note, str):
                raise TypeError("이용 정보 안내는 문자열이어야 합니다.")
            if len(availability_note) > 100:
                raise ValueError("이용 정보 안내는 최대 100자까지 가능합니다.")

        self._platform_name = platform_name
        self._watch_url = watch_url
        self._logo_image_url = logo_image_url
        self._availability_note = availability_note

    @property
    def platform_name(self):
        return self._platform_name

    @property
    def watch_url(self):
        return self._watch_url

    @property
    def logo_image_url(self):
        return self._logo_image_url

    @property
    def availability_note(self):
        return self._availability_note

    def __eq__(self, other):
        if not isinstance(other, OTTInfoVO):
            return NotImplemented
        return self._platform_name == other._platform_name and \
            self._watch_url == other._watch_url and \
            self._logo_image_url == other._logo_image_url and \
            self._availability_note == other._availability_note

    def __hash__(self):
        return hash((self._platform_name, self._watch_url, self._logo_image_url, self._availability_note))

    def __str__(self):
        if self._availability_note:
            return f"{self._platform_name} ({self._availability_note})"
        return self._platform_name