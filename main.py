import asyncio
import datetime
import random
import re
import time

import aiohttp

OPER_list = ["bxqjhxkOper", "fawxkOper", "knjxkOper", "ggxxkxkOper"]

XK_URL = "https://jwxt.sustech.edu.cn/jsxsd/xsxkkc/"
XK_Center_URL = 'https://jwxt.sustech.edu.cn/jsxsd/xsxk/xklc_list?Ves632DSdyV=NEW_XSD_PYGL'
CAS_URL = "https://cas.sustech.edu.cn/cas/login?service=https%3A%2F%2Fjwxt.sustech.edu.cn%2Fjsxsd%2Fxsxk%2Fxklc_list%3FVes632DSdyV%3DNEW_XSD_PYGL"
ROOT = 'http://jwxt.sustech.edu.cn'

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 '
                  'Safari/537.36',
    'Connection': 'keep-alive',
    'Referer': 'http://jwxt.sustech.edu.cn/'
}


async def handle(username, password, courseList):
    async with aiohttp.ClientSession(headers=headers) as session:
        login_status = await cas_login(session, username, password)
        if login_status != 200:
            print(login_status)
            print("Login Failed. Please check your username and password.")
            return
        log("Login Success")
        log("Waiting for beginning")
        system_url = ROOT + await get_system_url(session)
        async with session.get(system_url) as resp:
            print(resp.cookies)
        log("Begin!")
        task = task_generator(session, courseList)
        await asyncio.wait(task)


def log(message):
    print(str(datetime.datetime.now()), message)


def task_generator(session, courseList):
    task = []
    for course_id in courseList:
        url_list = [XK_URL + oper + "?jx0404id=" +
                    course_id + "&xkzy=&trjf=" for oper in OPER_list]
        for url in url_list:
            future = asyncio.create_task(rush(session, url))
            future.add_done_callback(lambda out: print(out.result()))
            task.append(future)
    return task


async def rush(session, url):
    async with session.get(url) as resp:
        html_resp = await resp.text()
        # return str(html_resp).find("true") != -1
        return str(html_resp)


async def get_system_url(session):
    while True:
        async with session.get(XK_Center_URL) as resp:
            html_resp = await resp.text()
            key = re.findall('href="(.+)" target="blank">进入选课', html_resp)
            if len(key) > 0:
                return key[0]
        time.sleep(random.random())


async def cas_login(session, username, password):
    async with session.get(CAS_URL) as resp:
        html_resp = await resp.text()
        execution = re.findall('on" value="(.+?)"', html_resp)[0]
    post_data = dict(username=username, password=password,
                     execution=execution, _eventId='submit', geolocation='')
    async with session.post(CAS_URL, data=post_data) as resp:
        return resp.status


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(
        handle("11810000", "PA55W0RD", ["202020211000934", "202020211000933"]))
