import abc
from typing import NamedTuple


class SocialUserInfo(NamedTuple):
    social_id: str
    email: str
    nickname: str

class SocialTokenVerifier(abc.ABC):
    @abc.abstractmethod
    def verify(self, token: str) -> SocialUserInfo:
        raise NotImplementedError

