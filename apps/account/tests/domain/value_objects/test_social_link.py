import unittest
from apps.account.domain.value_objects.social_link import SocialLink

class TestSocialLinkValueObject(unittest.TestCase):

    def test_create_valid_google_social_link(self):
        # 계약: 유효한 'google' provider_name과 social_id로 SocialLink 객체를 성공적으로 생성할 수 있어야 한다.
        provider = "google"
        social_id_value = "test_google_id_12345"
        social_link_vo = SocialLink(provider_name=provider, social_id=social_id_value)
        self.assertIsInstance(social_link_vo, SocialLink)
        self.assertEqual(social_link_vo.provider_name, provider)
        self.assertEqual(social_link_vo.social_id, social_id_value)

    def test_create_social_link_with_unsupported_provider_raises_value_error(self):
        # 계약: 지원하지 않는 provider_name으로 SocialLink 객체 생성을 시도하면 ValueError가 발생해야 한다.
        # 계약: 오류 메시지는 "지원하지 않는 소셜 정보 제공자입니다: [provider_name]" 이어야 한다.
        unsupported_provider = "facebook"
        with self.assertRaisesRegex(ValueError, f"지원하지 않는 소셜 정보 제공자입니다: {unsupported_provider}"):
            SocialLink(provider_name=unsupported_provider, social_id="test_facebook_id")

    def test_create_social_link_with_empty_social_id_raises_value_error(self):
        # 계약: 비어있는 social_id로 SocialLink 객체 생성을 시도하면 ValueError가 발생해야 한다.
        # 계약: 오류 메시지는 "소셜 ID는 비어있을 수 없습니다." 이어야 한다.
        with self.assertRaisesRegex(ValueError, "소셜 ID는 비어있을 수 없습니다."):
            SocialLink(provider_name="google", social_id="")

    def test_create_social_link_with_none_social_id_raises_value_error(self):
        # 계약: social_id로 None 값을 전달하여 SocialLink 객체 생성을 시도하면 ValueError가 발생해야 한다.
        # 계약: 오류 메시지는 "소셜 ID는 비어있을 수 없습니다." 이어야 한다.
        with self.assertRaisesRegex(ValueError, "소셜 ID는 비어있을 수 없습니다."):
            SocialLink(provider_name="google", social_id=None) # type: ignore

    def test_create_social_link_with_non_string_provider_name_raises_type_error(self):
        # 계약: provider_name이 문자열이 아닐 경우 TypeError가 발생해야 한다.
        with self.assertRaisesRegex(TypeError, "provider_name은 문자열이어야 합니다."):
            SocialLink(provider_name=123, social_id="test_id") # type: ignore

    def test_create_social_link_with_non_string_social_id_raises_type_error(self):
        # 계약: social_id가 문자열이 아닐 경우 TypeError가 발생해야 한다.
        with self.assertRaisesRegex(TypeError, "social_id는 문자열이어야 합니다."):
            SocialLink(provider_name="google", social_id=12345) # type: ignore

    def test_social_link_equality_based_on_attributes(self):
        # 계약: 두 SocialLink 객체는 provider_name과 social_id가 모두 같으면 동등한 것으로 간주되어야 한다.
        link1 = SocialLink(provider_name="google", social_id="user123")
        link2 = SocialLink(provider_name="google", social_id="user123")
        link3_diff_id = SocialLink(provider_name="google", social_id="user456")
        # link4_diff_provider = SocialLink(provider_name="facebook", social_id="user123") # 현재는 google만 지원

        self.assertEqual(link1, link2)
        self.assertTrue(link1 == link2)
        self.assertNotEqual(link1, link3_diff_id)
        # self.assertNotEqual(link1, link4_diff_provider) # 다른 provider 테스트는 PROVIDER_CHOICES 확장 후 가능

    def test_social_link_equality_with_other_types(self):
        # 계약: SocialLink 객체는 다른 타입의 객체와 동등하지 않아야 한다.
        link1 = SocialLink(provider_name="google", social_id="user123")
        self.assertNotEqual(link1, "google_user123") # 문자열과 비교
        self.assertNotEqual(link1, None)

    def test_social_link_hash_consistency(self):
        # 계약: 동등한 SocialLink 객체는 동일한 해시 값을 가져야 한다.
        link1 = SocialLink(provider_name="google", social_id="user123")
        link2 = SocialLink(provider_name="google", social_id="user123")
        self.assertEqual(hash(link1), hash(link2))

if __name__ == '__main__':
    unittest.main()