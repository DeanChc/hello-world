import o
import pandas as pd
import random

o.CNCa.worktime = int(input("CNC的加工时间: "))
one = o.CNCa(1, 1)  # 1号CNC
two = o.CNCa(2, 1)  # 2号CNC
three = o.CNCa(3, 2)  # 3号CNC
four = o.CNCa(4, 2)  # 4号CNC
five = o.CNCa(5, 3)   # 5号CNC
six = o.CNCa(6, 3)  # 6号CNC
seven = o.CNCa(7, 4)  # 7号CNC
eight = o.CNCa(8, 4)  # 8号CNC

o.RGV.washtime = int(input("RGV的清洗时间: "))
o.RGV.work1 = int(input("RGV移动1个单位的时间: "))
o.RGV.work2 = int(input("RGV移动2个单位的时间: "))
o.RGV.work3 = int(input("RGV移动3个单位的时间: "))

t1 = int(input("输入1#、3#、5#、7#每次上下料时间: "))
o.RGV.take1 = t1
t2 = int(input("输入2#、4#、6#、8#每次上下料时间: "))
o.RGV.take2 = t2

R = o.RGV()  # RGV

time = 0  # 开始时间

List0 = [one, two, three, four, five, six, seven, eight]  # CNC序列

i = 0  # 物料计数

L1 = []
L2 = []
L3 = []
L4 = []
L5 = []
L6 = []
L7 = []
L8 = []

for time in range(1, 28800):  # 8小时
    print("第%d时刻 RGV状态：%d  CNC状态: %d %d %d %d %d %d %d %d" % (time, R.state, one.state, two.state, three.state, four.state, five.state, six.state, seven.state, eight.state))
    for t in List0:
        if t.state == 0:  # 如果CNC空闲
            if R.waitlist.count(t) == 0:  # 如果CNC不在等待列表中
                t.need(R)  # CNC发送需求
        elif t.state < 0:
            print("1#_ERROR")  # CNC出错
        else:  # 如果1号CNC在工作
            if t.state <= t.worktime:  # 如果CNC在第二道工序工作时间内
                if random.randint(1, 100 * t.worktime) == 1:  # 1%的概率故障
                    t.wronghappen(time, L5, L6, L7, L8)  # CNC故障
                    t.process = 0
            t.state -= 1  # CNC减去一个单位的工作时间
    if R.state == 0:
        if len(R.waitlist) > 0:
            k = R.waitlist[0]  # 取出等待的CNC
            j = R.waitlist[0].p  # 删除等待的CNC
            for x in R.waitlist:
                if abs(R.place - x.p) < abs(R.place - j):
                    k = x
                elif abs(R.place - x.p) == abs(R.place - j):
                    if x.n % 2 == 0:
                        k = x
                if k.state == 0:
                    w = k  # 锁定等待的CNC
                    R.move(w)  # 移动到等待的CNC
                    i += 1  # 物料计数加1
                    m = w.process
                    w.process = i
                    L1.append(i)   # 写入表格
                    L2.append(w.n)
                    L3.append(time+R.state)
                    if w.process > 8 and m > 0:
                        L4.append(time + R.state)
                    R.take(w)  # 上下料
                    w.work()  # 加工
                    if w.process > 8 and m > 0:  # 已有物料
                        R.wash()  # 清洗
                    R.waitlist.remove(w)     # 删除等待的CNC
                    R.state -= 1
                    break
                else:
                    R.waitlist.remove(k)
    elif R.state < 0:
        print("RGV_ERROR")
    else:
        R.state -= 1   # RGV减去一个单位的工作时间

for i in range(len(L1)-len(L2)):
    L2.append(0)
for i in range(len(L1)-len(L3)):
    L3.append(0)
for i in range(len(L1)-len(L4)):
    L4.append(0)

D = {'物料序号': L1, 'CNC号': L2, '上料开始时间': L3, '下料开始时间': L4}
E = {'故障物料序号': L5, '故障CNC号': L6, '故障开始时间': L7, '故障结束时间': L8}
T = pd.DataFrame(D)
F = pd.DataFrame(E)
T.to_excel("一道工序有故障3.xlsx")  # 保存表格
F.to_excel("一道工序有故障情况3.xlsx")

