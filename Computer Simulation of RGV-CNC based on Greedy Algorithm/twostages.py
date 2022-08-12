import o
import pandas as pd
import random

o.CNCb.worktime1 = int(input("CNC的第一道工序加工时间: "))
o.CNCb.worktime2 = int(input("CNC的第二道工序加工时间: "))
one = o.CNCb(1, 1)  # 1号CNC
two = o.CNCb(2, 1)  # 2号CNC
three = o.CNCb(3, 2)  # 3号CNC
four = o.CNCb(4, 2)  # 4号CNC
five = o.CNCb(5, 3)   # 5号CNC
six = o.CNCb(6, 3)  # 6号CNC
seven = o.CNCb(7, 4)  # 7号CNC
eight = o.CNCb(8, 4)  # 8号CNC

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

L1 = []  # 物料编号
L2 = []  # 第一道工序的加工CNC编号
L3 = []  # 第一道工序上料时间
L4 = []  # 第一道工序下料时间
L5 = []  # 第二道工序的加工CNC编号
L6 = []  # 第二道工序上料时间
L7 = []  # 第二道工序下料时间
L8 = []  # 故障物料编号
L9 = []  # 故障CNC编号
L10 = []  # 故障开始时间
L11 = []  # 故障结束时间


i = 0  # 物料计数
for time in range(1, 28800):  # 8小时
    print("第%d时刻 RGV状态：%d  CNC状态: %d %d %d %d %d %d %d %d\n" % (time, R.state, one.state, two.state, three.state, four.state, five.state, six.state, seven.state, eight.state))
    for t in List0:
        if t.state == 0:  # 如果CNC空闲
            if R.waitlist1.count(t) == 0 and R.waitlist2.count(t) == 0:  # 如果CNC不在等待列表中
                t.need(R)  # CNC发送需求
        elif t.state < 0:
            print("1#_ERROR\n")  # CNC出错
        else:  # 如果CNC在工作
            if t.n % 2 == 0:  # 如果CNC在第二道工序工作
                  if t.state <= t.worktime2:  # 如果CNC在第二道工序工作时间内
                    if random.randint(1, 100 * t.worktime2) == 1:  # 1%的概率故障
                        t.wronghappen(time, L8, L9, L10, L11)  # CNC故障
                        t.process = 0
            else:
                if t.state <= t.worktime1:
                    if random.randint(1, 100 * t.worktime1) == 1:
                        t.wronghappen(time, L8, L9, L10, L11)
                        t.process = 0
            t.state -= 1  # CNC减去一个单位的工作时间
    if R.state == 0:
        if R.hold == 0:
            if len(R.waitlist1) > 0:  # 第一道工序
                k = R.waitlist1[0]
                j = k.p
                for x in R.waitlist1:
                    if abs(R.place - x.p) < abs(R.place - j):
                        k = x
                    elif abs(R.place - x.p) == abs(R.place - j):
                        if x.n % 2 > 0:
                            k = x
                    if k.state == 0:  # 有等待的CNC
                        w = k  # 锁定等待的CNC
                        R.move(w)  # 移动到等待的CNC
                        i += 1  # 物料计数加1
                        m = w.process
                        w.process = i
                        L1.append(i)
                        L2.append(w.n)
                        L3.append(time+R.state)
                        if w.process > 4 and m > 0:
                            R.hold = 1  # 持有物料
                            L4.append(time+R.state)
                        R.take(w)  # 上下料
                        w.process = i  # CNC开始工作
                        w.work()  # 加工
                        R.waitlist1.remove(w)    # 删除等待的CNC
                        R.state -= 1
                        break
                    else:
                        R.waitlist1.remove(k)  # 删除等待的CNC
        else:
            if len(R.waitlist2) > 0:   # 第二道工序
                for x in R.waitlist2:
                    k = R.waitlist2[0]
                    j = k.p
                    if abs(R.place - x.p) < abs(R.place - j):
                        k = x
                    elif abs(R.place - x.p) == abs(R.place - j):
                        if x.n % 2 > 0:
                            k = x
                    if k.state == 0:
                        z = k  # 锁定等待的CNC
                        m = z.process
                        z.process = i-4
                        R.move(z)
                        L5.append(z.n)
                        L6.append(time + R.state)
                        if z.process > 4 and m > 0:
                            L7.append(time + R.state)
                        R.take(z)
                        z.work()
                        R.waitlist2.remove(z)
                        R.hold = 0
                        if z.process > 4 and m > 0:
                            R.wash()
                        R.state -= 1
                        break
                    else:
                        R.waitlist2.remove(k)
    elif R.state < 0:
        print("RGV_ERROR\n")
    else:
        R.state -= 1  # RGV减去一个单位的工作时间
# 填补空缺
for i in range(len(L1)-len(L2)):
    L2.append(0)
for i in range(len(L1)-len(L3)):
    L3.append(0)
for i in range(len(L1)-len(L4)):
    L4.append(0)
for i in range(len(L1)-len(L5)):
    L5.append(0)
for i in range(len(L1)-len(L6)):
    L6.append(0)
for i in range(len(L1)-len(L7)):
    L7.append(0)
D = {'物料序号': L1, '第一道工序CNC号': L2, '第一道工序上料开始时间': L3, '第一道工序下料开始时间': L4, '第二道工序CNC号': L5, '第二道工序上料开始时间': L6, '第二道工序下料开始时间': L7}
E = {'故障物料编号': L8, '故障CNC编号': L9, '故障开始时间': L10, '故障结束时间': L11}
T = pd.DataFrame(D)
F = pd.DataFrame(E)
T.to_excel("两道程序有故障3.xlsx")  # 保存表格
F.to_excel("故障情况二3.xlsx")  # 保存表格
