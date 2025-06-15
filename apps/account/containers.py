from dependency_injector import containers, providers

from apps.account.application.services import UserAuthAppService, UserProfileAppService, \
    UserAccountDeactivationAppService
from apps.account.infrastructure.adapters.google_verifier import GoogleTokenVerifier
from apps.account.infrastructure.repositories import DjangoUserAccountRepository
from apps.account.infrastructure.token_services import SimpleJwtTokenService


class AccountContainer(containers.DeclarativeContainer):
    repository = providers.Factory(DjangoUserAccountRepository)
    auth_token_service = providers.Factory(SimpleJwtTokenService)

    google_verifier = providers.Factory(GoogleTokenVerifier)

    social_verifier_map = providers.Dict(
        google=google_verifier
    )

    user_auth_service = providers.Factory(
        UserAuthAppService,
        user_account_repository=repository,
        social_verifier_map=social_verifier_map,
        token_service=auth_token_service,
    )
    user_profile_service = providers.Factory(
        UserProfileAppService,
        user_account_repository=repository,
    )
    user_deactivation_service = providers.Factory(
        UserAccountDeactivationAppService,
        user_account_repository=repository,
    )