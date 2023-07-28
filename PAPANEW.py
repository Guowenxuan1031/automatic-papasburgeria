import pyautogui
import time
import os
import cv2

filenames = os.listdir('E:\\PAPA\\full')
root = 'E:\\PAPA\\full'

time.sleep(0.5)
print("脚本已启动！")

ham = [-1 for i in range(9)]
ticket = [1000 for i in range(10)]
meatLoc = [0 for i in range(24)]
foodStr = ["汉堡顶", "西红柿", "生菜", "洋葱卷", "黄瓜", "芝士", "汉堡底", "", "", "", "红酱", "黄酱", "白酱", "棕酱",
           "", "", "", "", "", "", "三分熟", "五分熟", "七分熟"]
# 0 为底 ； 8 为顶
# 汉堡顶 -- 0； 西红柿 -- 1； 生菜 -- 2；洋葱卷 -- 3；黄瓜 -- 4； 芝士 -- 5；汉堡底 -- 6
# 红酱 -- 10； 黄酱 -- 11； 白酱 -- 12； 棕酱 -- 13    1210-1540
# 1/4肉 -- 20； 1/2肉 -- 21； 3/4肉 -- 22     700-1160   300-800
# 888 240   24
# 191 + 50  菜单  -5    186
meatX_origin = 700
meatY_origin = 300
meatX_delta = 230
meatY_delta = 167
xPosition = 975
yPosition = 450
orderNum = 0
dayNum = 1
yellowTime = 30
blueTime = 15
redTime = 45
orderTime = 15
dayBegin = False
startTime = time.time()


def grillStation():
    pyautogui.click(970, 970)
    print("转到烤肉部分")
    time.sleep(0.3)


def buildStation():
    pyautogui.click(1180, 970)
    print("转到制作部分")
    time.sleep(0.2)


def orderStation():
    pyautogui.click(760, 970)
    print("转到点餐部分")
    time.sleep(0.3)


def dragMeatOn(row, line):
    xpoint = meatX_origin + row * meatX_delta
    ypoint = meatY_origin + line * meatY_delta
    pyautogui.moveTo(400, 700, duration=0.15)
    pyautogui.dragTo(xpoint, ypoint, duration=0.15)
    print("将烤肉移到第" + str(row + 1) + "行，第" + str(line + 1) + "列")


def dragMeatOff(row, line):
    xpoint = meatX_origin + row * meatX_delta
    ypoint = meatY_origin + line * meatY_delta
    pyautogui.moveTo(xpoint, ypoint, duration=0.15)
    pyautogui.dragTo(1445, 300, duration=0.15)
    print("将第" + str(row + 1) + "行，第" + str(line + 1) + "列烤肉移出")


def rotationMeat(row, line):
    xpoint = meatX_origin + row * meatX_delta
    ypoint = meatY_origin + line * meatY_delta
    pyautogui.click(xpoint, ypoint)
    print("将第" + str(row + 1) + "行，第" + str(line + 1) + "列烤肉翻面")
    time.sleep(0.3)


def recognizeThing():
    #     for m in range(10):
    #         ticket[m] = 0
    for picture in filenames:
        repreNum = -1
        if (picture == "hamberger-up-pink.png") | (picture == "hamberger-up-white.png"):
            repreNum = 0
        elif (picture == "tomato-pink.png") | (picture == "tomato-white.png"):
            repreNum = 1
        elif (picture == "vegetable-pink.png") | (picture == "vegetable-white.png"):
            repreNum = 2
        elif (picture == "onion-pink.png") | (picture == "onion-white.png"):
            repreNum = 3
        elif (picture == "cucumber-pink.png") | (picture == "cucumber-white.png"):
            repreNum = 4
        elif (picture == "cheese-pink.png") | (picture == "cheese-white.png"):
            repreNum = 5
        elif picture == "hamberger-down-pink.png":
            repreNum = 6
        elif (picture == "redsauce-pink.png") | (picture == "redsauce-white.png"):
            repreNum = 10
        elif (picture == "yellowsauce-pink.png") | (picture == "yellowsauce-white.png"):
            repreNum = 11
        elif (picture == "whitesauce-pink.png") | (picture == "whitesauce-white.png"):
            repreNum = 12
        elif (picture == "brownsauce-pink.png") | (picture == "brownsauce-white.png"):
            repreNum = 13
        elif picture == "meat-blue.png":
            repreNum = 20
        elif picture == "meat-yellow.png":
            repreNum = 21
        elif picture == "meat-red.png":
            repreNum = 22
        picture = os.path.join(root, picture)
        allpic = list(pyautogui.locateAllOnScreen(picture, confidence=0.90))
        if (repreNum >= 10) & (repreNum <= 13):
            allpic = list(pyautogui.locateAllOnScreen(picture, confidence=0.95))

        if (allpic != []) & (repreNum != -1):
            for allpic1 in allpic:
                indexPic = (620 - allpic1.top) // 50
                ham[indexPic] = repreNum


