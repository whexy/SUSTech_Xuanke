import random
import requests
import re
import time
import sys
import json
courseList = {}
s = requests.Session()


def rush_manager():
    global courseList
    while len(courseList.keys()) != 0:
        failedList = {}
        for group in courseList:
            if rush_group(courseList[group]):
                print(group + "组选课成功")
            else:
                failedList[group] = courseList[group]
        courseList = failedList
        print("开始下一轮。")


def rush_group(courseList):
    for aSimpleClass in courseList:
        course_id = courseList[aSimpleClass]
        if rush(course_id):
            print("已抢到", aSimpleClass)
            return True
        else:
            print("未抢到", aSimpleClass)
    print("本组全部失败。准备进入下一组。")
    return False


def rush(num):
    operlist = ["bxqjhxkOper", "fawxkOper", "knjxkOper", "ggxxkxkOper"]
    url = "https://jwxt.sustech.edu.cn/jsxsd/xsxkkc/"
    urllist = [url + i + "?jx0404id=" + num + "&xkzy=&trjf=" for i in operlist]
    for urls in urllist:
        r = s.get(urls)
        result = str(r.text)
        print(result)
        time.sleep(random.random() * random.random())
        if result.find("true") >= 1:
            return True
    return False


if __name__ == '__main__':
    username = input("id:")
    password = input("pwd:")
    with open("course.json", "r") as f:
        courseList = json.loads(f.read())
    data = {
        'username': username,
        'password': password,
        'execution': re.findall('on" value="(.+?)"', r.text)[0],
        '_eventId': 'submit',
        'geolocation': ''
    }
    r = s.post(
        'https://cas.sustech.edu.cn/cas/login?service=https%3A%2F%2Fjwxt.sustech.edu.cn%2Fjsxsd%2Fxsxk%2Fxklc_list%3FVes632DSdyV%3DNEW_XSD_PYGL',
        data)
    print(r)
    if str(r) != "<Response [200]>":
        print("CAS 验证失败，请重新运行脚本。按回车键结束。")
        input()
        exit(-1)
    print("CAS验证成功")
    print("等待选课开始")
    while True:
        r = s.get(
            'https://jwxt.sustech.edu.cn/jsxsd/xsxk/xklc_list?Ves632DSdyV=NEW_XSD_PYGL'
        )
        key = re.findall('href="(.+)" target="blank">进入选课', r.text)
        if len(key) > 0:
            break
        time.sleep(random.random() * random.random())

    k = key[0]
    s.get('https://jwxt.sustech.edu.cn' + k)
    print("------抢课开始------")
    rush_manager()
    s.close()
    print("脚本运行结束，按回车键退出。")
    input()
