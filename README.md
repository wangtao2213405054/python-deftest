# ���������ϵ����

`QQ: 2213405054`

## python-deftest
������ unittest �Զ������ԵĿ��ӻ�����
![��ʾͼƬ](https://github.com/wangtao2213405054/python-deftest/blob/master/demonstration.gif)

## ���ʹ��
```angular2html
git clone https://github.com/wangtao2213405054/python-deftest.git

����Ŀ�����Լ���Ŀ����Ȼ��Ӧ�� runner.py �ļ��µ� MainReport �༴��, ʾ������:
import unittest
form runner import MainReport


if __name__ == '__main__':
    discover = unittest.defaultTestLoader.discover('test', pattern='t*.py')
    obj = MainReport(discover)
    obj.run()
```
## APi ˵��
```angular2html
��Ŀ�������� logging ������, ����Ĭ���ǹر�״̬, �����Ҫ���ڵ���run����ʱ���� obj.run(islog=True) ����
���ɵ���־��Ĭ�ϼ�¼�ڲ��Ա����������־��
��������� logging ��ô��ҪΪ��־ָ��һ��λ��, Ĭ�ϴ���ڵ�ǰ�ļ�

run ������4���������Խ���ѡ��, ˵������: 
:param filename: ���Ա�������
:param report_path: ���Ա�����·��
:param islog: �Ƿ�������־��ӡ
:param log_path: ��־���·��
```