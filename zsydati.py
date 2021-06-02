import json
from datetime import datetime
import random
import time

from uiautomator2.exceptions import XPathElementNotFoundError

import tiaozhandati
import uiautomator2 as u2
import main
import readanswer
import datetime


# 读题
def read(d):
    question = d.xpath(
        '//*[@resource-id="app"]/android.view.View[1]/android.view.View[3]/android.view.View[1]/android.view.View['
        '1]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View['
        '1]/android.view.View[1]').get_text()

    return question


# 答题
def answerTest(d, question, load_dict, sleep, unknown):
    result = "不知道"
    curr_time1 = datetime.datetime.now()
    if (str(question.replace(" ", "")[3:]) == "选择词语的正确词形。" or str(
            question.replace(" ", "")[3:]) == "选择正确的读音。") or None == str(question.replace(" ", "")[3:]):

        time.sleep(sleep)
        options = []
        options_length = len(d.xpath('//android.widget.ListView/android.view.View').all())
        for i in range(0, options_length):
            options.append(str(d.xpath(
                '//android.widget.ListView/android.view.View[' + str(
                    i + 1) + ']/android.view.View[1]/android.view.View[1]').get_text()[3:]))
        for answer in load_dict:
            if answer["options"] == options:
                if str(answer['answer']) == "A":
                    d.xpath('//android.widget.ListView/android.view.View[1]').click()
                    result = str(answer['answer'])
                    break
                if str(answer['answer']) == "B":
                    d.xpath('//android.widget.ListView/android.view.View[2]').click()
                    result = str(answer['answer'])
                    break
                if str(answer['answer']) == "C":
                    d.xpath('//android.widget.ListView/android.view.View[3]').click()
                    result = str(answer['answer'])
                    break
                if str(answer['answer']) == "D":
                    d.xpath('//android.widget.ListView/android.view.View[4]').click()
                    result = str(answer['answer'])
                    break
    else:
        for answer in load_dict:
            if str(answer['content']) == str(question.replace(" ", "")[3:]):
                time.sleep(sleep)
                if str(answer['answer']) == "A":
                    if (str(answer["options"][0]) == str(d.xpath(
                            '//android.widget.ListView/android.view.View[1]/android.view.View[1]/android.view.View[1]').get_text()[
                                                         3:])):
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        result = str(answer['answer']);
                        break;
                if str(answer['answer']) == "B":
                    if (str(answer["options"][1]) == str(d.xpath(
                            '//android.widget.ListView/android.view.View[2]/android.view.View[1]/android.view.View[1]').get_text()[
                                                         3:])):
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        result = str(answer['answer']);
                        break;
                if str(answer['answer']) == "C":
                    if (str(answer["options"][2]) == str(d.xpath(
                            '//android.widget.ListView/android.view.View[3]/android.view.View[1]/android.view.View[1]').get_text()[
                                                         3:])):
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        result = str(answer['answer']);
                        break;
                if str(answer['answer']) == "D":
                    if (str(answer["options"][3]) == str(d.xpath(
                            '//android.widget.ListView/android.view.View[4]/android.view.View[1]/android.view.View[1]').get_text()[
                                                         3:])):
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        result = str(answer['answer']);
                        break;
                if str(answer['answer']) == "挑战不知道":
                    d.xpath('//android.widget.ListView/android.view.View[1]').click()
                    result = str(answer['answer']);
                    break;
                if str(answer['answer']) == "争上游不知道":
                    d.xpath('//android.widget.ListView/android.view.View[1]').click()
                    result = str(answer['answer']);
                    break;
    if result == "不知道":
        options = []
        options_length = len(d.xpath('//android.widget.ListView/android.view.View').all())
        for i in range(options_length):
            options.append(str(d.xpath('//android.widget.ListView/android.view.View[' + str(
                i + 1) + ']/android.view.View[1]/android.view.View[1]').get_text()[3:]))
        data = {
            "category": "争上游答题",
            "content": str(question.replace(" ", "")[3:]),
            "options": options,
            "answer": "争上游不知道",
            "excludes": "",
            "notes": ""
        }
        unknown.append(data)
        time.sleep(sleep)
        d.xpath('//android.widget.ListView/android.view.View[1]').click()
        d.screenshot("./error/" + str(time.time()) + ".jpg")
        result = result
    curr_time2 = datetime.datetime.now()
    # print(curr_time2 - curr_time1, "异常")
    return result, unknown


# zsy答题
def zsydati(d, load_dict, anwser_delay):
    i = 1
    unknown = []
    while (True):

        try:
            question = read(d)
            if int(str(question.replace(" ", "")[0])) == i:
                # print(str(question.replace(" ", "")[0]), i)
                print(question)
                if i == 1:
                    sleep = 0.1
                else:
                    sleep = anwser_delay
                result, unknown = answerTest(d, question, load_dict, sleep, unknown)
                print(result)
                i = i + 1
        except XPathElementNotFoundError as e:
            print("=====================================================")
            time.sleep(10)
            d.xpath('//*[@text=""]').click()
            break

    return unknown


def zsy(d, count, answer_delay, delay_max, delay_min):
    unknown = []
    main.init(d)
    d(resourceId="cn.xuexi.android:id/comm_head_xuexi_mine").click()
    time.sleep(5)
    d.xpath(
        '//*[@resource-id="cn.xuexi.android:id/my_recycler_view"]/android.widget.LinearLayout['
        '3]/android.widget.ImageView[1]').click()
    time.sleep(5)
    d.xpath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[3]/android.view.View[9]').click()
    load_dict = tiaozhandati.loadanswer() + tiaozhandati.loadunknown()
    for i in range(0, count):
        d.xpath('//*[@text="开始比赛"]').click()
        time.sleep(4)
        if d.xpath('//*[@text="知道了"]').exists:
            d.xpath('//*[@text="知道了"]').click()
            return -1
        unknown = zsydati(d, load_dict, answer_delay)
        if len(unknown) > 0:
            print(unknown)
        time.sleep(random.randint(delay_min, delay_max))
        if len(unknown) > 0:
            data = unknown + tiaozhandati.loadunknown()
            with open("unknown.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            time.sleep(20)
            print("生成题库完成")

    d.xpath('//*[@text=""]').click()
    time.sleep(2)
    return count


if __name__ == '__main__':
    d = u2.connect_usb('emulator-5554')
    zsy(d, count=30, answer_delay=0.78, delay_max=8, delay_min=5)
