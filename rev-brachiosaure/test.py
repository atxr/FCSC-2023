from z3 import *
import os
import itertools
import math
from hashlib import sha512
from sys import argv
import qrcode
from PIL import Image, ImageOps
from pyzbar import pyzbar
import numpy as np
import time


def get_concat_h(im1, im2):
    dst = Image.new("RGB", (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def get_concat_v(im1, im2):
    dst = Image.new("RGB", (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


def decode_xy():
    imgx = Image.open("x.png")
    imgxinv = Image.open("xinv.png")
    imgy = Image.open("y.png")

    rdx = pyzbar.decode(imgx)[0].data
    rdxinv = pyzbar.decode(imgxinv)[0].data
    rdy = pyzbar.decode(imgy)[0].data

    def decode(rd):
        d = []
        c = -1
        for i in range(len(rd)):
            if rd[i] & 0xC0 == 0xC0:
                c = (rd[i] << 6) & 0xFF
            elif c != -1:
                d.append(rd[i] & 0x3F ^ c)
                c = -1
            else:
                d.append(rd[i])

        return bytes(d)

    dx = decode(rdx)
    dx = decode(rdxinv)
    dy = decode(rdy)

    print(dx)
    print(dy)


def sub_mul(l1, l2, i, j, s):
    r = 0
    for k in range(s):
        r += l1[s * i + k] * l2[j + s * k]
        r &= 0xFF
    return r


def mul(l1, l2, n):
    r = [-1] * (n**2)
    for i in range(n):
        for j in range(n):
            s = 0
            for k in range(n):
                if l1[i * n + k] == 1 and l2[k * n + j] == 1:
                    s = (s + 1) & 0xFF

            r[i * 8 + j] = s

    return r


def sol(a1, a2, n, t=5):
    s = Solver()
    X = [[Bool(f"x{i}{j}") for j in range(n)] for i in range(n)]

    def avg(l, i, j):
        r = 0
        for k1 in range(i, i + t):
            for k2 in range(j, j + t):
                if l[k1 * n + k2]:
                    r += 1
        return r > 0.5

    correctness = [
        avg(a1, i, j) == X[i][j] for i in range(n // t) for j in range(n // t)
    ]
    constr = mul(a1, a2, n)

    s.add(constr)
    s.add(correctness)


def main():
    if len(argv) != 2:
        print("Need username")
        exit(1)

    t0 = time.time()

    hash = sha512(argv[1].encode()).digest()
    hl = np.array(list(hash), dtype=c_uint8)
    hl = hl.reshape(8, 8)
    y = hl @ hl
    yv = y.reshape(1, 64)[0]

    ix = qrcode.make(bytes(hash), box_size=2, border=1).get_image()
    iy = qrcode.make(bytes(y), box_size=2, border=1).get_image()
    n = ix.width
    N = n * n

    ix.save("x.png")
    iy.save("y.png")

    ax = np.asmatrix(ix, "L")
    ay = np.copy(np.asmatrix(iy, "L"))
    lx = ax.reshape(1, n * n).tolist()[0]
    ly = ay.reshape(1, n * n).tolist()[0]

    m = 200
    s = Solver()
    X = [Int(f"x{i}_{j}") for j in range(n + m) for i in range(n + m)]
    Y = [Int(f"y{i}_{j}") for j in range(n + m) for i in range(n + m)]

    s.add(
        [
            And(X[i * n + j] == lx[i * n + j], Y[i * n + j] == ly[i * n + j])
            for i in range(n)
            for j in range(n)
        ]
    )
    s.add(
        [Or(X[i * n + j] == 1, X[i * n + j] == 0) for j in range(n) for i in range(n)]
    )
    s.add(
        [Or(Y[i * n + j] == 1, Y[i * n + j] == 0) for j in range(n) for i in range(n)]
    )

    Z = mul(X, Y, n + m)
    s.add(
        [
            Z[i * n + j] == (1 if i == j else 0)
            for i in range(n + m)
            for j in range(n + m)
        ]
    )

    print(s.check())
    if s.check() == sat:
        m = s.model()
        x = np.array([X[i * n + j].evaluate() for j in range(n) for i in range(n)])
        y = np.array([Y[i * n + j].evaluate() for j in range(n) for i in range(n)])

        Image.fromarray(x).save("x.png")
        Image.fromarray(y).save("y.png")

    else:
        print("unsat")

    print("Time:")
    print(str((time.time() - t0) / 60) + "min")


main()
# decode_xy()