def dragTicket(num):
    xpoint = 457 + num * 75  # 457-909
    pyautogui.moveTo(1440, 150, duration=0.2)
    pyautogui.dragTo(xpoint, 90, duration=0.2)
    print("将小票拖到第" + str(num + 1) + "位")


def dragTicketOn(num):
    xpoint = 457 + num * 75  # 457-909
    pyautogui.moveTo(xpoint, 90, duration=0.2)
    pyautogui.dragTo(1440, 150, duration=0.2)
    print("将第" + str(num + 1) + "位小票拖至位置")


def dragTicketOrder():
    pyautogui.moveTo(1440, 150, duration=0.2)
    pyautogui.dragTo(694, 700, duration=0.2)


def orderNeed():
    continueBox = pyautogui.locateOnScreen('E:\\PAPA\\full\\continue.png', confidence=0.95)
    if continueBox != None:
        return False
    orderBox = pyautogui.locateOnScreen('E:\\PAPA\\full\\order.png', confidence=0.90)
    if orderBox != None:
        print("找到页面中Order")
        return True
    else:
        return False


def orderCheck():
    global orderNum
    for i in range(10):
        if ticket[i] == 1000:
            break
        elif i == 10:
            print("菜单已满，本次不接单")
            return
    pyautogui.click(655, 415)
    print("正在接受点餐")
    # time.sleep(orderTime)



def yellowCheck():
    grillStation()
    for i in range(3):
        for j in range(4):
            dragMeatOn(i, j)
    time.sleep(yellowTime - 3.6)
    for i in range(3):
        for j in range(4):
            rotationMeat(i, j)
    time.sleep(yellowTime - 3.6)
    for i in range(3):
        for j in range(4):
            dragMeatOff(i, j)

    for q in range(24):
        if (meatLoc[q] == 0):
            for p in range(12):
                meatLoc[q + p] = 21
            orderStation()
            break


def blueCheck():
    grillStation()
    for i in range(3):
        for j in range(2):
            dragMeatOn(i, j)
    time.sleep(blueTime - 1.8)
    for i in range(3):
        for j in range(2):
            rotationMeat(i, j)
    time.sleep(blueTime - 1.8)
    for i in range(3):
        for j in range(2):
            dragMeatOff(i, j)
    for q in range(24):
        if (meatLoc[q] == 0):
            for p in range(6):
                meatLoc[q + p] = 20
            orderStation()
            break


def redCheck():
    grillStation()
    for i in range(3):
        for j in range(2):
            dragMeatOn(i, 3 - j)
    time.sleep(redTime - 1.8)
    for i in range(3):
        for j in range(2):
            rotationMeat(i, 3 - j)
    time.sleep(redTime - 1.8)
    for i in range(3):
        for j in range(2):
            dragMeatOff(i, 3 - j)
    for q in range(24):
        if (meatLoc[q] == 0):
            for p in range(6):
                meatLoc[q + p] = 22
            orderStation()
            break


def dragThing(num):
    if num < 10:
        pyautogui.moveTo(432, 300 + num * 95, duration=0.05)
    elif num < 20:
        pyautogui.moveTo(1210 + (num - 10) * 110, 800, duration=0.05)
    else:
        for j in range(24):
            print(str(num) + "  " + str(meatLoc[j]))
            if meatLoc[j] == 0:
                print("j", j)
                if num == 20:
                    blueCheck()
                elif num == 21:
                    yellowCheck()
                elif num == 22:
                    redCheck()
                time.sleep(0.2)
                buildStation()
                pyautogui.moveTo(690, 888 - j * 28, duration=0.1)
                #                 pyautogui.dragTo(xPosition, yPosition, duration=0.2)
                break
            if num == meatLoc[j]:
                print("j", j)
                pyautogui.moveTo(690, 888 - j * 28, duration=0.1)
                for m in range(23):
                    if (m >= j):
                        meatLoc[m] = meatLoc[m + 1]
                meatLoc[23] = 0
                break
    print("drag!")
    pyautogui.dragTo(xPosition, yPosition, duration=0.2)


