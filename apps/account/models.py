# apps/account/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# UserManager는 변경 사항 없음 (기존 코드 유지)
class UserManager(BaseUserManager):
    def create_user(self, email_address, nickname, password=None, **extra_fields):
        if not email_address:
            raise ValueError('Users must have an email address')
        if not nickname:
            raise ValueError('Users must have a nickname')

        email_address = self.normalize_email(email_address)
        user = self.model(email_address=email_address, nickname=nickname, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password() # 소셜 로그인 사용자는 비밀번호를 사용 안 함으로 설정 가능

        user.save(using=self._db)
        return user

    def create_superuser(self, email_address, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if not password: # 슈퍼유저는 비밀번호가 필요함
            raise ValueError('Superuser creation requires a password.')

        return self.create_user(email_address, nickname, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email_address = models.EmailField(unique=True, max_length=254) # Google 이메일을 저장
    nickname = models.CharField(max_length=100, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) # Google 로그인 시 이 필드가 True인지 확인 필요

    last_login_at = models.DateTimeField(null=True, blank=True) # 로그인 시간 기록
    created_at = models.DateTimeField(auto_now_add=True)

    # [선택적 추가 고려] Google 프로필 사진 URL 등을 저장하고 싶다면 여기에 필드 추가
    # profile_picture_url = models.URLField(max_length=2048, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email_address'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        db_table = "users"
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"

    def __str__(self):
        return self.email_address

    def get_full_name(self):
        return self.nickname

    def get_short_name(self):
        return self.nickname


class UserSocialAccounts(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="social_accounts")
    PROVIDER_CHOICES = [
        ('google', 'Google'),
        # 다른 소셜 프로바이더 추가 가능
    ]
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES, default='google') # [확인] 'google'로 저장
    provider_account_id = models.CharField(max_length=255) # [확인] Google의 'sub' ID 저장

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_social_account"
        unique_together = (('user', 'provider'), ('provider', 'provider_account_id'))
        verbose_name = "사용자 소셜 계정"
        verbose_name_plural = "사용자 소셜 계정 목록"

    def __str__(self):
        return f"{self.user.nickname} - {self.provider}"