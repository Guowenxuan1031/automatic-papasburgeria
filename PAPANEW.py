import pyautogui
import time
import os
import cv2

filenames = os.listdir('E:\\PAPA\\full')
root = 'E:\\PAPA\\full'
print("脚本已启动！")

ham = [12 for a in range(9)]
ticket = [1000 for b in range(10)]
ticRec = [-1 for aa in range(10)]
meatLoc = [0 for c in range(24)]
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
dayNum = 306
baseTime = 16.5
dayBegin = False

def stationClick(num):
    pyautogui.click(760+num*210, 970)
    stationList = ["转到点餐部分","转到烤肉部分","转到制作部分"]
    print(stationList[num])
    time.sleep(0.3)



def dragMeatOn(row, line):
    xpoint = meatX_origin + row * meatX_delta
    ypoint = meatY_origin + line * meatY_delta
    pyautogui.moveTo(400, 700, duration=0.05)
    pyautogui.dragTo(xpoint, ypoint, duration=0.1)
    print("将烤肉移到第" + str(row + 1) + "行，第" + str(line + 1) + "列，时间为" + str(time.time()))


def dragMeatOff(row, line):
    xpoint = meatX_origin + row * meatX_delta
    ypoint = meatY_origin + line * meatY_delta
    pyautogui.moveTo(xpoint, ypoint, duration=0.05)
    pyautogui.dragTo(1445, 300, duration=0.1)
    print("将第" + str(row + 1) + "行，第" + str(line + 1) + "列烤肉移出，时间为" + str(time.time()))


def rotationMeat(row, line):
    xpoint = meatX_origin + row * meatX_delta
    ypoint = meatY_origin + line * meatY_delta
    pyautogui.click(xpoint, ypoint)
    print("将第" + str(row + 1) + "行，第" + str(line + 1) + "列烤肉翻面，时间为" + str(time.time()))

def deleteMeat(num):
    pyautogui.moveTo(1450, 850 - num * 28, duration=0.05)
    pyautogui.dragTo(440, 340, duration=0.1)

foodName1 = ["hamberger-up-pink.png", "tomato-pink.png", "vegetable-pink.png", "onion-pink.png", "cucumber-pink.png",
             "cheese-pink.png", "hamberger-down-pink.png", "", "", "", "redsauce-pink.png", "yellowsauce-pink.png",
             "whitesauce-pink.png", "brownsauce-pink.png", "", "", "", "", "", "", "meat-blue.png", "meat-yellow.png", "meat-red.png"]
foodName2 = ["hamberger-up-white.png", "tomato-white.png", "vegetable-white.png", "onion-white.png", "cucumber-white.png",
             "cheese-white.png", "", "", "", "", "redsauce-white.png", "yellowsauce-white.png",
             "whitesauce-white.png", "brownsauce-white.png", "", "", "", "", "", "", "", "", ""]
def recognizeThing():
    #     for m in range(10):
    #         ticket[m] = 0
    for picture in filenames:
        repreNum = -1
        for foodNameNum in range(23):
            if (picture == foodName1[foodNameNum]) | (picture == foodName2[foodNameNum]):
                repreNum = foodNameNum
                break
        picture = os.path.join(root, picture)
        allpic = []
        if (repreNum >= 10) & (repreNum <= 13):
            allpic = list(pyautogui.locateAllOnScreen(picture, confidence=0.96, region=(1340, 170, 270, 500)))
        elif repreNum != -1:
            allpic = list(pyautogui.locateAllOnScreen(picture, confidence=0.90, region=(1340, 170, 270, 500)))

        if (allpic != []) & (repreNum != -1):
            for allpic1 in allpic:
                indexPic = (620 - allpic1.top) // 50
                ham[indexPic] = repreNum


def dragTicket(num):
    xpoint = 457 + num * 75  # 457-909
    pyautogui.moveTo(1440, 150, duration=0.05)
    pyautogui.dragTo(xpoint, 90, duration=0.1)
    print("将小票拖到第" + str(num + 1) + "位")


def dragTicketOn(num):
    xpoint = 457 + num * 75  # 457-909
    pyautogui.moveTo(xpoint, 90, duration=0.05)
    pyautogui.dragTo(1440, 150, duration=0.1)
    print("将第" + str(num + 1) + "位小票拖至位置")


