import unittest
from apps.movie.domain.value_objects.runtime_vo import RuntimeVO


class TestRuntimeValueObject(unittest.TestCase):

    def test_create_valid_runtime(self):
        # 계약: 유효한 (0 이상의) 정수값으로 RuntimeVO를 성공적으로 생성할 수 있어야 한다.
        runtime_vo_90 = RuntimeVO(90)
        self.assertIsInstance(runtime_vo_90, RuntimeVO)
        self.assertEqual(runtime_vo_90.minutes, 90)

        runtime_vo_0 = RuntimeVO(0)  # 0분도 유효하다고 가정
        self.assertEqual(runtime_vo_0.minutes, 0)

    def test_create_with_negative_minutes_raises_value_error(self):
        # 계약: 음수 값으로 RuntimeVO 생성을 시도하면 ValueError가 발생해야 한다.
        # 계약: 오류 메시지는 "상영 시간은 0 이상의 정수여야 합니다." 이어야 한다.
        with self.assertRaisesRegex(ValueError, "상영 시간은 0 이상의 정수여야 합니다."):
            RuntimeVO(-10)

    def test_create_with_non_integer_type_raises_value_error(self):
        # 계약: 정수가 아닌 타입으로 RuntimeVO 생성을 시도하면 ValueError가 발생해야 한다.
        # (현재 __init__에서는 TypeError 대신 ValueError를 발생시키고 있음, 일관성을 위해 ValueError 유지 또는 TypeError로 변경 고려)
        # 여기서는 현재 코드에 맞춰 ValueError를 테스트합니다.
        invalid_inputs = [10.5, "90", None]
        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                with self.assertRaisesRegex(ValueError, "상영 시간은 0 이상의 정수여야 합니다."):
                    RuntimeVO(invalid_input)  # type: ignore

    def test_formatted_duration_method(self):
        # 계약: formatted_duration 메서드는 상영 시간을 "X시간 Y분" 또는 "Y분" 형식으로 반환해야 한다.
        self.assertEqual(RuntimeVO(0).formatted_duration(), "0분")
        self.assertEqual(RuntimeVO(59).formatted_duration(), "59분")
        self.assertEqual(RuntimeVO(60).formatted_duration(), "1시간 0분")
        self.assertEqual(RuntimeVO(90).formatted_duration(), "1시간 30분")
        self.assertEqual(RuntimeVO(120).formatted_duration(), "2시간 0분")
        self.assertEqual(RuntimeVO(125).formatted_duration(), "2시간 5분")

    def test_runtime_equality(self):
        # 계약: 두 RuntimeVO 객체는 minutes 속성 값이 같으면 동등해야 한다.
        vo1 = RuntimeVO(120)
        vo2 = RuntimeVO(120)
        vo3 = RuntimeVO(90)

        self.assertEqual(vo1, vo2)
        self.assertNotEqual(vo1, vo3)

    def test_runtime_hash_consistency(self):
        # 계약: 동등한 RuntimeVO 객체는 동일한 해시 값을 가져야 한다.
        vo1 = RuntimeVO(120)
        vo2 = RuntimeVO(120)
        self.assertEqual(hash(vo1), hash(vo2))

    def test_runtime_string_representation(self):
        # 계약: RuntimeVO 객체의 문자열 표현은 formatted_duration 메서드의 결과와 같아야 한다.
        self.assertEqual(str(RuntimeVO(95)), "1시간 35분")


if __name__ == '__main__':
    unittest.main()