import datetime
import json
import random
import re
import time

import uiautomator2 as u2
import readanswer

# 读题
import main


def read(d):
    question = d.xpath(
        '//*[@resource-id="app"]/android.view.View[1]/android.view.View[3]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]').get_text()
    return question


# 载入题库
def loadanswer():
    with open("challenge.json", "r", encoding='UTF-8') as f:
        load_dict = json.load(f)
    return load_dict


def loadunknown():
    with open("unknown.json", "r", encoding='UTF-8') as f:
        load_dict = json.load(f)
    return load_dict


# 退出重新开始
def restart(d):
    time.sleep(2)
    count = re.findall(r"\d+\.?\d*", d.xpath('//android.view.View[contains(@text, "答对")]').get_text())[0]
    time.sleep(2)
    d.xpath('//*[@text="结束本局"]').click()
    time.sleep(2)
    d.xpath('//*[@text=""]').click()
    return count


# 答题
def answerRight(d, question, load_dict, sleep):
    result = "不知道"
    option = "空"
    curr_time1 = datetime.datetime.now()
    if str(question.replace(" ", "")) == "选择词语的正确词形。":
        time.sleep(sleep)
        options = []
        options_length = len(d.xpath('//android.widget.ListView/android.view.View').all())
        for i in range(0, options_length):
            options.append(str(d.xpath(
                '//android.widget.ListView/android.view.View[' + str(
                    i + 1) + ']/android.view.View[1]/android.view.View[1]').get_text()))
        print(options)
        for answer in load_dict:
            if answer["options"] == options:
                if str(answer['answer']) == "A":
                    d.xpath('//android.widget.ListView/android.view.View[1]').click()
                    result = str(answer['answer']);
                    option = answer["options"][0]
                    break;
                if str(answer['answer']) == "B":
                    d.xpath('//android.widget.ListView/android.view.View[2]').click()
                    result = str(answer['answer']);
                    option = answer["options"][1]
                    break;
                if str(answer['answer']) == "C":
                    d.xpath('//android.widget.ListView/android.view.View[3]').click()
                    result = str(answer['answer']);
                    option = answer["options"][2]
                    break;
                if str(answer['answer']) == "D":
                    d.xpath('//android.widget.ListView/android.view.View[4]').click()
                    result = str(answer['answer']);
                    option = answer["options"][3]
                    break;
    else:
        for answer in load_dict:
            if str(answer['content']) == str(question.replace(" ", "")):
                if str(answer['answer']) == "A":
                    if (str(answer["options"][0]) == str(d.xpath(
                            '//android.widget.ListView/android.view.View[1]/android.view.View[1]/android.view.View[1]').get_text())):
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        result = str(answer['answer']);
                        option = answer["options"][0]
                        break;
                if str(answer['answer']) == "B":
                    if (str(answer["options"][1]) == str(d.xpath(
                            '//android.widget.ListView/android.view.View[2]/android.view.View[1]/android.view.View[1]').get_text())):
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        result = str(answer['answer']);
                        option = answer["options"][1]
                        break;
                if str(answer['answer']) == "C":
                    if (str(answer["options"][2]) == str(d.xpath(
                            '//android.widget.ListView/android.view.View[3]/android.view.View[1]/android.view.View[1]').get_text())):
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        result = str(answer['answer']);
                        option = answer["options"][2]
                        break;
                if str(answer['answer']) == "D":
                    if (str(answer["options"][3]) == str(d.xpath(
                            '//android.widget.ListView/android.view.View[4]/android.view.View[1]/android.view.View[1]').get_text())):
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        result = str(answer['answer']);
                        option = answer["options"][3]
                        break;
                if str(answer['answer']) == "挑战不知道":
                    time.sleep(sleep)
                    d.xpath('//android.widget.ListView/android.view.View[1]').click()

                    result = str(answer['answer']);
                    option = "空"
                    break;
                if str(answer['answer']) == "争上游不知道":
                    time.sleep(sleep)
                    d.xpath('//android.widget.ListView/android.view.View[1]').click()

                    result = str(answer['answer']);
                    option = "空"
                    break;

    curr_time2 = datetime.datetime.now()
    # if (str(question.replace(" ", "")) == "选择词语的正确词形。"):
    #     print(curr_time2 - curr_time1, "异常")
    # else:
    # print(curr_time2 - curr_time1, "正常")

    return result, option


