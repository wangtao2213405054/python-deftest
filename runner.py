# _author: Coke
# _date: 2022/6/21 17:54

from io import StringIO
from logging import config, getLogger

import logging.config
import configparser
import traceback
import unittest
import inspect
import logging
import json
import time
import os
import re


class CaseResult(unittest.case.TestCase):
    """ 测试用例 """

    def __init__(self, test: unittest.case.TestCase):
        super(CaseResult, self).__init__()
        self.test = test  # 确保为测试用例

        self.name = self.get_case_content(test, 'title')  # 测试用例名称
        self.case_path = test.id()  # 测试用例路径
        self.describe = self.get_case_content(test, 'describe')  # 测试用例描述
        self.docs = test._testMethodDoc  # 测试用例备注信息

        self.file_name = test.__module__  # 测试用例所在文件

        self.class_name = self._get_content(test.__class__.__doc__, 'title') or test.__class__.__name__  # 测试用例所在类名
        self.class_path = f'{test.__module__}.{test.__class__.__name__}'  # 测试用例所在类路径
        self.class_docs = test.__class__.__doc__  # 测试类所有的描述信息

        self.tags = self.get_case_tags(test)  # 用例标签
        self.level = self.get_case_level(test)  # 用例级别
        self.code = self.inspect_code(test)  # 用例代码

        self.start_time = round(time.time(), 6)  # 测试用例开始时间
        self.end_time = None  # 测试用例结束时间
        self.duration = None  # 间隔时间

        self.status = None  # 用例状态
        self.output = None  # 操作日志
        self.exc_info = None  # 异常信息
        self.reason = None  # 跳过, 失败, 出错原因

    @property
    def case_info(self):
        """
        组装当前用例的基础数据结构
        :return:
        """
        case_data = dict(
            name=self.name,
            casePath=self.case_path,
            description=self.describe,
            status=self.status,
            tags=self.tags,
            level=self.level,
            time=dict(startTime=self.start_time, endTime=self.end_time, duration=self.duration),
            className=self.class_name,
            classDocs=self.class_docs,
            moduleName=self.file_name,
            code=self.code,
            output=self.output,
            excInfo=self.exc_info,
            reason=self.reason,
        )
        return case_data

    @staticmethod
    def inspect_code(test: unittest.case.TestCase):
        """
        根据测试对象获取用例代码
        :param test: unittest.case.TestCase 对象
        :return:
        """
        test_method = getattr(test.__class__, test._testMethodName)

        try:
            code = inspect.getsource(test_method)
        except Exception as e:
            logging.error(f'获取测试代码失败: {e}')
            code = ''

        return code

    @staticmethod
    def get_case_tags(test: unittest.case.TestCase):
        """
        从测试用例备注中匹配出指定格式的 tags
        多个 Tag 以英文逗号 , 分割
        :param test: unittest.case.TestCase 对象
        :return:
        """
        case_tags = []

        case_docs = test._testMethodDoc
        if case_docs and 'tag' in case_docs:
            pattern = re.compile(r'tag: (.+)')
            tag = re.findall(pattern, case_docs)
            for item in tag:
                for items in item.split(','):
                    case_tags.append(items)

        return case_tags

    def get_case_content(self, test: unittest.case.TestCase, content):
        """
        从测试用例备注中匹配出指定格式的内容信息
        :param test: unittest.case.TestCase 对象
        :param content: 需要匹配的关键字
        :return:
        """

        case_docs = test._testMethodDoc

        return self._get_content(case_docs, content)

    @staticmethod
    def _get_content(docs, content):
        """
        正则匹配出指定的内容信息
        :param docs: 要匹配的数据
        :param content: 需要匹配的内容信息
        :return:
        """
        case_content = ''

        pattern = re.compile(fr'{content}: (.+)')
        content_data = re.findall(pattern, docs)
        if content_data:
            case_content = content_data[0]

        return case_content

    @staticmethod
    def get_case_level(test: unittest.case.TestCase):
        """
        从测试用例备注中匹配出指定格式的优先级信息
        :param test: unittest.case.TestCase 对象
        :return:
        """

        case_docs = test._testMethodDoc
        case_level = 2  # 默认二级优先级
        pattern = re.compile(r'level: (\d+)')
        level = re.findall(pattern, case_docs)
        if level:
            try:
                case_level = int(level[0])
            except Exception as e:
                logging.error(f'获取用例级别错误: {e}')

        return case_level


