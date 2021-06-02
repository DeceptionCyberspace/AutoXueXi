import datetime
import random
import time
from configparser import ConfigParser
import os
import tiaozhandati
import uiautomator2 as u2
import appstart
from meiridati import meiridati
from readlisten import listenaudios, readarticles
from shuangrenduizhan import shuangren
import zsydati


def init(d):
    if d(resourceId="cn.xuexi.android:id/comm_head_title").exists(timeout=3):
        d(resourceId="cn.xuexi.android:id/home_bottom_tab_icon_large").click()
        # print("回归首页")
        return True
    else:
        if d(resourceId="cn.xuexi.android:id/my_back").exists(timeout=3):
            d(resourceId="cn.xuexi.android:id/my_back").click()
            init(d)
        else:
            d(text="").click()
            init(d)


def readconfigUser():
    conn = ConfigParser()
    file_path = os.path.join(os.path.abspath('.'), 'config.ini')
    if not os.path.exists(file_path):
        raise FileNotFoundError("文件不存在")
    conn.read(file_path, encoding='utf-8')
    user = conn.get('usernames', 'user').split(" ")
    password = user[1]
    username = user[0]
    dir = conn.get('virtual','dir')
    return username, password,dir


def readconfigAnswer(typeAnswer):
    conn = ConfigParser()
    file_path = os.path.join(os.path.abspath('.'), 'config.ini')
    if not os.path.exists(file_path):
        raise FileNotFoundError("文件不存在")
    conn.read(file_path, encoding='utf-8')
    if typeAnswer == "challenge":
        return conn.get('api', typeAnswer), int(conn.get('api', typeAnswer + '_count_min')), int(conn.get('api',
                                                                                                          typeAnswer + '_count_max')), int(
            conn.get(
                'api', typeAnswer + '_delay_min')), int(conn.get('api', typeAnswer + '_delay_max'))
    if typeAnswer == "four" or typeAnswer == "double":
        return conn.get('api', typeAnswer), int(conn.get('api', typeAnswer + '_count')), float(
            conn.get('api', typeAnswer + '_answer_delay')), int(conn.get('api', typeAnswer + '_delay_max')), int(conn.get(
            'api', typeAnswer + '_delay_max'))
    if typeAnswer == "local":
        return conn.get('api', typeAnswer),conn.get('api', typeAnswer+'_name')
    if typeAnswer == "daily" or typeAnswer=="listenaudio":
        return conn.get('api', typeAnswer)
    if typeAnswer == "readarticle":
        return conn.get('api', typeAnswer),conn.get('api',typeAnswer+'_commenttext'),conn.get('api',typeAnswer+'_sharename')


def getIntegral(d):
    d(resourceId="cn.xuexi.android:id/comm_head_xuexi_mine").click()
    time.sleep(1)
    d.xpath(
        '//*[@resource-id="cn.xuexi.android:id/my_recycler_view"]/android.widget.LinearLayout[1]/android.widget.ImageView[1]').click()
    time.sleep(3)
    print(d.xpath('//*[@resource-id="app"]/android.view.View[3]/android.view.View[2]').get_text())
    print(d(text="登录").get_text() + ":" + d.xpath(
        '//android.widget.ListView/android.view.View[1]/android.view.View[3]').get_text())
    print(d(text="我要选读文章").get_text() + ":" + d.xpath(
        '//android.widget.ListView/android.view.View[2]/android.view.View[3]').get_text())
    if d.xpath('//android.widget.ListView/android.view.View[2]/android.view.View[3]').get_text()[3]=="分":
        readIntegral=int(d.xpath('//android.widget.ListView/android.view.View[2]/android.view.View[3]').get_text()[2])
    else:
        readIntegral=int(d.xpath('//android.widget.ListView/android.view.View[2]/android.view.View[3]').get_text()[2:4])
    print(d(text="视听学习").get_text() + ":" + d.xpath(
        '//android.widget.ListView/android.view.View[3]/android.view.View[3]').get_text())
    listenIntegral = int(d.xpath('//android.widget.ListView/android.view.View[3]/android.view.View[3]').get_text()[2])
    print(d(text="视听学习时长").get_text() + ":" + d.xpath(
        '//android.widget.ListView/android.view.View[4]/android.view.View[3]').get_text())
    listenTimeIntegral = int(
        d.xpath('//android.widget.ListView/android.view.View[4]/android.view.View[3]').get_text()[2])
    print(d(text="每日答题").get_text() + ":" + d.xpath(
        '//android.widget.ListView/android.view.View[5]/android.view.View[3]').get_text())
    dailyIntegral = int(
        d.xpath('//android.widget.ListView/android.view.View[5]/android.view.View[3]').get_text()[2])
    print(d(text="每周答题").get_text() + ":" + d.xpath(
        '//android.widget.ListView/android.view.View[6]/android.view.View[3]').get_text())
    weekIntegral = int(
        d.xpath('//android.widget.ListView/android.view.View[6]/android.view.View[3]').get_text()[2])
    print(d(text="专项答题").get_text() + ":" + d.xpath(
        '//android.widget.ListView/android.view.View[7]/android.view.View[3]').get_text())
    specialIntegral = int(
        d.xpath('//android.widget.ListView/android.view.View[7]/android.view.View[3]').get_text()[2])
    print(d(text="挑战答题").get_text() + ":" + d.xpath(
        '//android.widget.ListView/android.view.View[8]/android.view.View[3]').get_text())
    challengeIntegral = int(
        d.xpath('//android.widget.ListView/android.view.View[8]/android.view.View[3]').get_text()[2])
    print(d(text="四人赛").get_text() + ":" + d.xpath(
        '//android.widget.ListView/android.view.View[9]/android.view.View[3]').get_text())
    fourIntegral = int(
        d.xpath('//android.widget.ListView/android.view.View[9]/android.view.View[3]').get_text()[2])
    print(d(text="双人对战").get_text() + ":" + d.xpath(
        '//android.widget.ListView/android.view.View[10]/android.view.View[3]').get_text())
    doubleIntegral = int(
        d.xpath('//android.widget.ListView/android.view.View[10]/android.view.View[3]').get_text()[2])
    print(d(text="订阅").get_text() + ":" + d.xpath(
        '//android.widget.ListView/android.view.View[11]/android.view.View[3]').get_text())
    bookIntegral = int(
        d.xpath('//android.widget.ListView/android.view.View[11]/android.view.View[3]').get_text()[2])
    print(d(text="分享").get_text() + ":" + d.xpath(
        '//android.widget.ListView/android.view.View[12]/android.view.View[3]').get_text())
    shareIntegral = int(
        d.xpath('//android.widget.ListView/android.view.View[12]/android.view.View[3]').get_text()[2])
    print(d(text="发表观点").get_text() + ":" + d.xpath(
        '//android.widget.ListView/android.view.View[13]/android.view.View[3]').get_text())
    publishIntegral = int(
        d.xpath('//android.widget.ListView/android.view.View[13]/android.view.View[3]').get_text()[2])
    print(d(text="本地频道").get_text() + ":" + d.xpath(
        '//android.widget.ListView/android.view.View[14]/android.view.View[3]').get_text())
    localIntegral = int(
        d.xpath('//android.widget.ListView/android.view.View[14]/android.view.View[3]').get_text()[2])
    print(d(text="强国运动").get_text() + ":" + d.xpath(
        '//android.widget.ListView/android.view.View[15]/android.view.View[3]').get_text())
    return readIntegral, listenIntegral, listenTimeIntegral, dailyIntegral, weekIntegral, specialIntegral, challengeIntegral, fourIntegral, doubleIntegral, bookIntegral, shareIntegral, publishIntegral, localIntegral


