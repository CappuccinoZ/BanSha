import pandas as pd
import random


class Game:
    def __init__(self, 杀手, 玩家):
        self.存活 = list(range(玩家))
        self.杀手 = random.sample(self.存活, 杀手)
        self.预言家 = random.choice([i for i in self.存活 if i not in self.杀手])
        self.预言家公开 = False
        self.已查 = [self.预言家]
        self.天数 = 0

    def remove(self, x):
        self.存活.remove(x)
        if x in self.杀手:
            self.杀手.remove(x)
        if x in self.已查:
            self.已查.remove(x)

    def 平民(self):
        return [i for i in self.存活 if i not in self.杀手]

    def 查杀(self):
        return [i for i in self.已查 if i in self.杀手]

    def 查民(self):
        return [i for i in self.已查 if i not in self.杀手]

    def 未查(self):
        return [i for i in self.存活 if i not in self.已查]

    def 刀(self):
        a = self.查民()
        if self.预言家公开 and len(a) != 0:
            t = a[0]
        else:
            t = random.choice(self.平民())
        self.remove(t)
        #print('刀', t)

    def 投(self):
        if not self.预言家公开:
            if ((self.预言家 in self.存活 and self.天数 == 4)
                or (self.预言家 not in self.存活 and self.天数 < 4)
                    or (len(self.查杀()) == len(self.杀手))):
                self.预言家公开 = True
                #print('预言家公开，查', self.已查)
            else:
                t = random.choice(self.存活)
                if t == self.预言家:
                    self.预言家公开 = True
                    #print('预言家公开，查', self.已查)

        if self.预言家公开:
            a = self.查杀()
            if len(a) != 0:
                t = a[0]
            else:
                t = random.choice(self.未查())

        self.remove(t)
        #print('投', t)

    def 查(self):
        if self.预言家 in self.存活 and not self.预言家公开:
            a = self.未查()
            if len(a) > 1:
                t = random.choice(a)
                self.已查.append(t)
                #print('查', t)

    def 判定(self):
        t = len(self.杀手)
        if t == 0 or t == len(self.查杀()):
            #print('平民赢')
            return 1
        elif t << 1 >= len(self.存活):
            #print('杀手赢')
            return 0
        else:
            return -1

    def play(self):
        #print('杀手：', game.杀手)
        while True:
            self.刀()
            if self.判定() != -1:
                return self.判定()

            self.天数 += 1
            #print('进入第{}天，存活：{}'.format(game.天数, game.存活))

            self.投()
            if self.判定() != -1:
                return self.判定()

            self.查()


df = pd.DataFrame(columns=['杀手1', '杀手2', '杀手3', '杀手4'],
                  index=list(range(10, 25)))

for n in range(10, 25):
    for m in range(1, 5):
        a = 0
        b = 10000
        for i in range(b):
            game = Game(m, n)
            a += game.play()
        df.loc[n][m-1] = round(a/b, 2)
        print(n, m, a/b)
print(df)