class RewriteTestResult(unittest.TestResult):
    """ 重写了 unittest.TestResult 部分方法 """

    result = None  # 测试用例对象 CaseResult

    def __init__(self, stream=None, descriptions=None, verbosity=None):

        super().__init__(stream, descriptions, verbosity)

        self.testcase_results = []  # 所有用例测试结果的对象列表
        self.class_list = []  # 测试类列表
        self.verbosity = verbosity or 1
        self.buffer = True  # 缓存用例输出

        self.name = None  # 重写 result 对象的 name 属性
        self.begin_time = round(time.time(), 6)  # 测试开始时间
        self.finish_time = None  # 测试完成时间
        self.duration = None  # 测试持续时间

        self.successes_count = 0  # 成功用例数
        self.failures_count = 0  # 失败用例数
        self.skipped_count = 0  # 跳过用例数
        self.success = False  # 测试是否通过

        # 日志缓存
        self.log_cap = StringIO()
        self.logger = logging.getLogger()

        self.know_exceptions = {}  # 已知异常字典, 用于通过异常名称映射失败原因

    @property
    def summary(self):
        """
        组装结果概要
        :return:
        """

        data = dict(
            name=self.name,
            success=self.success,
            result=dict(
                testRun=self.testsRun,
                successes=self.successes_count,
                failures=self.failures_count,
                skipped=self.skipped_count
            ),
            time=dict(beginTime=self.begin_time, finishTime=self.finish_time, duration=self.duration),
            details=[item.case_info for item in self.testcase_results],
            classList=self.class_list
        )
        return data

    def startTestRun(self) -> None:
        """
        重写 unittest.TestResult.startTestRun 方法
        测试开始时调用, 可参考 unittest.TextTestRunner 中的 run 方法
        在测试开始前, 启动 usbcan 的设备并开启通道
        :return:
        """

        # 定义日志内存
        log = logging.StreamHandler(self.log_cap)
        self.logger.addHandler(log)

        logging.info('开始测试')

    def stopTestRun(self) -> None:
        """
        重写 unittest.TestResult.stopTestRun 方法
        测试结束后调用
        在测试结束后, 停止 usbcan 的通道并关闭设备
        :return:
        """

        self.finish_time = round(time.time(), 6)  # 测试结束时间
        self.success = self.wasSuccessful()  # 测试是否通过
        self.duration = round(self.finish_time - self.begin_time, 3)  # 测试间隔时间

        self.finish_time = time.strftime(r'%Y-%m-%d %H:%M:%S', time.localtime(self.finish_time))
        self.begin_time = time.strftime(r'%Y-%m-%d %H:%M:%S', time.localtime(self.begin_time))

        logging.info(f'完成测试, 本次测试耗时 {self.duration} 秒')

    def startTest(self, test: unittest.case.TestCase) -> None:
        """
        重写 unittest.TestResult.startTest 方法
        单个用例执行开始时调用, 可参考 unittest.TestCase 中的 run 方法
        :param test: unittest.case.TestCase 对象
        :return:
        """
        # 清空日志内存
        self.log_cap.truncate(0)
        self.log_cap.seek(0)

        # 获取用例对象
        self.result = None  # 初始化 result
        self.result = CaseResult(test)
        self.testcase_results.append(self.result)
        if self.result.class_name not in self.class_list:
            self.class_list.append(self.result.class_name)

        # 开始执行用例
        unittest.TestResult.startTest(self, test)
        # logging.info(f'—————————— 开始执行用例: {self.result.name} ——————————')

    def stopTest(self, test: unittest.case.TestCase) -> None:
        """
        重写 unittest.TestResult.stopTest 方法
        单个用例执行结束后调用
        :param test: unittest.case.TestCase 对象
        :return:
        """
        # logging.info(f'—————————— 结束执行用例: {self.result.name} ——————————')

        # 获取用例对象
        self.result.end_time = round(time.time(), 6)
        self.result.duration = round(self.result.end_time - self.result.start_time, 3)
        self.result.output = self.log_cap.getvalue()

        # 清空日志内存
        self.log_cap.truncate(0)
        self.log_cap.seek(0)

    def addSuccess(self, test: unittest.case.TestCase) -> None:
        """
        重写 unittest.TestResult.addSuccess 方法
        用例成功时调用
        :param test: unittest.case.TestCase 对象
        :return:
        """

        self.result.status = 'pass'
        self.successes_count += 1
        super().addSuccess(test)

    def addError(self, test: unittest.case.TestCase, err) -> None:
        """
        重写 unittest.TestResult.addError 方法
        用例异常时调用
        :param test: unittest.case.TestCase 对象
        :param err: 错误信息元组
        :return:
        """

        self._add_failures(test, err)

    def addFailure(self, test: unittest.case.TestCase, err) -> None:
        """
        重写 unittest.TestResult.addFailure 方法
        用例失败时调用
        :param test: unittest.case.TestCase 对象
        :param err: 错误信息元组
        :return:
        """

        self._add_failures(test, err)

    def _add_failures(self, test: unittest.case.TestCase, err):
        """
        用例异常、用例失败时调用
        :param test: unittest.case.TestCase 对象
        :param err: 错误信息元组
        :return:
        """

        self.result.status = 'fail'
        self.failures_count += 1
        super().addFailure(test, err)

        error_info, traceback_info = self._get_exception_message(err)

        self.result.reason = error_info
        self.result.exc_info = traceback_info

    def addSkip(self, test: unittest.case.TestCase, reason: str) -> None:
        """
        重写 unittest.TestResult.addSkip 方法
        用例跳过时调用
        :param test: unittest.case.TestCase 对象
        :param reason: 跳过原因
        :return:
        """

        self.result.status = 'skip'
        self.skipped_count += 1
        self.result.reason = reason
        super().addSkip(test, reason)

    def _get_exception_message(self, err):
        """
        获取异常消息并返回异常原因以及原始错误
        :param err: unittest 抛出的 err 元组
        :return:
        """
        error_class, error_info, traceback_info = err
        error_info = str(error_info)

        # 寻找当前错误是否有映射关系
        exc_full_path = f'{error_class.__module__}.{error_class.__name__}'
        if self.know_exceptions and isinstance(self.know_exceptions, dict):
            error_info = self.know_exceptions.get(exc_full_path, error_info)

        return error_info, ''.join(traceback.format_exception(*err))


