import pyautogui
import time
import os
import cv2
import numpy as np

filenames = os.listdir('E:\\PAPA\\full')
root = 'E:\\PAPA\\full'
print("脚本已启动！")


ham = [12 for a in range(9)]
hamRec = [[12 for cc in range(9)]for dd in range(10)]
ticket = [1000 for b in range(10)]
ticRec = [[1200 for aa in range(3)] for bb in range(10)]
meatLoc = [0 for c in range(24)]
foodStr = ["汉堡顶", "西红柿", "生菜", "洋葱卷", "黄瓜", "芝士", "汉堡底", "", "", "", "红酱", "黄酱", "白酱", "棕酱",
           "", "", "", "", "", "", "三分熟", "五分熟", "七分熟"]

dataAll = np.loadtxt(open("papaall.csv","r"),delimiter=",")
print("dataAll.size",dataAll.size)
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
dayNum = 579
baseTime = 15.5
startSec = time.time()
dayBegin = False
dayEnd = False

def stationClick(num):
    pyautogui.click(760+num*210, 970)
    stationList = ["转到点餐部分","转到烤肉部分","转到制作部分"]
    print(stationList[num])
    time.sleep(0.3)



def dragMeatOn(row, line):
    xpoint = meatX_origin + row * meatX_delta
    ypoint = meatY_origin + line * meatY_delta
    pyautogui.moveTo(400, 700, duration=0.01)
    pyautogui.dragTo(xpoint, ypoint, duration=0.01)
    print("将烤肉移到第" + str(row + 1) + "行，第" + str(line + 1) + "列，时间为" + str(time.time()))


def dragMeatOff(row, line):
    xpoint = meatX_origin + row * meatX_delta
    ypoint = meatY_origin + line * meatY_delta
    pyautogui.moveTo(xpoint, ypoint, duration=0.01)
    pyautogui.dragTo(1445, 300, duration=0.01)
    print("将第" + str(row + 1) + "行，第" + str(line + 1) + "列烤肉移出，时间为" + str(time.time()))


def rotationMeat(row, line):
    xpoint = meatX_origin + row * meatX_delta
    ypoint = meatY_origin + line * meatY_delta
    pyautogui.click(xpoint, ypoint)
    print("将第" + str(row + 1) + "行，第" + str(line + 1) + "列烤肉翻面，时间为" + str(time.time()))

def deleteMeat(num):
    pyautogui.moveTo(1450, 850 - num * 28, duration=0.01)
    pyautogui.dragTo(440, 340, duration=0.01)

foodName1 = ["hamberger-up-pink.png", "tomato-pink.png", "vegetable-pink.png", "onion-pink.png", "cucumber-pink.png",
             "cheese-pink.png", "hamberger-down-pink.png", "", "", "", "redsauce-pink.png", "yellowsauce-pink.png",
             "whitesauce-pink.png", "brownsauce-pink.png", "", "", "", "", "", "", "meat-blue.png", "meat-yellow.png", "meat-red.png"]
foodName2 = ["hamberger-up-white.png", "tomato-white.png", "vegetable-white.png", "onion-white.png", "cucumber-white.png",
             "cheese-white.png", "", "", "", "", "redsauce-white.png", "yellowsauce-white.png",
             "whitesauce-white.png", "brownsauce-white.png", "", "", "", "", "", "", "", "", ""]
def recognizeThing():
    global ham
    #     for m in range(10):
    #         ticket[m] = 0
    for hamOri in range(9):
        ham[hamOri] = 12
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

    smallNum = 9
    smallIndex = 0
    for alldata in range(44):
        nowSmallNum = 0
        for alldata2 in range(9):
            if dataAll[alldata][alldata2] - ham[alldata2] != 0:
                nowSmallNum += 1
        if nowSmallNum < smallNum:
            smallNum = nowSmallNum
            smallIndex = alldata
    for dataInt in range(9):
        ham[dataInt] = int(dataAll[smallIndex][dataInt])



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
    ticketCount = 0
    for tickets in range(10):
        if ticket[tickets] != 1000:
            ticketCount += 1
    if ticketCount >= 4:
        print("ticket too much, have to serve")
        return False

    pyautogui.click(655, 415)
    time.sleep(0.5)
    orderBox = pyautogui.locateOnScreen('E:\\PAPA\\full\\order.png', confidence=0.90, region=(1183, 629, 450, 250))
    if orderBox != None:
        print("找到页面中Order")
        while True:
            time.sleep(0.1)
            orderBox = pyautogui.locateOnScreen('E:\\PAPA\\full\\orderSign.png', confidence=0.90, region=(458, 221, 300, 200))
            if orderBox != None:
                recognizeThing()
                break
        return True
    else:
        return False
    # continueBox = pyautogui.locateOnScreen('E:\\PAPA\\full\\dayContinue.png', confidence=0.95)
    # if continueBox != None:
    #     return False

def continueOn():
    contibox = pyautogui.locateOnScreen('E:\\PAPA\\full\\dayContinue.png', confidence=0.95)
    if contibox != None:
        return True
    else:
        return False


