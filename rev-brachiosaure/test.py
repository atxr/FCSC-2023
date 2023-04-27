from hashlib import sha512
import qrcode
from PIL import Image
from ctypes import *

# from pyzbar import pyzbar
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


# def decode_xy():
#     imgx = Image.open("x.png")
#     imgxinv = Image.open("xinv.png")
#     imgy = Image.open("y.png")

#     rdx = pyzbar.decode(imgx)[0].data
#     rdxinv = pyzbar.decode(imgxinv)[0].data
#     rdy = pyzbar.decode(imgy)[0].data

#     def decode(rd):
#         d = []
#         c = -1
#         for i in range(len(rd)):
#             if rd[i] & 0xC0 == 0xC0:
#                 c = (rd[i] << 6) & 0xFF
#             elif c != -1:
#                 d.append(rd[i] & 0x3F ^ c)
#                 c = -1
#             else:
#                 d.append(rd[i])

#         return bytes(d)

#     dx = decode(rdx)
#     dx = decode(rdxinv)
#     dy = decode(rdy)

#     print(dx)
#     print(dy)


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
                s += (l1[i * n + k] * l2[k * n + j]) % 256

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


def main(username):
    t0 = time.time()

    hash = sha512(username.encode()).digest()
    hl = np.array(list(hash), dtype=c_uint8)
    hl = hl.reshape(8, 8)
    y = hl @ hl
    yv = y.reshape(1, 64)[0]

    ix = qrcode.make(bytes(hash), box_size=2, border=4).get_image()
    iy = qrcode.make(bytes(y), box_size=2, border=4).get_image()
    n = ix.width
    N = n * n

    ix.save("x.png")
    iy.save("y.png")

    ax = np.asmatrix(np.zeros((n, n), dtype=c_uint8))
    ay = np.asmatrix(np.zeros((n, n), dtype=c_uint8))
    for i in range(n):
        for j in range(n):
            ax[i, j] = ix.getpixel((i, j))
            ay[i, j] = iy.getpixel((i, j))

    lx = ax.reshape(1, n * n).tolist()[0]
    ly = ay.reshape(1, n * n).tolist()[0]

    tmp = [0] * (n * n)
    for i in range(n):
        for j in range(n):
            tmp[i * n + j] = (256 - lx[n * i + j]) & 0xFF
    lx = tmp

    def mat_equ(a, b):
        for i in range(n):
            for j in range(n):
                if a[i, j] != b[i, j]:
                    return False
        return True

    def get_last_nilp(m):
        n = m.shape[0]
        z = np.zeros((n, n))
        t = np.copy(m)
        for order in range(n):
            tmp = t * m
            if mat_equ(tmp, z):
                print(f"nilp order {order=}")
                break
            t = tmp

        return t

    Xn = get_last_nilp(ax)
    Yn = get_last_nilp(ay)

    fin = np.asmatrix(np.eye(n * 4, dtype=c_uint8))
    finv = np.asmatrix(np.eye(n * 4, dtype=c_uint8))

    for i in range(n):
        for j in range(n):
            fin[i + 2 * n, j] = ax[i, j]
            fin[i + 3 * n, j + n] = -ay[i, j]
            finv[i + 2 * n, j] = -ax[i, j]
            finv[i + 3 * n, j + n] = ay[i, j]

            fin[i, j + 3 * n] = Xn[i, j]
            fin[i + n, j + 3 * n] = -Yn[i, j]
            finv[i, j + 3 * n] = -Xn[i, j]
            finv[i + n, j + 3 * n] = Yn[i, j]

    print(fin)
    print("==================")
    print(finv)

    print(mat_equ(fin @ finv, np.eye(n * 2, dtype=c_uint8)))

    Image.fromarray(fin).save("out/fin.png")
    Image.fromarray(finv).save("out/finv.png")

    return

    s = Solver()
    I = [Int(f"i{i}_{j}") for j in range(n) for i in range(n)]

    s.add(
        [And(I[i * n + j] < 256, I[i * n + j] >= 0) for i in range(n) for j in range(n)]
    )
    Z = mul(lx, I, n)
    s.add([Z[i * n + j] == (1 if i == j else 0) for i in range(n) for j in range(n)])

    print(s.check())
    if s.check() == sat:
        m = s.model()
        inv = np.array([I[i * n + j].evaluate() for j in range(n) for i in range(n)])

        Image.fromarray(inv).save("invx.png")

    else:
        print("unsat")

    print("Time:")
    print(time.time() - t0)


from requests import *

r = get("https://brachiosaure.france-cybersecurity-challenge.fr/").content.decode()
x = r.find('<h4 class="text-warning">') + len('<h4 class="text-warning">')
r = r[x:]
x = r.find("</h4>")
r = r[:x]

main(r)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(
    executable_path=".\\selenium\\chromedriver.exe", options=chrome_options
)
driver.maximize_window()

driver.get("https://brachiosaure.france-cybersecurity-challenge.fr/")
# to identify element
username = driver.find_element("xpath", "//h4[@class='text-warning']")
s = driver.find_element("id", "upload1")
s.send_keys("C:\\Users\\Alexandre\\Desktop\\FCSC-2023\\rev-brachiosaure\\out\\fin.png")
s = driver.find_element("id", "upload2")
s.send_keys("C:\\Users\\Alexandre\\Desktop\\FCSC-2023\\rev-brachiosaure\\out\\finv.png")
# file path specified with send_keys

# LET THE USER CLICK :)
