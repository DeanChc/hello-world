import random


class CNCa:
    worktime = 1

    def __init__(self, number, place):
        self.n = number
        self.p = place
        self.state = 0
        self.process = 0

    def work(self):
        self.state += self.worktime

    def need(self, r):
        if self.state == 0:
            r.waitlist.append(self)

    def wronghappen(self, time, p, n, b, e):
        p.append(self.process)
        n.append(self.n)
        b.append(time)
        self.fix(time, e)

    def fix(self, time, e):
        f = random.randint(600, 1200)
        e.append(time+f)
        self.state += f



class CNCb:
    worktime1 = 1
    worktime2 = 2

    def __init__(self, number, place):
        self.n = number
        self.p = place
        self.state = 0
        self.process = 0    # 当前正在处理的物料

    def need(self, r):
        if self.state == 0:
            if self.n % 2 == 0:
                r.waitlist2.append(self)
            else:
                r.waitlist1.append(self)

    def work(self):
        if self.n % 2 == 0:
            self.state += self.worktime2
        else:
            self.state += self.worktime1

    def wronghappen(self, time, p, n, b, e):
        p.append(self.process)
        n.append(self.n)
        b.append(time)
        self.fix(time, e)

    def fix(self, time, e):
        f = random.randint(600, 1200)
        e.append(time+f)
        self.state += f



class RGV:
    place = 1
    work1 = 1
    work2 = 2
    work3 = 3
    washtime = 1
    take1 = 1
    take2 = 2
    state = 0
    hold = 0    # 持有物料
    waitlist = []  # 工作序列
    waitlist1 = []  # 工作序列1
    waitlist2 = []  # 工作序列2


    def move(self, name):
        if self.place == name.p:
            self.state += 0
            name.state += 0
            self.place = name.p
        elif name.p > self.place:
            if name.p - self.place == 1:
                self.state += self.work1
                name.state += self.work1
                self.place = name.p
            elif name.p - self.place == 2:
                self.state += self.work2
                name.state += self.work2
                self.place = name.p
            else:
                self.state += self.work3
                name.state += self.work3
                self.place = name.p
        else:
            if self.place - name.p == 1:
                self.state += self.work1
                name.state += self.work1
                self.place = name.p
            elif self.place - name.p == 2:
                self.state += self.work2
                name.state += self.work2
                self.place = name.p
            else:
                self.state += self.work3
                name.state += self.work3
                self.place = name.p

    def take(self, name):
        if name.n % 2 == 0:
            self.state += self.take2
            name.state += self.take2
        else:
            self.state += self.take1
            name.state += self.take1

    def wash(self):
        self.state += self.washtime
