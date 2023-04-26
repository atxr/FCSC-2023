from z3 import *
import itertools
import math
from hashlib import sha512
from sys import argv
import qrcode
from PIL import Image
from pyzbar import pyzbar
import numpy as np

def decode_xy():
    imgx = Image.open('x.png')
    imgxinv = Image.open('xinv.png')
    imgy = Image.open('y.png')

    rdx = pyzbar.decode(imgx)[0].data
    rdxinv = pyzbar.decode(imgxinv)[0].data
    rdy = pyzbar.decode(imgy)[0].data

    def decode(rd):
        d = []
        c = -1
        for i in range(len(rd)):
            if rd[i] & 0xc0 == 0xc0:
                c = (rd[i] << 6) & 0xff
            elif c != -1:
                d.append(rd[i] & 0x3f ^ c)
                c = -1
            else:
                d.append(rd[i])

        return bytes(d)

    dx = decode(rdx)
    dx = decode(rdxinv)
    dy = decode(rdy)

    print(dx)
    print(dy)

def cross(l1, l2, i, j, s):
    r = 0
    for k in range(s):
        r += l1[s*i + k]*l2[j + s*k]
        r &= 0xff
    return r

def f(l1, l2, s, v=False):
    B = True
    X2 = [-1] *(s**2) 
    for i in range(s):
        if i % 10 == 0:
            print(f"{i}/{s}")

        for j in range(s):
            r = cross(l1, l2, i, j, s)
            X2[i*8+j] = r
            if i == j:
                B = r == 1 and B
                if v and r != 1:
                    print(f"{i=} {j=} {r=}")
            else:
                B = r == 0 and B
                if v and r != 0:
                    print(f"{i=} {j=} {r=}")

        if v and B == 0:
            print(f"{i=} {j=}")

    return X2, B

def sol(a1, a2, n, t=5):
    s = Solver()
    X = [[Bool(f"x{i}{j}") for j in range(n)] for i in range(n)]

    def avg(l, i, j):
        r = 0
        for k1 in range(i, i+t):
            for k2 in range(j, j+t):
                if l[k1*n + k2]:
                    r += 1
        return r > 0.5

    correctness = [avg(a1, i, j) == X[i][j] for i in range(n//t) for j in range(n//t)]
    constr = f(a1, a2, n)

    s.add(constr)
    s.add(correctness)

def main():
    if len(argv) != 2:
        print("Need username")
        exit(1)

    hash = sha512(argv[1].encode()).digest()

    s = Solver()
    X = [BitVec(f"x{i}", 8) for i in range(64)]
    Y = [BitVec(f"y{i}", 8) for i in range(64)]
    
    X2, _ = f(X, X, 8)

    data_user_c = [hash[i] == X[i] for i in range(64)]
    data_serial_c = [X2[i] == Y[i] for i in range(64)]

    chall_c = data_user_c 
    chall_c += data_serial_c

    s.add(chall_c)
    if s.check() == sat:
        m = s.model()
        x = [m.evaluate(X[i]).as_long() for i in range(64)]
        y = [m.evaluate(Y[i]).as_long() for i in range(64)]

        border = 60
        imgx = qrcode.make(bytes(x), box_size=9, border=0)
        imgy = qrcode.make(bytes(y), box_size=9, border=0)

        arrx = np.array(imgx)
        arry = np.array(imgy)
        farrx = [x for l in arrx for x in l]
        farry = [y for l in arry for y in l]
        n = imgx.get_image().width

        #sol(farrx, farry, n)
        mx = np.asmatrix(arrx)
        mxinv = np.invert(mx)
        mx2 = mx * mx

        Image.fromarray(mxinv).save("xinv.png")
        Image.fromarray(mxinv).save("x2.png")

        """
        over = cross(farrx, farry, 0, 0, n) - 1
        print(over)
        c = 0
        while math.comb(c, over) < border:
            c += 1 
        
        combs = itertools.combinations(range(c), over)
        for i in range(border):
            js = next(combs)
            for j in js:
                arrx[i,j] = False

            
        farrx = [x for l in arrx for x in l]
        farry = [y for l in arry for y in l]
        """

        _, B = f(farrx, farry, n)
        arrx[0][0] = 1
        Image.fromarray(arrx).save("x.png")
        Image.fromarray(arry).save("y.png")
        if B:
            print("WAOUW")

        else:
            print("sorry")

    else:
        print("unsat")
        exit(1)

main()
decode_xy()