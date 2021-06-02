import json
import random
import time

import tiaozhandati
import uiautomator2 as u2

# 读答案
import main
from util import writequestion


def loadanswer():
    with open("daily.json", "r", encoding='UTF-8') as f:
        load_dict = json.load(f)
    return load_dict


# 读题
def read(d):
    question = ""
    category = d.xpath(
        '//*[@resource-id="app"]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]')
    options = d.xpath(
        '//*[@resource-id="app"]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[2]')
    if str(category.get_text()) == "填空题":
        for data in options.all():
            for child in (data.elem.getchildren()):
                if len(child.get("text")) == 0:
                    for i in range(len(child.getchildren()) - 1):
                        question = question + " "
                else:
                    question = question + child.get("text")
    if str(category.get_text()) == "单选题":
        question = d.xpath(
            '//*[@resource-id="app"]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[2]').get_text().replace(
            " ", "").replace(" ", "")
    if str(category.get_text()) == "多选题":
        question = d.xpath(
            '//*[@resource-id="app"]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[2]').get_text().replace(
            " ", "").replace(" ", "")
    return str(category.get_text()), question


# 答题
def answerRight(d,category, question, load_dict, sleep):
    result = "不知道"
    option = "空"
    if category == "填空题":
        index = []
        options = d.xpath(
            '//*[@resource-id="app"]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[2]')
        for data in options.all():
            for child in (data.elem.getchildren()):
                if len(child.get("text")) == 0:
                    index.append(int(child.get("index")) + 1)
                    length = len(child.getchildren()) - 1
                else:
                    continue
        for answer in load_dict:
            if str(answer['content']) == question:
                result = answer['answer']
                time.sleep(random.randint(2, 4))
                answer_next = 0
                for i in range(0, len(index)):
                    d.xpath(
                        '//*[@resource-id="app"]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.view.View[' + str(
                            index[i]) + ']/android.view.View[1]').click()
                    answer_options = d.xpath(
                        '//*[@resource-id="app"]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.view.View[' + str(
                            index[i]) + ']/android.view.View').all()
                    d.set_fastinput_ime(True)  # 切换成FastInputIME输入法
                    d.send_keys(result[answer_next:answer_next + len(answer_options)])  # adb广播输入
                    d.set_fastinput_ime(False)  # 切换成正常的输入法
                    answer_next = answer_next + len(answer_options)

    if category == "单选题":
        for answer in load_dict:
            if str(answer['content']) == question:
                result = answer['answer']
                time.sleep(random.randint(2, 4))
                if str(answer['answer']) == "A":
                    if (str(answer["options"][0]) == str(d.xpath(
                            '//android.widget.ListView/android.view.View[1]/android.view.View[1]/android.view.View[2]').get_text())):
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        result = str(answer['answer']);
                        option = answer["options"][0]
                        break
                if str(answer['answer']) == "B":
                    if (str(answer["options"][1]) == str(d.xpath(
                            '//android.widget.ListView/android.view.View[2]/android.view.View[1]/android.view.View[2]').get_text())):
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        result = str(answer['answer']);
                        option = answer["options"][1]
                        break
                if str(answer['answer']) == "C":
                    if (str(answer["options"][2]) == str(d.xpath(
                            '//android.widget.ListView/android.view.View[3]/android.view.View[1]/android.view.View[2]').get_text())):
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        result = str(answer['answer']);
                        option = answer["options"][2]
                        break
                if str(answer['answer']) == "D":
                    if (str(answer["options"][3]) == str(d.xpath(
                            '//android.widget.ListView/android.view.View[4]/android.view.View[1]/android.view.View[2]').get_text())):
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        result = str(answer['answer']);
                        option = answer["options"][3]
                        break
                if str(answer['answer']) == "每日不知道":
                    time.sleep(sleep)
                    d.xpath('//android.widget.ListView/android.view.View[1]').click()
                    result = str(answer['answer']);
                    option = "空"
                    break
    if category == "多选题":
            for answer in load_dict:
                if str(answer['content']) == question:
                    if str(answer['answer']) == "A":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "AB":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "AC":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "AD":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "AE":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[5]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "AF":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[6]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "ABC":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "ABD":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "ABE":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[5]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "ABF":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[6]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "ACD":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "ACE":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[5]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "ACF":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[6]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "ABCD":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "ABCE":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[5]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "ABCF":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[6]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "ABCDE":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[5]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "ABCDF":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[6]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "ABCDEF":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[1]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[5]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[6]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "B":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "BC":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "BD":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "BE":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[5]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "BF":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[6]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "BCD":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "BCE":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[5]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "BCF":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[6]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "BCDE":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[5]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "BCDF":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[6]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "BCDEF":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[2]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[5]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[6]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "C":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "CD":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "CE":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[5]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "CF":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[6]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "CDE":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[5]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "CDF":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[6]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "CDEF":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[3]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[5]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[6]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "D":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "DE":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[5]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "DF":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[6]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "DEF":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[4]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[5]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[6]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "E":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[5]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "EF":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[5]').click()
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[6]').click()
                        result = str(answer['answer']);
                        break;
                    if str(answer['answer']) == "F":
                        time.sleep(sleep)
                        d.xpath('//android.widget.ListView/android.view.View[6]').click()
                        result = str(answer['answer']);
                        break;

    return result, option, category


