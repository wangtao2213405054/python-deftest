# 有问题可联系作者

`QQ: 2213405054`

## python-deftest
适用于 unittest 自动化测试的可视化报告
![演示图片](https://github.com/wangtao2213405054/python-deftest/blob/master/demonstration.gif)

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
## APi 说明
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