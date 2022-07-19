# 有问题可联系作者

`QQ: 2213405054`
---

## python-deftest
适用于 unittest 自动化测试的可视化报告
![演示图片](https://github.com/wangtao2213405054/python-deftest/blob/master/demonstration.gif)
---

## 功能介绍
* 提供了测试总览的功能, 展示测试总数、通过、失败、跳过、开始时间、运行时间、运行时长
* 提供了可视化饼状图功能, 可清晰看到比例
* 提供了模块、结果的筛选功能
* 内置了失败/跳过原因、原始日志、运行日志、代码展示、标签、优先级、描述等功能
* 可将传统的类和方法进行汉化
---

## 如何使用
```angular2html
git clone https://github.com/wangtao2213405054/python-deftest.git

将项目放在自己项目本地然后应用 runner.py 文件下的 MainReport 类即可, 示例如下:
import unittest
form runner import MainReport


if __name__ == '__main__':
    discover = unittest.defaultTestLoader.discover('test', pattern='t*.py')
    obj = MainReport(discover)
    obj.run()
```

## 用例编写
```angular2html
用例编写可参考 /test/test_case.py 文件
* 类的汉化
    class TestCase(unittest.TestCase):
        """ title: 测试类 """

可在类的下方添加注释, 并且注释中添加 "title: " 标签即可 (需要注意的是:冒号后方需要添加一个空格, 否则无法识别)

* 函数的汉化
    def test_case(self):
        """
        title: 这是一个方法名称
        describe: 这是方法的描述
        level: 1 这是用例的优先级, 需要注意必须为数字
        tag: 成功,五虎上将  这是用例的标签, 多个标签请以英文逗号分割
        :return:
        """

在函数中添加注释即可, 如没有注释则取默认值。(需要注意的是:冒号后方需要添加一个空格, 否则无法识别)
```
---

## API 说明
```angular2html
项目中内置了 logging 的配置, 但是默认是关闭状态, 如果需要请在调用run方法时传递 obj.run(islog=True) 即可
生成的日志会默认记录在测试报告的运行日志中
如果启用了 logging 那么需要为日志指定一个位置, 默认存放在当前文件

run 方法有4个参数可以进行选择, 说明如下: 
:param filename: 测试报告名称
:param report_path: 测试报告存放路径
:param islog: 是否启用日志打印
:param log_path: 日志存放路径
```