# 每日答题
def meiridati_single(d):
    category, question = read(d)
    print(category, question)
    load_dict = loadanswer()+tiaozhandati.loadanswer()
    data=[]
    result, option, category = answerRight(d,category, question, load_dict, 1)
    if result == "不知道":
        time.sleep(1)
        options = []

        options_length = len(d.xpath('//android.widget.ListView/android.view.View').all())
        for i in range(options_length):
            options.append(str(d.xpath('//android.widget.ListView/android.view.View[' + str(
                i + 1) + ']/android.view.View[1]/android.view.View[2]').get_text()))
        if category == "多选题":
            d.xpath('//android.widget.ListView/android.view.View[1]').click()
            time.sleep(1)
            d(text="确定").click()
            answer = d.xpath(
                '//*[@resource-id="app"]/android.view.View[3]/android.view.View[1]/android.view.View[2]/android.view.View[2]').get_text()[
                     6:]
            data = {
                "category": category,
                "content": question,
                "options": options,
                "answer": answer,
                "excludes": "",
                "notes": ""
            }
        if category == "单选题":
            d.xpath('//android.widget.ListView/android.view.View[1]').click()
            time.sleep(1)
            d(text="确定").click()
            time.sleep(1)
            if d(text="查看提示").exists() or d(text="再来一组").exists():
                data = {
                    "category": category,
                    "content": question,
                    "options": options,
                    "answer": 'A',
                    "excludes": "",
                    "notes": ""
                }
            else:
                answer = d.xpath(
                    '//*[@resource-id="app"]/android.view.View[3]/android.view.View[1]/android.view.View[2]/android.view.View[2]').get_text()[
                         6:]
                data = {
                    "category": category,
                    "content": question,
                    "options": options,
                    "answer": answer,
                    "excludes": "",
                    "notes": ""
                }


        if category == "填空题":
            index = []
            options = d.xpath(
                '//*[@resource-id="app"]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[2]')
            for data in options.all():
                for child in (data.elem.getchildren()):
                    if len(child.get("text")) == 0:
                        index.append(int(child.get("index")) + 1)
                        length = len(child.getchildren()) - 1
                    else:
                        continue
            # if len(index)>1:
            #     exit()
            for i in range(0, len(index)):
                d.xpath(
                    '//*[@resource-id="app"]/android.view.View[2]/android.view.View[1]/android.view.View['
                    '1]/android.view.View[2]/android.view.View[' + str(
                        index[i]) + ']/android.view.View[1]').click()
                d.set_fastinput_ime(True)  # 切换成FastInputIME输入法
                d.send_keys("不知道")  # adb广播输入
                d.set_fastinput_ime(False)  # 切换成正常的输入法
            time.sleep(2)
            d(text="确定").click()
            time.sleep(1)
            answer = d.xpath(
                '//*[@resource-id="app"]/android.view.View[3]/android.view.View[1]/android.view.View[2]/android.view.View[2]').get_text()[
                     6:]
            data = {
                "category": category,
                "content": question,
                "options": "空",
                "answer": answer,
                "excludes": "",
                "notes": ""
            }
        if d(text="下一题").exists:
            d(text="下一题").click()
        if d(text="完成").exists:
            d(text="完成").click()
            # d.xpath('//*[@resource-id="app"]/android.view.View[1]').click()
            # time.sleep(1)
            # d(text="退出").click()
    else:
        time.sleep(1)
        d(text="确定").click()
    return result, option, data

