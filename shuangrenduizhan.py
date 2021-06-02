import json
from datetime import datetime
import random
import time

from uiautomator2.exceptions import XPathElementNotFoundError

import readanswer
import tiaozhandati
import uiautomator2 as u2

import main


# 读题
import zsydati


def read(d):
    question = d.xpath(
        '//*[@resource-id="app"]/android.view.View[1]/android.view.View[3]/android.view.View[1]/android.view.View['
        '1]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View['
        '1]/android.view.View[1]').get_text()

    return question


# 双人
def shuangrendati(d, load_dict):
    i = 1
    unknown = []
    time.sleep(random.randint(1, 3))
    d.xpath(
        '//*[@resource-id="app"]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[4]').click()

    while True:
        try:
            question = read(d)
            if int(str(question.replace(" ", "")[0])) == i:
                print(question)
                if i == 1:
                    sleep = 0
                else:
                    sleep = 0.85
                result, unknown = zsydati.answerTest(d, question, load_dict, sleep, unknown)
                print(result)
                i = i + 1
        except XPathElementNotFoundError as e:
            print("=====================================================")
            time.sleep(10)
            d.xpath('//*[@text=""]').click()
            break
        # if d.xpath('//*[@text="继续挑战"]').exists:
        #     d.xpath('//*[@text=""]').click()
        #     print("退出")
        #     break
    return unknown


def shuangren(d, count):
    unknown = []
    load_dict = tiaozhandati.loadanswer()
    main.init(d)
    d(resourceId="cn.xuexi.android:id/comm_head_xuexi_mine").click()
    time.sleep(5)
    d.xpath(
        '//*[@resource-id="cn.xuexi.android:id/my_recycler_view"]/android.widget.LinearLayout['
        '3]/android.widget.ImageView[1]').click()
    time.sleep(5)
    d.xpath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[3]/android.view.View[10]').click()
    #time.sleep(random.randint(1,3))
    #d.xpath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[4]').click()

    for i in range(0, count):
        # time.sleep(2)
        # d.xpath('//*[@text=""]').click()
        time.sleep(5)
        unknown = shuangrendati(d, load_dict)
        if len(unknown)>0:
            print(unknown)
        time.sleep(random.randint(5, 10))
        if len(unknown) > 0:
            data = tiaozhandati.loadunknown() + unknown
            with open("unknown.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("生成题库...")
            time.sleep(10)
    time.sleep(2)
    d.xpath('//*[@text=""]').click()
    time.sleep(2)
    d.xpath('//*[@text="退出"]').click()
    time.sleep(2)
    d.xpath('//*[@text=""]').click()
    time.sleep(2)
    d.xpath('//*[@text=""]').click()


if __name__ == '__main__':
    d = u2.connect_usb('emulator-5554')
    shuangren(d, 10)
    # shuangrendati(d, tiaozhandati.loadanswer())