class MainReport(RewriteTestResult):
    """ 运行入口 """

    report_path = None
    filename = 'report.html'

    def __init__(self, suites, stream=None, descriptions=None, verbosity=None):

        super(RewriteTestResult, self).__init__(stream, descriptions, verbosity)

        self.suites = suites

    @staticmethod
    def log(file_path):
        log_time = time.strftime('%Y-%m-%d')
        file_path = os.path.abspath(file_path)
        # 获取 Log 配置文件
        con_log = os.path.join(os.path.dirname(__file__), 'conf', 'log.conf')

        # 拼接 Log 存放
        text = (os.path.join(file_path, f'{log_time}log.log'), 'a')
        conf = configparser.ConfigParser()
        conf.read(con_log)
        conf.set('handler_fileHandler', 'args', str(text))
        conf.write(open(con_log, 'w'))
        config.fileConfig(con_log)
        log_config = getLogger()
        return log_config

    def run(self, filename=None, report_path='.', islog=False, log_path='.'):
        """
        运行测试并生成测试报告
        :param filename: 测试报告名称
        :param report_path: 测试报告存放路径
        :param islog: 是否启用日志打印
        :param log_path: 日志存放路径
        :return:
        """
        if islog:
            self.log(log_path)

        if filename:
            self.filename = filename if filename.endswith('.html') else f'{filename}.html'

        self.report_path = os.path.abspath(report_path)

        runner = unittest.TextTestRunner(resultclass=RewriteTestResult)
        result = runner.run(self.suites)
        all_data = result.summary

        template_path = os.path.join(os.path.dirname(__file__), 'conf', 'template')
        template_path = os.path.abspath(template_path)

        set_list = [{'key': None, 'value': '全部'}]

        for item in all_data['classList']:
            set_list.append({'key': item, 'value': item})

        with open(template_path, 'rb') as file:
            template_data = file.readlines()

        file_path = os.path.abspath(os.path.join(self.report_path, self.filename))
        with open(file_path, 'wb') as file:
            for item in template_data:
                if b'#CaseSummaryString' in item:
                    item = f'   summary: {json.dumps(all_data, ensure_ascii=False, indent=4)},\n'.encode()
                if b'#CaseSetListString' in item:
                    item = f'   caseSetList: {json.dumps(set_list, ensure_ascii=False, indent=4)},\n'.encode()

                file.write(item)

        logging.info(f'测试报告已生成: {file_path}')


if __name__ == '__main__':
    discover = unittest.defaultTestLoader.discover(r'test', pattern='t*.py')
    obj = MainReport(discover)
    obj.run(islog=True)
