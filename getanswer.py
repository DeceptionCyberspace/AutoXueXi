import time

import uiautomator2 as u2
import tiaozhandati
def read(d):
    question = d.xpath('//*[@resource-id="com.kaoshibaodian.app:id/root_view"]/android.widget.RelativeLayout[1]/android.widget.TextView').get_text()
    return question
def readanswer(d):
    answer=d(resourceId="com.kaoshibaodian.app:id/answerTextView").get_text()[3:]
    return answer
if __name__ == '__main__':
    d = u2.connect_usb('emulator-5554')
    for i in range(1819):
        d.drag(0.17, 0.4, 0.9, 0.4)
        time.sleep(1)
        d.xpath('//*[@resource-id="com.kaoshibaodian.app:id/root_view"]/android.widget.LinearLayout[1]').click()
        time.sleep(1)
        question=read(d)
        dicts= tiaozhandati.loadanswer()
        for answer in dicts:
            if str(answer['content']) == str(question[8:].replace("(　　)","")):
                if answer['answer'] == readanswer(d):
                    print(answer)
                    break
                else:
                    print(answer)
                    break
        d.screenshot("./error/" + str(time.time()) + ".jpg")
        time.sleep(4)