def orderRoutine(orderSitu):
    global orderNum
    for i in range(10):
        if ticket[i] == 1000:
            break
        # elif i == 10:
        #     print("菜单已满，本次不接单")
        #     return 0

    print("正在处理点餐")

    for i in range(10):
        print("ticket", ticket[i])
        print("ticRec", ticRec[i])
    for i in range(10):
        if ticket[i] == 1000:
            ticket[i] = orderNum
            for ticr in range(3):
                ticRec[i][ticr] = 0
            time.sleep(1)
            dragTicket(i)
            for k in range(9):
                print("ham", ham[k])
                if ham[k] >= 20:
                    ticRec[i][ham[k] - 20] = ticRec[i][ham[k] - 20] + 1
                hamRec[i][k] = ham[k]
                # ham[k] = 12

            break
    orderNum = orderNum + 1

def grillRoutine(dayState):
    global orderNum, startSec, dayEnd

    for allGrill in range(12):

        if dayEnd:
            print("yes")
            return 0

    # line = 2
    # if num == 21:
    #     line = 4


        # startSec = time.time()
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
        sleepTime1 = baseTime - timeDelta

        if sleepTime1 > 14:
            startSec = time.time()
            print("startSec-SET")
            ticketRec = 1000
            ticketOrd = 1100
            upperCount = [0 for c in range(3)]

            # if sleepTime1 > 15:
            for l in range(24):
                if meatLoc[l] >= 20:
                    upperCount[meatLoc[l] - 20] = upperCount[meatLoc[l] - 20] + 1
            for m in range(10):
                    # print(ticRec[m], meatLoc[l])


                if (upperCount[0] >= ticRec[m][0]) & (upperCount[1] >= ticRec[m][1]) & (upperCount[2] >= ticRec[m][2]):
                    if ticketOrd > ticket[m]:
                        ticketOrd = ticket[m]
                        ticketRec = m
                    # break
            # for upper in range(3):
            #     upperCount[upper] = 0

            # print(ticketRec)
            if ticketRec != 1000:
                buildRoutine(ticketRec)

        sleepTime1 = sleepTime1 - (time.time() - startSec)
        print("sleepTime1", sleepTime1)

        startSec = time.time()
        print("startSec-SET")

        if dayEnd:
            print("yes")
            return 0
        if sleepTime1 > 0.3:
            time.sleep(sleepTime1)
        stationClick(1)



        time.sleep(0.2)
        if allGrill % 2 == 0:
            for f in range(3):
                rotationMeat(f, 0)
        if (allGrill - 1) % 4 == 0:
            for f in range(6):
                rotationMeat(f % 3, 1 + (f // 3))
        if (allGrill - 2) % 6 == 0:
            for f in range(3):
                rotationMeat(f, 3)

        if dayEnd:
            print("yes")
            return 0
        num = 0
        print("allGrill", allGrill)
        if allGrill % 2 == 1:
            print("%2==1?")

            pyautogui.click(1450, 900)
            time.sleep(0.2)
            for numf in range(3):
                if numf == 0:
                    num = 20
                elif numf == 1:
                    if (allGrill == 1) | (allGrill == 9):
                        break
                    elif (allGrill-3) % 4 == 0:
                        num = 21
                    elif allGrill == 5:
                        num = 22
                elif numf == 2:
                    if allGrill == 11:
                        num = 22
                    else:
                        break

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
                print("num", num)
                if num == 20:
                    for f in range(3):
                        dragMeatOff(f, 0)
                        dragMeatOn(f, 0)
                elif num == 21:
                    for f in range(6):
                        dragMeatOff(f % 3, 1 + (f // 3))
                        dragMeatOn(f % 3, 1 + (f // 3))
                elif num == 22:
                    for f in range(3):
                        dragMeatOff(f, 3)
                        dragMeatOn(f, 3)

                for q in range(24):
                    if meatLoc[q] == 0:
                        print("num2", num)
                        if (num == 20) | (num == 22):
                            for p in range(3):
                                print("meatLocnum2", num)
                                meatLoc[q + p] = num
                            break
                        elif num == 21:
                            for p in range(6):
                                print("meatLocnum2", num)
                                meatLoc[q + p] = num
                            break
        if allGrill == 5:
            stationClick(0)
        # break

    # for i in range(3):
    #     for j in range(line):
    #         rotationMeat(i, j)
    #
    # startSec = time.time()
    # timeDelta = 0
    # if dayState == 0:
    #     stationClick(0)
    #     if orderNeed():
    #         orderRoutine(1)
    #         timeDelta = time.time() - startSec
    #     else:
    #         timeDelta = 0
    # else:
    #     timeDelta = 0
    # print("timeDelta-2", timeDelta)
    # # sleepTime2 = baseTime * (num - 19) - line * 3 * 0.69 - timeDelta
    # sleepTime2 = baseTime * (num - 19) - timeDelta
    # while sleepTime2 > 14:
    #     startSec = time.time()
    #     ticketRec = 1000
    #     ticketOrd = 1100
    #     upperCount = [0 for c in range(3)]
    # # if sleepTime2 > 15:
    #     for m in range(10):
    #         for l in range(24):
    #             # print(ticRec[m], meatLoc[l])
    #             if ticRec[m] == meatLoc[l]:
    #                 if ticketOrd > ticket[m]:
    #                     ticketOrd = ticket[m]
    #                     ticketRec = m
    #                 break
    #             elif ticRec[m] > 23:
    #                 for b in range(24):
    #                     if meatLoc[b] > 0:
    #                         upperCount[meatLoc[b] - 20] = 1
    #                     else:
    #                         break
    #                 if upperCount[0] == 1 & upperCount[1] == 1 & upperCount[2] == 1:
    #                     if ticketOrd > ticket[m]:
    #                         ticketOrd = ticket[m]
    #                         ticketRec = m
    #                     break
    #     # print(ticketRec)
    #     if ticketRec != 1000:
    #         buildRoutine(ticketRec)
    #     else:
    #         time.sleep(0.5)
    #
    #         if orderNeed():
    #             orderRoutine(1)
    #     if continueOn():
    #         print("yes")
    #         return 0
    #     sleepTime2 = sleepTime2 - (time.time() - startSec)
    #     print("sleepTime2", sleepTime2)
    #
    # if continueOn():
    #     print("yes")
    #     return 0
    #
    # if sleepTime2 > 0.3:
    #     time.sleep(sleepTime2)
    #
    # stationClick(1)


def dragThing(num):
    if num < 10:
        pyautogui.moveTo(432, 300 + num * 95, duration=0.03)
        # if num != 5:
        #     pyautogui.moveTo(432, 300 + num * 95, duration=0.03)
        # elif num == 5:
        #     pyautogui.moveTo(432, 300 + num * 95, duration=0.03)
    elif num < 20:
        # pyautogui.moveTo(1210 + (num - 10) * 110, 800, duration=0.03)
        if num == 10:
            pyautogui.moveTo(1215, 800, duration=0.03)
        elif num == 11:
            pyautogui.moveTo(1320, 800, duration=0.03)
        elif num == 12:
            pyautogui.moveTo(1426, 800, duration=0.03)
        elif num == 13:
            pyautogui.moveTo(1534, 800, duration=0.03)
    else:
        for j in range(24):
            print(str(num) + "  " + str(meatLoc[j]))
            # if meatLoc[j] == 0:
            #     print("j", j)
            #     grillRoutine(num, 1)
            #     time.sleep(0.2)
            #     stationClick(2)
            #     pyautogui.moveTo(690, 888 - j * 28, duration=0.05)
            #     #                 pyautogui.dragTo(xPosition, yPosition, duration=0.2)
            #     break
            if num == meatLoc[j]:
                print("j", j)
                pyautogui.moveTo(690, 888 - j * 28, duration=0.03)
                for m in range(23):
                    if (m >= j):
                        meatLoc[m] = meatLoc[m + 1]
                meatLoc[23] = 0
                break
    print("drag!")
    pyautogui.dragTo(xPosition, yPosition, duration=0.03)


def buildRoutine(buildState):
    global dayEnd
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
    for tict in range(3):
        ticRec[minTicketFlag][tict] = 1200
    time.sleep(0.1)
    starttime = time.time()
    # recognizeThing()
    ham = hamRec[minTicketFlag]
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
        hamRec[minTicketFlag][i] = 12
    if minTicketNum == 10:
        dayEnd = True
    dragTicketOrder()
    while True:
        time.sleep(0.1)
        moneyBox = pyautogui.locateOnScreen('E:\\PAPA\\full\\money.png', confidence=0.90, region=(1051, 434, 350, 200))
        if moneyBox != None:
            time.sleep(2)
            break


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
            for tice in range(3):
                ticRec[l][tice] = 1200
        for o in range(10):
            for oo in range(9):
                hamRec[o][oo] = 12
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
        dayEnd = False
        print("今天是第" + str(dayNum) + "天")
        dayBegin = False
        orderNum = 0
        stationClick(1)
        startSec = time.time()
        print("startSec-SET")
        for i in range(3):
            for j in range(4):
                dragMeatOn(i, j)
        if dayNum == 1:
            baseTime = baseTime / 2
        if dayNum == 2:
            baseTime = baseTime * 2

        for grill in range(6):
            grillRoutine(0)
            print("grill", grill)
            contibox = pyautogui.locateOnScreen('E:\\PAPA\\full\\dayContinue.png', confidence=0.95)
            if contibox != None:
                break

    # if orderNeed() & (orderNum < 10):
    #     orderRoutine(0)
    #     for i in range(24):
    #         print(meatLoc[i])
    #     time.sleep(0.6)
    # else:
    #     for tic in range(10):
    #         if ticket[tic] != 1000:
    #             buildRoutine(-1)
    #             break


    time.sleep(0.1)