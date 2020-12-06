import random, copy
from math import sqrt

class Matrix:
    def __init__(self, width=0, height=0, homogeneous=False, value=7, ls=[], coordinates=[0,0]):
        self.body = []
        self.maxValLen = len(str(value))
        self.width = width
        self.height = height
        self.coordinates = coordinates
        if len(ls) == 0:
            if homogeneous:
                for i in range(height):
                    temp = []
                    for j in range(width):
                        temp.append(value)
                    self.body.append(temp)
            else:
                n = 0
                for i in range(height):
                    temp = []
                    for j in range(width):
                        n += 1
                        temp.append(n)
                    self.body.append(temp)
        else:
            self.body.extend(ls)
            

    def matrixToString(self):
        if type(self.body[0]) == int:
                for i in self.body:
                    lenght = len(str(i))
                    if lenght > self.maxValLen:
                        self.maxValLen = lenght
        else:    
            for i in self.body:
                for j in i:
                    lenght = len(str(j))
                    if lenght > self.maxValLen:
                        self.maxValLen = lenght
        s = ""
        if type(self.body[0]) != int:
            for i, o in enumerate(self.body):
                for j, oo in enumerate(o):
                    val = str(oo)
                    s += val + " "
                    if len(val) < self.maxValLen:
                        for i in range(self.maxValLen - len(val)):
                            s += " "
                s += "\n"
        else:
            for i in self.body:
                s += str(i) + " "
        return s

    def transpose(self):
        '''
        поворачивает матрицуц по диагонали
        '''
        ls = []
        if type(self.body[0]) != int:
            for i in range(len(self.body[0])):
                ls.append([])

            for i in self.body:
                for j in range(len(i)):
                    ls[j].append(i[j])
            self.body = ls
        else:
            print("одномерный список не подходит")

    def fill(self, value):
        if type(self.body[0]) == int:
            for i in range(len(self.body)):
                self.body[i] = value
        else:
            for i in range(len(self.body)):
                for j in range(len(self.body[i])):
                    self.body[i][j] = value

    def rectangle(self, x, y, w, h, value=1):
        for i in range(0,h):
            for j in range(0,w):
                if (0 <= i+y < len(self.body) and 
                    0 <= j+x < len(self.body[0])):
                    self.body[y+i][x+j] = value

    def circle(self, x, y, r, value, k=1):
        print(type(r), type(k))
        for i in range(int(-r/k-2), int(r/k+3)):
            for j in range(-r-2, r+3):
                if (sqrt(i*i*k + j*j) < r and
                    0 <= i+y < len(self.body) and 
                    0 <= j+x < len(self.body[0])):
                        self.body[i+y][j+x] = value

    def flatten(self):
        ls = []
        for i in range(len(self.body)):
            ls.extend(self.body[i])
        self.body = ls

    def shuffle(self):
        lenX = len(self.body)
        lenY = len(self.body[0])
        if type(self.body[0]) == int:
            random.shuffle(self.body)
        else:
            for i in range(lenX):
                for j in range(lenY):
                    x = random.randint(0, lenX-1)
                    y = random.randint(0, lenY-1)
                    self.body[i][j], self.body[x][y] = self.body[x][y], self.body[i][j]        

    def reshape(self, width, height):
        if type(self.body[0]) == int:
            lenght = len(self.body)
        else:
            lenght = len(self.body) * len(self.body[0])

        if width*height != lenght:
            print("неподходящий размер матрицы")
        else:
            if type(self.body[0]) != int:
                self.flatten()
            ls = []
            n = 0
            for i in range(height):
                ls.append([])
                for j in range(width):
                    if n < lenght:
                        ls[i].append(self.body[n])
                        n += 1
                    else:
                        break
            self.body = ls
        
    def glue(self, m):
        y, x = m.coordinates
        #print(y, x)
        h, w = m.height, m.width
        for i, o in enumerate(m):
            for j, oo in enumerate(o):
                self.body[i+y][j+x] = oo

    def matrixJoiner(self, ml, symbols="./^<—+|\\>L?-*:JZxbM"):
        #symbols = "./^<—+|\\>L?-*:JZxbM"
        for i, o in enumerate(ml):
            o.fill(symbols[i:i+1])
            o.bordürtschiki(value="#")
            self.glue(o)

    def bordürtschiki(self, value=0):
        w = self.width
        h = self.height
        self.rectangle(0, 0, w, 1, value)
        self.rectangle(0, h-1, w, 1, value)
        self.rectangle(0, 1, 1, h, value)
        self.rectangle(w-1, 1, 1, h, value)


    def copy(self):
        return copy.deepcopy(self.body)

    def __str__(self):
        return self.matrixToString()

    def __add__(self, other):
        for i,o in enumerate(self.body):
            for j,oo in enumerate(o):
                self.body[i][j] = oo + other
        return Matrix(ls=self.body)

    def __radd__(self, other):
        for i,o in enumerate(self.body):
            for j,oo in enumerate(o):
                self.body[i][j] = other + oo
        return Matrix(ls=self.body)

    def __sub__(self, other):
        for i,o in enumerate(self.body):
            for j,oo in enumerate(o):
                self.body[i][j] = oo - other
        return Matrix(ls=self.body)

    def __rsub__(self, other):
        for i,o in enumerate(self.body):
            for j,oo in enumerate(o):
                self.body[i][j] = other - oo
        return Matrix(ls=self.body)
    
    def __len__(self):
        return len(self.body)
    
    def __getitem__(self, key):
        return self.body[key]
    
    def __setitem__(self, key, value):
        self.body[key] = item
        
    #def __iter__(self):
        #return iter(self.body)


