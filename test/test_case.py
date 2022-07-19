# _author: Coke
# _date: 2022/6/29 16:44
import logging
import random
import unittest


class TestCase(unittest.TestCase):
    """
    title: 测试类
    """

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_pass(self):
        """
        title: 测试方法A
        describe: 测试方法A备注
        level: 1
        tag: 成功,五虎上将
        :return:
        """
        data = [random.choice(['张飞', '关羽', '赵云', '马超', '黄忠']) for _ in range(random.randint(5, 20))]

        for item in data:
            logging.info(item)

        self.assertTrue(True, '我想让他成功')

    def test_fail(self):
        """
        title: 测试方法B
        describe: 测试方法B备注
        level: 0
        tag: 失败,五子良将
        :return:
        """
        data = [random.choice(['张辽', '张郃', '于禁', '乐进', '徐晃']) for _ in range(random.randint(5, 20))]

        for item in data:
            logging.info(item)

        self.assertTrue(False, '我想让他失败')

    @unittest.skip('我想让他跳过')
    def test_skip(self):
        """
        title: 测试方法C
        describe: 测试方法C备注
        level: 2
        tag: 跳过
        :return:
        """
        pass