def dragTicketOrder():
    pyautogui.moveTo(1440, 150, duration=0.15)
    pyautogui.dragTo(694, 700, duration=0.1)


def orderNeed():
    continueBox = pyautogui.locateOnScreen('E:\\PAPA\\full\\continue.png', confidence=0.95)
    if continueBox != None:
        return False
    orderBox = pyautogui.locateOnScreen('E:\\PAPA\\full\\order.png', confidence=0.90, region=(550, 320, 240, 190))
    if orderBox != None:
        print("找到页面中Order")
        return True
    else:
        return False

def continueOn():
    contibox = pyautogui.locateOnScreen('E:\\PAPA\\full\\continue.png', confidence=0.95)
    if contibox != None:
        return True
    else:
        return False


def orderRoutine(orderSitu):
    global orderNum
    for i in range(10):
        if ticket[i] == 1000:
            break
        elif i == 10:
            print("菜单已满，本次不接单")
            return
    pyautogui.click(655, 415)
    print("正在接受点餐")
    while True:
        time.sleep(0.1)
        orderBox = pyautogui.locateOnScreen('E:\\PAPA\\full\\orderSign.png', confidence=0.90)
        if orderBox != None:
            if orderSitu == 1:
                recognizeThing()
            for i in range(10):
                print("ticket", ticket[i])
                print("ticRec", ticRec[i])
            for i in range(10):
                if ticket[i] == 1000:
                    ticket[i] = orderNum
                    dragTicket(i)
                    for k in range(9):
                        print("ham", ham[k])
                        if ham[k] >= 20:
                            if ticRec[i] != ham[k]:
                                ticRec[i] = ticRec[i] + ham[k] + 1
                        ham[k] = 12
                    break
            orderNum = orderNum + 1
            break

def grillRoutine(num, dayState):
    global orderNum
    stationClick(1)
    line = 2
    if num == 21:
        line = 4





    for i in range(3):
        for j in range(line):
            dragMeatOn(i, j)
    startSec = time.time()
    timeDelta = 0
    if dayState == 0:
        stationClick(0)
        if orderNeed():
            orderRoutine(1)
            timeDelta = time.time() - startSec
            print("timeDelta", timeDelta)
        else:
            timeDelta = 0

    else:
        timeDelta = 0
    print("timeDelta-1", timeDelta)
    # sleepTime1 = baseTime*(num-19) - line * 3 * 0.69 - timeDelta
    sleepTime1 = baseTime*(num-19) - timeDelta

    while sleepTime1 > 14:
        startSec = time.time()
        ticketRec = 1000
        ticketOrd = 1100
        # if sleepTime1 > 15:
        for m in range(10):
            for l in range(24):
                # print(ticRec[m], meatLoc[l])
                if ticRec[m] == meatLoc[l]:
                    if ticketOrd > ticket[m]:
                        ticketOrd = ticket[m]
                        ticketRec = m
                    break
        # print(ticketRec)
        if ticketRec != 1000:
            buildRoutine(ticketRec)
        else:
            time.sleep(1)
            if orderNeed():
                orderRoutine(1)
        sleepTime1 = sleepTime1 - (time.time() - startSec)
        print("sleepTime1", sleepTime1)

    if sleepTime1 > 0.3:
        time.sleep(sleepTime1)
    stationClick(1)

    for i in range(3):
        for j in range(line):
            rotationMeat(i, j)

    startSec = time.time()
    timeDelta = 0
    if dayState == 0:
        stationClick(0)
        if orderNeed():
            orderRoutine(1)
            timeDelta = time.time() - startSec
        else:
            timeDelta = 0
    else:
        timeDelta = 0
    print("timeDelta-2", timeDelta)
    # sleepTime2 = baseTime * (num - 19) - line * 3 * 0.69 - timeDelta
    sleepTime2 = baseTime * (num - 19) - timeDelta
    while sleepTime2 > 14:
        startSec = time.time()
        ticketRec = 1000
        ticketOrd = 1100
    # if sleepTime2 > 15:
        for m in range(10):
            for l in range(24):
                # print(ticRec[m], meatLoc[l])
                if ticRec[m] == meatLoc[l]:
                    if ticketOrd > ticket[m]:
                        ticketOrd = ticket[m]
                        ticketRec = m
                    break
        # print(ticketRec)
        if ticketRec != 1000:
            buildRoutine(ticketRec)
        else:
            time.sleep(1)
            if orderNeed():
                orderRoutine(1)
        sleepTime2 = sleepTime2 - (time.time() - startSec)
        print("sleepTime2", sleepTime2)
    if sleepTime2 > 0.3:
        time.sleep(sleepTime2)
    if continueOn():
        return
    stationClick(1)

    pyautogui.click(1450, 900)
    time.sleep(0.2)
    for removeNum in range(24):
        for locLoop in range(24):
            if meatLoc[removeNum] == num:
                deleteMeat(removeNum)
                for rem in range(23):
                    if (rem >= removeNum):
                        meatLoc[rem] = meatLoc[rem + 1]
                meatLoc[23] = 0
            else:
                break
    for i in range(3):
        for j in range(line):
            dragMeatOff(i, j)

    for q in range(24):
        if (meatLoc[q] == 0):
            for p in range(line * 3):
                meatLoc[q + p] = num
            stationClick(0)
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
                grillRoutine(num, 1)
                time.sleep(0.2)
                stationClick(2)
                pyautogui.moveTo(690, 888 - j * 28, duration=0.05)
                #                 pyautogui.dragTo(xPosition, yPosition, duration=0.2)
                break
            if num == meatLoc[j]:
                print("j", j)
                pyautogui.moveTo(690, 888 - j * 28, duration=0.05)
                for m in range(23):
                    if (m >= j):
                        meatLoc[m] = meatLoc[m + 1]
                meatLoc[23] = 0
                break
    print("drag!")
    pyautogui.dragTo(xPosition, yPosition, duration=0.05)