def concantenator(matrixList, axis=0):
    """
    эта штука соединяет матрицы
    """
    tempList = []
    if axis == 0:
        for i in matrixList:
            tempList.extend(i.body)

    elif axis == 1:
        for i in range(len(matrixList[0].body)):
            tempList.append([])

        for i in range(len(matrixList[0].body)):
            for j in matrixList:
                tempList[i].extend(j.body[i])
    return Matrix(ls=tempList)


def summatorz(la, lb, a=1):
    '''
    сложение матриц
    '''
    t = Matrix(ls=lb.copy())
    l = min(len(la), len(la[0]), len(lb), len(lb[0]))
    if a == 1:
        for i in range(0, l):
            t[i][i] += la[i][i]
    elif a == 2:
        k = len(t[0])-1
        for i in range(0, l):
            t[i][k-i] += la[i][l-1-i]
    return t

def subtractorz(la, lb, a=1):
    '''
    вычитает из первой матрицы вторую
    '''
    t = Matrix(ls=lb.copy())
    l = min(len(la), len(la[0]), len(lb), len(lb[0]))
    if a == 1:
        for i in range(0, l):
            t[i][i] -= la[i][i]
    elif a == 2:
        k = len(t[0])-1
        for i in range(0, l):
            t[i][k-i] -= la[i][l-1-i]
    return t

def multiplierz(la, lb, a=1):
    '''
    умножает матрицы
    '''
    t = Matrix(ls=lb.copy())
    l = min(len(la), len(la[0]), len(lb), len(lb[0]))
    if a == 1:
        for i in range(0, l):
            t[i][i] *= la[i][i]
    elif a == 2:
        k = len(t[0])-1
        for i in range(0, l):
            print(i, k-i)
            print(t[i][k-i])
            t[i][k-i] *= la[i][l-1-i]
    return t

def dividerz(la, lb, a=1):
    '''
    делит матрицы
    '''
    t = Matrix(ls=lb.copy())
    l = min(len(la), len(la[0]), len(lb), len(lb[0]))
    if a == 1:
        for i in range(0, l):
            t[i][i] //= la[i][i]
    elif a == 2:
        k = len(t[0])-1
        for i in range(0, l):
            t[i][k-i] //= la[i][l-1-i]
    return t

def exponentiatorz(la, lb, a=1):
    '''
    водит числаиз первой матрицы в степени из второй матрицы
    '''
    tmat = Matrix(ls=lb.copy())
    l = min(len(la), len(la[0]), len(lb), len(lb[0]))     
    if a == 1:
        for i in range(0, l):
            t = tmat[i][i]
            for j in range(la[i][i] - 1):
                tmat[i][i] *= t
    elif a == 2:
        k = len(t[0])-1
        for i in range(0, l):
            t = tmat[i][k-i]
            for j in range(la[i][l-1-i] - 1):
                tmat[i][k-i] *= t
    return tmat

def turner(matrix, a=1):
    '''
    поворачивает матрицу на a*90 градусов
    '''
    if a == 1:
        tm = Matrix(len(matrix), len(matrix[0]))
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                tm[x][-y-1] = matrix[y][x]
    elif a == -1:
        tm = Matrix(len(matrix), len(matrix[0]))
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                tm[-x-1][y] = matrix[y][x]
    elif a in (2, -2):
        tm = copy.deepcopy(matrix)
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                tm[len(matrix)-y-1][len(matrix[0])-x-1] = matrix[y][x]
    elif a == 0:
        tm = copy.deepcopy(matrix)
    return tm
