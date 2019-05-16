# 1.unittest使用
import unittest


class WANGYI(unittest.TestCase):
    '''unittest使用'''
    def setUp(self):
        '''开始'''
        print('test start')
        self.veriftString = 'test'

    def test01(self):
        '''测试方法'''
        self.assertEquals('test',self.veriftString,msg='俩值不等')

    def tearDown(self):
        '''结束'''
        print('test over')

if __name__ == '__main__':
    # unittest.main()方法会搜索该模块下所有以test开头的测试用例方法，并自动执行它们。
    unittest.main()


# from selenium import webdriver
import unittest, time


class BaiduTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)  # 隐性等待时间为30秒
        self.base_url = "https://www.baidu.com"

    def test_baidu(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("kw").clear()
        driver.find_element_by_id("kw").send_keys("unittest")
        driver.find_element_by_id("su").click()
        time.sleep(3)
        title = driver.title
        self.assertEqual(title, u"unittest_百度搜索")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()


# 2.collections
# from collections import namedtuple
#
# Circle = namedtuple('Circle', ['x', 'y', 'z'])
# p = Circle(10, 2, 5)
# print(p)
# print(p.x)
# print(p.y)
# print(p.z)

# 3.hashlib
# import hashlib
#
# sha1 = hashlib.sha1()
# # python3需要对字符串encode()
# sha1.update('how to use sha1 in '.encode())
# sha1.update('python hashlib?'.encode())
# print(sha1.hexdigest())


# 4.subprocess
# import subprocess
# 在桌面上创建一个文件夹
# obj = subprocess.Popen('mkdir subprocesstest', shell=True, cwd='/home/lijianguo/桌面')


5.mock
from unittest import TestCase, mock
import unittest


class Person(object):

    def __init__(self):
        self.__age = 10

    def get_fullname(self, first_name, last_name):
        return first_name + ' ' + last_name

    def get_age(self):
        return self.__age

    @staticmethod
    def get_class_name():
        return Person.__name__
#
#
class PersonTest(TestCase):

    def test_should_get_age(self):
        p = Person()
        # 不mock时,get_age应该时10
        self.assertEquals(p.get_age(), 10)
    
    def test_should_get_fullname(self):
        p = Person()
        p.get_fullname = mock.Mock(return_value='James Harden')  # 直接模拟出了get_fullname的返回值
        self.assertEquals(p.get_fullname(), 'James Harden')
#
#
    def test_should_get_fullname(self):
        p = Person()
        p.get_fullname = mock.create_autospec(p.get_fullname, return_value='James Harden')
        # 随便给了get_fullname两个参数,还是返回了mock的return_value
        # 使用mock.create_autospec效验参数个数,两个才OK
        self.assertEquals(p.get_fullname('1','2'), 'James Harden')
#
    def test_should_get_age(self):
        p = Person()
        # 使用side_effect参数,依次返回指定值
        p.get_age = mock.Mock(side_effect=[10, 11, 12])
        self.assertEquals(p.get_age(), 10)
        self.assertEquals(p.get_age(), 11)
        self.assertEquals(p.get_age(), 12)

    def test_should_get_fullname(self):
        p = Person()
        values = {('James', 'Harden'): 'James Harden', ('Tracy', 'Grady'): 'Tracy Grady'}
        # 根据不同参数,返回不同的值
        p.get_fullname = mock.Mock(side_effect=lambda x, y: values[(x, y)])
        self.assertEquals(p.get_fullname('James', 'Harden'), 'James Harden')
        # lambda说明
        # assertEquals中将get_fullname参数传给lambda中的x,y,lambda返回values中相应的(x, y)元组对应的值
        self.assertEquals(p.get_fullname('Tracy', 'Grady'), 'Tracy Grady')
#
#     def test_should_raise_exception(self):
#         p = Person()
#         p.get_age = mock.Mock(side_effect=TypeError('integer type'))
#         # 只要调就会抛出异常
#         self.assertRaises(TypeError, p.get_age)
#
#
    # 以字符串的形式列出静态方法的路径，在测试的参数里会自动得到一个Mock对象
    @mock.patch('0313.Person.get_class_name')
    def test_should_get_class_name(self, mock_get_class_name):
        mock_get_class_name.return_value = 'Guy'
    
        self.assertEqual(Person.get_class_name(), 'Guy')
#
#
# if __name__ == '__main__':
#     unittest.main()


import psycopg2

# 连接数据库
conn = psycopg2.connect(dbname="test_0313", user="lijianguo", password="123456", host="127.0.0.1", port="5432")

# 创建cursor以访问数据库
cur = conn.cursor()

# 创建表
# cur.execute(
#         'CREATE TABLE Employee ('
#         'name    varchar(80),'
#         'address varchar(80),'
#         'age     int,'
#         'date    date'
#         ')'
#     )

# 插入数据
cur.execute("INSERT INTO Employee VALUES('Gopher', 'China Beijing', 100, '2017-05-27')")
# 更新数据
cur.execute("UPDATE Employee SET age=12 WHERE name='Gopher'")
# 查询数据
cur.execute("SELECT * FROM Employee")
rows = cur.fetchall()
for row in rows:
    print('name=' + str(row[0]) + ' address=' + str(row[1]) +
        ' age=' + str(row[2]) + ' date=' + str(row[3]))



# 删除数据
# cur.execute("DELETE FROM Employee WHERE name='Gopher'")

# 提交事务
conn.commit()

# 关闭连接
conn.close()