def answerWrong(d, question, load_dict, sleep):
    result = "不知道"
    option = "空"
    for answer in load_dict:
        if str(answer['content']) == str(question.replace(" ", "")):
            if str(answer['answer']) == "A":
                if (str(answer["options"][0]) == str(d.xpath(
                        '//android.widget.ListView/android.view.View[1]/android.view.View[1]/android.view.View[1]').get_text())):
                    d.xpath('//android.widget.ListView/android.view.View[2]').click()
                    time.sleep(sleep)
                    result = str(answer['answer']);
                    option = answer["options"][0]
                    break;
            if str(answer['answer']) == "B":
                if (str(answer["options"][1]) == str(d.xpath(
                        '//android.widget.ListView/android.view.View[2]/android.view.View[1]/android.view.View[1]').get_text())):
                    d.xpath('//android.widget.ListView/android.view.View[1]').click()
                    time.sleep(sleep)
                    result = str(answer['answer']);
                    option = answer["options"][1]
                    break;
            if str(answer['answer']) == "C":
                if (str(answer["options"][2]) == str(d.xpath(
                        '//android.widget.ListView/android.view.View[3]/android.view.View[1]/android.view.View[1]').get_text())):
                    d.xpath('//android.widget.ListView/android.view.View[1]').click()
                    time.sleep(sleep)
                    result = str(answer['answer']);
                    option = answer["options"][2]
                    break;
            if str(answer['answer']) == "D":
                if (str(answer["options"][3]) == str(d.xpath(
                        '//android.widget.ListView/android.view.View[4]/android.view.View[1]/android.view.View[1]').get_text())):
                    d.xpath('//android.widget.ListView/android.view.View[1]').click()
                    time.sleep(sleep)
                    result = str(answer['answer']);
                    option = answer["options"][3]
                    break;
            if str(answer['answer']) == "争上游不知道":
                d.xpath('//android.widget.ListView/android.view.View[1]').click()
                time.sleep(sleep)
                result = str(answer['answer']);
                option = "空"
                break;
    return result, option


def tiaozhandati(d, times,delay_min,delay_max):
    unknown = []
    # 点击挑战答题

    d.xpath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[3]/android.view.View[11]').click()
    time.sleep(5)
    load_dict = loadanswer() + loadunknown()
    for i in range(times):
        time.sleep(random.randint(delay_min, delay_max))
        question = read(d)
        result, option = answerRight(d, question, load_dict, 0)
        # print(question)
        # print(option)
        # print(result)
        if result == "不知道":
            options = []
            options_length = len(d.xpath('//android.widget.ListView/android.view.View').all())
            for i in range(options_length):
                options.append(str(d.xpath('//android.widget.ListView/android.view.View[' + str(
                    i + 1) + ']/android.view.View[1]/android.view.View[1]').get_text()))
            data = {
                "category": "挑战题",
                "content": str(question.replace(" ", "")),
                "options": options,
                "answer": "争上游不知道",
                "excludes": "",
                "notes": ""
            }
            unknown.append(data)
            time.sleep(random.randint(delay_min, delay_max))
            d.xpath('//android.widget.ListView/android.view.View[1]').click()
            time.sleep(1)
            d.screenshot("./error/" + str(time.time()) + ".jpg")
            time.sleep(4)
            if ((d.xpath('//*[@text="挑战结束"]').exists)):
                # print(question)
                # print(options)
                # print(result)
                count = restart(d)
                return int(count), unknown;

        if ((d.xpath('//*[@text="挑战结束"]').exists)):
            # print(question)
            # print(result)
            # print(option)
            count = restart(d)
            return int(count), unknown;
    time.sleep(2)
    while (True):
        question = read(d)
        result, option = answerWrong(d, question, load_dict, 0)
        time.sleep(2)
        if d.xpath('//*[@text="挑战结束"]').exists:
            print(question)
            print(result)
            print(option)
            count = restart(d)
            return int(count), unknown


def tiaozhan(d, count_max,count_min,delay_max,delay_min):
    success = 0
    d(resourceId="cn.xuexi.android:id/comm_head_xuexi_mine").click()
    time.sleep(5)
    d.xpath(
        '//*[@resource-id="cn.xuexi.android:id/my_recycler_view"]/android.widget.LinearLayout['
        '3]/android.widget.ImageView[1]').click()
    time.sleep(5)
    count = random.randint(count_min,count_max)
    while (success < count):
        success, unknown = tiaozhandati(d, count,delay_min,delay_max)
        # print(unknown)
        # print(success)
        if len(unknown) > 0:
            data = unknown + loadunknown()
            with open("unknown.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            time.sleep(20)
            print("生成题库完成")


if __name__ == '__main__':
    d = u2.connect_usb('emulator-5554')
    main.init(d)
    tiaozhan(d,3000,3000,4,2)