def buildRoutine():
    buildStation()
    minTicketNum = 1000
    minTicketFlag = 0
    for i in range(10):
        print(ticket[i])
        if (ticket[i] < minTicketNum):
            minTicketFlag = i
            minTicketNum = ticket[i]
    dragTicketOn(minTicketFlag)
    ticket[minTicketFlag] = 1000
    time.sleep(0.1)
    recognizeThing()
    for i in range(9):
        if ham[i] == -1:
            if ham[i-1] == 0:
                break
            else:
                dragThing(0)
                print("识别出现错误，直接出餐")
                time.sleep(0.5)
                break
        dragThing(ham[i])
        print("获取到食物" + foodStr[ham[i]])
        time.sleep(0.2)
    for i in range(9):
        ham[i] = -1
    dragTicketOrder()
    time.sleep(10)
    orderStation()
    time.sleep(1)


while True:

    #         orderCheck
    #         buildRoutine
    orderList = ["continue" , "dayContinue", "play"]
    for order in range(3):
        box = pyautogui.locateOnScreen('E:\\PAPA\\full\\' + orderList[order] + '.png', confidence=0.95)
        if box != None:
            pyautogui.click(box.left + box.width // 2, box.top + box.height // 2)
            print("找到页面中" + orderList[order])
            print(orderList[order], box)
            time.sleep(0.5)

    dayBeginSignBox = pyautogui.locateOnScreen('E:\\PAPA\\full\\dayBeginSign.png', confidence=0.95)
    if (dayBeginSignBox != None) & (dayBegin == False):
        print("找到页面中DayBeginSign")
        dayBegin = True
        time.sleep(4)
        for j in range(10):
            ticket[j] = 1000
        for k in range(24):
            meatLoc[k] = 0
        dayNum = dayNum + 1

    #         dayBeginSign.png

    emptyBox = pyautogui.locateOnScreen('E:\\PAPA\\full\\empty.png', confidence=0.95)
    if emptyBox != None:
        yellowTime = yellowTime / 2
        blueTime = blueTime / 2
        redTime = redTime / 2
        print("找到页面中Empty")
        print("emptyBox", emptyBox)
        print("正在进行教程初始化内容...")
        pyautogui.click(emptyBox.left + emptyBox.width // 2, emptyBox.top + emptyBox.height // 2)
        time.sleep(2)
        pyautogui.typewrite('autoplay', 0.3)
        time.sleep(0.5)
        pyautogui.click(1070, 930)
        print("1...")
        time.sleep(2)
        pyautogui.click(1340, 830)
        time.sleep(8)
        grillStation()
        time.sleep(3)
        buildStation()
        time.sleep(3)
        orderStation()
        time.sleep(6)
        pyautogui.click(655, 415)
        time.sleep(15)
        dragTicket(0)
        time.sleep(3)
        grillStation()
        time.sleep(3)
        dragTicketOn(0)
        time.sleep(3)
        dragMeatOn(1, 2)
        time.sleep(yellowTime)
        rotationMeat(1, 2)
        time.sleep(yellowTime - 0.2)
        dragMeatOff(1, 2)
        meatLoc[0] = 21
        buildRoutine()
        time.sleep(1)
        print("教程初始化内容完毕...")
        dayBegin = True

    if dayBegin:
        print("今天是第" + str(dayNum) + "天")
        if dayNum == 2:
            yellowTime = yellowTime * 2
            blueTime = blueTime * 2
            redTime = redTime * 2
        dayBegin = False
    #         if dayNum >= 5:
    #             redCheck()
    #         if dayNum >= 5:
    #             blueCheck()
    #         if dayNum >= 1:
    #             yellowCheck()

    #         time.sleep(0.2)

    if orderNeed():
        orderCheck()
        while True:
            time.sleep(0.1)
            orderBox = pyautogui.locateOnScreen('E:\\PAPA\\full\\orderSign.png', confidence=0.92)
            if orderBox != None:
                for i in range(10):
                    if ticket[i] == 1000:
                        ticket[i] = orderNum
                        dragTicket(i)
                        break
                orderNum = orderNum + 1
                break
        for i in range(24):
            print(meatLoc[i])
        time.sleep(0.6)
        buildRoutine()

    time.sleep(0.1)