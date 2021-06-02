import json
import random

import uiautomator2 as u2
import time

import main
import tiaozhandati
from util import writequestion


def loadalready():
    with open("article.json", "r", encoding='UTF-8') as f:
        load_dict = json.load(f)
    return load_dict


def hasred(title):
    articles = loadalready()
    for article in articles:
        if article['title'] == title:
            return True
    return False


def readarticle(d):
    for i in range(10):
        d(scrollable=True).scroll.forward()
        time.sleep(random.randint(6,7))

def comment(d,commenttext):
    d.xpath('//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]').click()
    time.sleep(random.uniform(0.5,1))
    d.set_fastinput_ime(True)  # 切换成FastInputIME输入法
    d.send_keys(commenttext)  # adb广播输入
    d.set_fastinput_ime(False)  # 切换成正常的输入法
    time.sleep(random.uniform(0.5,1))
    d.xpath('//*[@text="发布"]').click()
    time.sleep(1)

def collection(d):
    d.xpath('//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]/android.widget.ImageView[1]').click()
    time.sleep(1)


def share(d,name):
    d.xpath('//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]/android.widget.ImageView[2]').click()
    time.sleep(random.uniform(0.5,1))
    d.xpath('//android.widget.GridView/android.widget.RelativeLayout[1]/android.widget.ImageView[1]').click()
    time.sleep(random.uniform(0.5,1))
    d.xpath('//*[@resource-id="cn.xuexi.android:id/view_search"]').click()
    time.sleep(random.uniform(0.5,1))
    d.set_fastinput_ime(True)  # 切换成FastInputIME输入法
    d.send_keys(name)  # adb广播输入
    d.set_fastinput_ime(False)  # 切换成正常的输入法
    time.sleep(random.uniform(0.5,1))
    d.xpath('//*[@resource-id="cn.xuexi.android:id/extend_list_view"]/android.widget.RelativeLayout[1]').click()
    time.sleep(random.uniform(0.5,1))
    d.xpath('//*[@resource-id="android:id/button1"]').click()
    time.sleep(1)

#不忘初心牢记使命
def readarticles(d, read_count,commenttext,comment_count,share_name,share_count,collection_count):
    d.xpath('//*[@resource-id="cn.xuexi.android:id/comm_search_view"]').click()
    time.sleep(random.uniform(0.5,1))
    d.set_fastinput_ime(True)  # 切换成FastInputIME输入法
    d.send_keys("时评")  # adb广播输入
    d.set_fastinput_ime(False)  # 切换成正常的输入法
    time.sleep(random.uniform(0.5,1))
    d.press("enter")
    time.sleep(random.uniform(2,3))
    d.xpath(
        '//*[@resource-id="app"]/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]').click()
    time.sleep(random.uniform(2,3))

    alreadyread = []
    succeed = 0
    while succeed<read_count:

        option_length = len(d.xpath('//android.widget.ListView/android.widget.FrameLayout').all())
        for i in range(1, option_length):
            try:
                title = d.xpath('//android.widget.ListView/android.widget.FrameLayout[' + str(
                    i) + ']/android.widget.LinearLayout[1]/android.widget.TextView[1]').get_text()

                if not hasred(title):
                    print(title)

                    d.xpath('//android.widget.ListView/android.widget.FrameLayout[' + str(
                        i) + ']/android.widget.LinearLayout[1]/android.widget.TextView[1]').click()
                    readarticle(d)
                    if succeed<comment_count:
                        comment(d,commenttext)
                    if succeed<share_count:
                        share(d,share_name)
                    # if succeed < collection_count:
                    #     collection(d)
                    succeed = succeed + 1
                    data = {
                        "title": title,
                    }
                    d.xpath('//*[@resource-id="cn.xuexi.android:id/TOP_LAYER_VIEW_ID"]/android.widget.ImageView[1]').click()

                    alreadyread.append(data)
                    writequestion(filenname="article.json", data=alreadyread + loadalready())
                    time.sleep(2)
                    print(succeed)
                    if succeed>=read_count:
                        break
            except:
                continue
        d(scrollable=True).scroll.forward()
    d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.ImageView[1]').click()
    time.sleep(1)
    d.xpath('//*[@resource-id="cn.xuexi.android:id/search_back"]').click()
    time.sleep(1)
    d.xpath('//*[@resource-id="cn.xuexi.android:id/search_back"]').click()




def listenaudios(d, count):
    d.xpath(
        '//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_ding"]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]').click()
    time.sleep(3)
    d.xpath(
        '//android.widget.ListView/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]').click()
    for i in range(0, count):
        d(scrollable=True).scroll.forward()
        time.sleep(random.randint(65, 75))
    d(resourceId="cn.xuexi.android:id/iv_back").click()


if __name__ == '__main__':
    d = u2.connect_usb('emulator-5554')
    main.init(d)
    readarticles(d, 20,"不忘初心牢记使命",2,"周晓",2,2)
