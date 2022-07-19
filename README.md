# ���������ϵ����

`QQ: 2213405054`
---

## python-deftest
������ unittest �Զ������ԵĿ��ӻ�����
![��ʾͼƬ](https://github.com/wangtao2213405054/python-deftest/blob/master/demonstration.gif)
---

## ���ܽ���
* �ṩ�˲��������Ĺ���, չʾ����������ͨ����ʧ�ܡ���������ʼʱ�䡢����ʱ�䡢����ʱ��
* �ṩ�˿��ӻ���״ͼ����, ��������������
* �ṩ��ģ�顢�����ɸѡ����
* ������ʧ��/����ԭ��ԭʼ��־��������־������չʾ����ǩ�����ȼ��������ȹ���
* �ɽ���ͳ����ͷ������к���
---

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

## ������д
```angular2html
������д�ɲο� /test/test_case.py �ļ�
* ��ĺ���
    class TestCase(unittest.TestCase):
        """ title: ������ """

��������·����ע��, ����ע������� "title: " ��ǩ���� (��Ҫע�����:ð�ź���Ҫ���һ���ո�, �����޷�ʶ��)

* �����ĺ���
    def test_case(self):
        """
        title: ����һ����������
        describe: ���Ƿ���������
        level: 1 �������������ȼ�, ��Ҫע�����Ϊ����
        tag: �ɹ�,�廢�Ͻ�  ���������ı�ǩ, �����ǩ����Ӣ�Ķ��ŷָ�
        :return:
        """

�ں��������ע�ͼ���, ��û��ע����ȡĬ��ֵ��(��Ҫע�����:ð�ź���Ҫ���һ���ո�, �����޷�ʶ��)
```
---

## API ˵��
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