def meiridati(d,count=5):
    success=0
    d(resourceId="cn.xuexi.android:id/comm_head_xuexi_mine").click()
    time.sleep(5)
    d.xpath(
        '//*[@resource-id="cn.xuexi.android:id/my_recycler_view"]/android.widget.LinearLayout['
        '3]/android.widget.ImageView[1]').click()
    d.xpath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[3]/android.view.View[3]').click()
    while True:
        unknown_single=[]
        unknown_other=[]
        for i in range(0,5):
                result, option, data = meiridati_single(d)
                if len(data)>0:
                    if data["category"]=="单选题":
                        unknown_single.append(data)
                    else:
                        unknown_other.append(data)
                time.sleep(2)
        writequestion(filenname="daily.json", data=unknown_other + loadanswer())
        writequestion(filenname="unknown.json", data=unknown_single + tiaozhandati.loadunknown())
        time.sleep(3)
        success=success+int(d.xpath('//*[@resource-id="app"]/android.view.View[2]/android.view.View[2]/android.view.View[2]').get_text())
        if success<count:
            d(text="再来一组").click()
        else:
            d(text="返回").click()
            return True


if __name__ == '__main__':
    d = u2.connect_usb('emulator-5554')
    main.init(d)
    meiridati(d,count=100000)
    # d.xpath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[3]/android.view.View[3]').click()
    # while True:
    #     unknown_single=[]
    #     unknown_other=[]
    #     for i in range(0,5):
    #         result, option, data = meiridati_single(d)
    #         if len(data)>0:
    #             if data["category"]=="单选题":
    #                 unknown_single.append(data)
    #             else:
    #                 unknown_other.append(data)
    #         time.sleep(2)
    #     writequestion(filenname="daily.json", data=unknown_other + loadanswer())
    #     writequestion(filenname="unknown2.json", data=unknown_single + tiaozhandati.loadunknown())
    #     time.sleep(3)
    #     if d(text="再来一组").exists:
    #         d(text="再来一组").click()
    #     else:
    #         d.xpath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[3]/android.view.View[3]').click()

    # cat,qu=read(d)
    # print(cat,qu)
    # index = []
    # options = d.xpath(
    #     '//*[@resource-id="app"]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[2]')
    # for data in options.all():
    #     for child in (data.elem.getchildren()):
    #         print(child.get("text"))
    #
    #         if len(child.get("text")) == 0:
    #             index.append(int(child.get("index")) + 1)
    #
    #             length = len(child.getchildren()) - 1
    #         else:
    #             continue
    # # time.sleep(random.randint(2, 4))
    # answertest="镰刀锤子"
    # answer_next = 0
    # for i in range(0,len(index)):
    #
    #     d.xpath(
    #                 '//*[@resource-id="app"]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.view.View[' + str(
    #                     index[i]) + ']/android.view.View[1]').click()
    #     answer_options = d.xpath(
    #         '//*[@resource-id="app"]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.view.View[' + str(
    #                     index[i]) + ']/android.view.View').all()
    #     d.set_fastinput_ime(True)  # 切换成FastInputIME输入法
    #     d.send_keys(answertest[answer_next:answer_next+len(answer_options)])  # adb广播输入
    #     d.set_fastinput_ime(False)  # 切换成正常的输入法
    #     answer_next = answer_next + len(answer_options)


