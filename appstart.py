import time
from subprocess import check_output, CalledProcessError
import uiautomator2 as u2
from tempfile import TemporaryFile
import os

import main


def open_app(app_dir):
    os.startfile(app_dir)  # os.startfile（）打开外部应该程序，与windows双击相同


def __getout(*args):
    with TemporaryFile() as t:
        try:
            out = check_output(args, stderr=t)
            return 0, out
        except CalledProcessError as e:
            t.seek(0)
            return e.returncode, t.read()


# cmd is string, split with blank
def getout(cmd):
    cmd = str(cmd)
    args = cmd.split(' ')
    return __getout(*args)


def bytes2str(bytes):
    return str(bytes, encoding='utf-8')


def isAdbConnected():
    cmd = 'adb devices'
    (code, out) = getout(cmd)
    print(out)
    if code != 0:
        print('something is error')
        return False
    outstr = bytes2str(out)
    devicelist = outstr.replace("\t", "\r\n").split("\r\n")
    for i in range(0, len(devicelist)):
        if devicelist[i] == "device":
            print('have devices')
            print(devicelist[i - 1])
            return devicelist[i - 1]
    print('no devices')
    return False


def app_start(app_dir):
    open_app(app_dir)
    time.sleep(10)
    for i in range(1, 10):
        if isAdbConnected():
            d = u2.connect_usb(isAdbConnected())
            time.sleep(5)
            d.app_start("cn.xuexi.android")
            return d
    return -1


def app_start_phone():
    for i in range(1, 10):
        if isAdbConnected():
            d = u2.connect_usb(isAdbConnected())
            time.sleep(5)
            d.app_start("cn.xuexi.android")
            return d
    return -1


def login(d, user, passwd):
    if (d(resourceId="cn.xuexi.android:id/btn_next").exists(timeout=3)):
        d(resourceId="cn.xuexi.android:id/et_phone_input").clear_text()
        d(resourceId="cn.xuexi.android:id/et_phone_input").set_text(user)
        d(resourceId="cn.xuexi.android:id/et_pwd_login").clear_text()
        d(resourceId="cn.xuexi.android:id/et_pwd_login").set_text(passwd)
        d(resourceId="cn.xuexi.android:id/btn_next").click()
        return True
    if (d(resourceId="cn.xuexi.android:id/comm_head_title").exists(timeout=3)):
        print("已登录")
        return True
    else:
        print("应用启动中。。。")
        return False


def start(user, pwd,dir):
    d = app_start(dir)
    # d = app_start_phone()
    for i in range(1, 10):
        if login(d, user, pwd):
            return d
        else:
            time.sleep(5)
            continue
    return False
if __name__ == '__main__':
    username, password, dir = main.readconfigUser()
    d = start(user=username, pwd=password, dir=dir)