def buildRoutine(buildState):

    stationClick(2)
    minTicketNum = 1000
    minTicketFlag = 0
    for i in range(10):
        print(ticket[i])
        if (ticket[i] < minTicketNum):
            minTicketFlag = i
            minTicketNum = ticket[i]
    if buildState != -1:
        minTicketFlag = buildState
    dragTicketOn(minTicketFlag)
    ticket[minTicketFlag] = 1000
    ticRec[minTicketFlag] = -1
    time.sleep(0.1)
    starttime = time.time()
    recognizeThing()
    print("time5", time.time() - starttime)
    ham[8] = 0
    for i in range(9):
        dragThing(ham[i])
        print("获取到食物" + foodStr[ham[i]])
        if ham[i] == 0:
            break
        time.sleep(0.2)
    for i in range(9):
        ham[i] = 12
    dragTicketOrder()
    time.sleep(10)
    stationClick(0)
    time.sleep(1)


while True:
    orderList = ["continue", "dayContinue", "play"]
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
        for l in range(10):
            ticRec[l] = -1
        dayNum = dayNum + 1

    #         dayBeginSign.png

    emptyBox = pyautogui.locateOnScreen('E:\\PAPA\\full\\empty.png', confidence=0.95)
    if emptyBox != None:
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
        stationClick(1)
        stationClick(2)
        stationClick(0)
        time.sleep(6)
        pyautogui.click(655, 415)
        time.sleep(15)
        dragTicket(0)
        time.sleep(3)
        stationClick(1)
        time.sleep(3)
        dragTicketOn(0)
        time.sleep(3)
        dragMeatOn(1, 2)
        time.sleep(baseTime)
        rotationMeat(1, 2)
        time.sleep(baseTime - 0.2)
        dragMeatOff(1, 2)
        meatLoc[0] = 21
        buildRoutine(-1)
        time.sleep(1)
        print("教程初始化内容完毕...")
        dayBegin = True

    if dayBegin:
        print("今天是第" + str(dayNum) + "天")
        dayBegin = False
        orderNum = 0
        if dayNum == 1:
            baseTime = baseTime / 2
        if dayNum == 2:
            baseTime = baseTime * 2
        if dayNum >= 2:
            for grill in range(6):
                grillRoutine((grill % 3) + 20, 0)
                print("grill", grill)
                contibox = pyautogui.locateOnScreen('E:\\PAPA\\full\\continue.png', confidence=0.95)
                if contibox != None:
                    break

    if orderNeed() & (orderNum < 10):
        orderRoutine(0)
        for i in range(24):
            print(meatLoc[i])
        time.sleep(0.6)
    else:
        for tic in range(10):
            if ticket[tic] != 1000:
                buildRoutine(-1)
                break


    time.sleep(0.1)