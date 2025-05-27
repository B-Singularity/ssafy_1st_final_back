import unittest
from apps.movie.domain.value_objects.plot_vo import PlotVO


class TestPlotValueObject(unittest.TestCase):

    def test_create_valid_plot(self):
        # 계약: 유효한 문자열로 PlotVO를 성공적으로 생성할 수 있어야 한다.
        plot_text = "흥미진진한 모험 이야기입니다."
        plot_vo = PlotVO(plot_text)
        self.assertIsInstance(plot_vo, PlotVO)
        self.assertEqual(plot_vo.text, plot_text)

    def test_create_plot_with_none(self):
        # 계약: 줄거리는 선택 사항이므로 None으로도 PlotVO를 성공적으로 생성할 수 있어야 한다.
        plot_vo = PlotVO(None)
        self.assertIsInstance(plot_vo, PlotVO)
        self.assertIsNone(plot_vo.text)

    def test_create_plot_with_empty_string(self):
        # 계약: 비어있는 문자열로도 PlotVO를 성공적으로 생성할 수 있어야 한다 (정책에 따라 다를 수 있음).
        plot_vo = PlotVO("")
        self.assertIsInstance(plot_vo, PlotVO)
        self.assertEqual(plot_vo.text, "")

    def test_create_plot_too_long_raises_value_error(self):
        # 계약: 줄거리가 최대 길이(4000자)를 초과하면 ValueError가 발생해야 한다.
        # 계약: 오류 메시지는 "줄거리는 최대 4000자까지 가능합니다." 이어야 한다.
        long_plot = "가" * 4001
        with self.assertRaisesRegex(ValueError, "줄거리는 최대 4000자까지 가능합니다."):
            PlotVO(long_plot)

    def test_create_plot_at_max_length(self):
        # 계약: 최대 길이(4000자)의 줄거리로 객체가 성공적으로 생성되어야 한다.
        plot_text = "가" * 4000
        try:
            plot_vo = PlotVO(plot_text)
            self.assertEqual(plot_vo.text, plot_text)
        except ValueError:
            self.fail("최대 길이 4000자 줄거리 생성에 실패했습니다.")

    def test_create_plot_with_non_string_non_none_raises_type_error(self):
        # 계약: 줄거리가 문자열이나 None이 아닌 다른 타입으로 전달되면 TypeError가 발생해야 한다.
        # 계약: 오류 메시지는 "줄거리는 문자열이어야 합니다." 이어야 한다.
        with self.assertRaisesRegex(TypeError, "줄거리는 문자열이어야 합니다."):
            PlotVO(12345)  # type: ignore

    def test_plot_equality(self):
        # 계약: 두 PlotVO 객체는 text 속성 값이 같으면 동등해야 한다.
        plot1 = PlotVO("같은 줄거리")
        plot2 = PlotVO("같은 줄거리")
        plot3 = PlotVO("다른 줄거리")
        plot4 = PlotVO(None)
        plot5 = PlotVO(None)

        self.assertEqual(plot1, plot2)
        self.assertNotEqual(plot1, plot3)
        self.assertNotEqual(plot1, plot4)  # 문자열과 None은 다름
        self.assertEqual(plot4, plot5)  # None과 None은 같음

    def test_plot_hash_consistency(self):
        # 계약: 동등한 PlotVO 객체는 동일한 해시 값을 가져야 한다.
        plot1 = PlotVO("해시테스트")
        plot2 = PlotVO("해시테스트")
        plot_none1 = PlotVO(None)
        plot_none2 = PlotVO(None)

        self.assertEqual(hash(plot1), hash(plot2))
        self.assertEqual(hash(plot_none1), hash(plot_none2))
        self.assertNotEqual(hash(plot1), hash(plot_none1))

    def test_plot_string_representation(self):
        # 계약: PlotVO 객체의 문자열 표현은 줄거리 텍스트 자체여야 하며, None일 경우 빈 문자열을 반환한다.
        plot_text = "문자열 표현 테스트"
        plot_vo_with_text = PlotVO(plot_text)
        self.assertEqual(str(plot_vo_with_text), plot_text)

        plot_vo_none = PlotVO(None)
        self.assertEqual(str(plot_vo_none), "")


if __name__ == '__main__':
    unittest.main()