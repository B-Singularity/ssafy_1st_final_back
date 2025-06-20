import abc
from typing import Dict, Any

class AuthTokenService(abc.ABC):
    @abc.abstractmethod
    def issue_for_user(self, user_account_id: int) -> Dict[str, str]:
        raise NotImplementedError

    @abc.abstractmethod
    def blacklist(self, refresh_token: str) -> None:
        raise NotImplementedError
