from rest_framework_simplejwt.tokens import RefreshToken

class TokenService:
    @staticmethod
    def create_token_for_user(user_model_instance):
        refresh = RefreshToken.for_user(user_model_instance)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }