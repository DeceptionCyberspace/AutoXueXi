import json
import time

#生成题库
def writequestion(filenname,data):
    with open(filenname, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    time.sleep(2)
    print("生成题库完成")