def daily(d):
    init(d)
    readIntegral, listenIntegral, listenTimeIntegral, dailyIntegral, weekIntegral, specialIntegral, challengeIntegral, fourIntegral, doubleIntegral, bookIntegral, shareIntegral, publishIntegral, localIntegral = getIntegral(
        d)
    challenge, challenge_count_max, challenge_count_min, challenge_delay_max, challenge_delay_min = readconfigAnswer(
        "challenge")
    four, four_count, four_answer_delay,four_delay_max,four_delay_min = readconfigAnswer("four")
    double, double_count,double_answer_delay,double_delay_max,double_delay_min = readconfigAnswer("double")
    local,local_name=readconfigAnswer("local")
    dailyquestion= readconfigAnswer("daily")
    listenaudio=readconfigAnswer("listenaudio")
    readarticle,comment_text,share_name=readconfigAnswer("readarticle")
    print(local_name)
    if challengeIntegral < 6 and challenge == "enable":
        print("开使挑战任务")
        init(d)
        tiaozhandati.tiaozhan(d, challenge_count_min, challenge_count_max, challenge_delay_min, challenge_delay_max)
        print("挑战答题已完成")
    if fourIntegral < 3 and four == "enable":
        print("开始四人答题任务")
        init(d)
        zsydati.zsy(d, four_count, four_answer_delay,four_delay_max,four_delay_min)
        print("四人答题已完成")
    if doubleIntegral < 1 and double == "enable":
        print("开始双人答题任务")
        init(d)
        shuangren(d, double_count)
        print("双人答题已完成")
    if dailyIntegral < 5 and dailyquestion == "enable":
        print("开始每日答题任务")
        init(d)
        meiridati(d)
        print("每日答题已完成")
    if (listenIntegral < 6 or listenTimeIntegral<6) and listenaudio == "enable":
        print("开始视听学习")
        init(d)
        listen_count=max(6-listenIntegral,6-listenTimeIntegral)
        listenaudios(d,listen_count)
        print("视听学习已完成")
    if localIntegral < 1 and local == "enable":
        print("开始本地频道")
        init(d)
        d(text="北京").click()
        time.sleep(2)
        d(text=local_name).click()
        time.sleep(10)
        d.xpath(
            '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.LinearLayout['
            '1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.ImageView[1]').click()
        print("本地频道已完成")
    if readIntegral < 12 and readarticle=="enable":
        print("开始读文章")
        init(d)
        read_count=12-readIntegral
        print(read_count)
        readarticles(d=d,read_count=read_count,commenttext=comment_text,comment_count=2,share_name=share_name,share_count=2,collection_count=2)
        print("读文章已完成")

def test(d):
    for i in range(50):
        tiaozhandati.tiaozhan(d, random.randint(5, 7))
    print("挑战答题测试完成")
    shuangren(d, 30)
    print("挑战答题测试完成")
    # zsy(d, 30)
    print("争上游测试完成")


if __name__ == '__main__':

    # d = u2.connect_usb('emulator-5554')
    username, password,dir = readconfigUser()
    d = appstart.start(user=username, pwd=password,dir=dir)
    if d:
        daily(d)
    else:
        print("应用启动失败")
    init(d)
