from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from hashlib import sha512
import qrcode
from PIL import Image
from ctypes import *
import numpy as np


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


# Check if two matrices are equal
def mat_equ(a, b):
    if a.shape != b.shape:
        return False
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            if a[i, j] != b[i, j]:
                return False
    return True


# Get m^(k-1) for a nilpotent matrix m of order k
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

    if order == n - 1:
        print("not nilpotent")
        exit(1)

    return t


def generate_qrcodes(username):
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

    Image.fromarray(fin).save("out/fin.png")
    Image.fromarray(finv).save("out/finv.png")


def main():
    url = "https://brachiosaure.france-cybersecurity-challenge.fr/"
    path = "C:\\Users\\Alexandre\\Desktop\\FCSC-2023\\rev-brachiosaure"

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(
        executable_path=".\\selenium\\chromedriver.exe", options=chrome_options
    )
    driver.maximize_window()

    driver.get(url)
    username = driver.find_element("xpath", "//h4[@class='text-warning']").text
    generate_qrcodes(username)

    s = driver.find_element("id", "upload1")
    s.send_keys(path + "\\out\\fin.png")

    s = driver.find_element("id", "upload2")
    s.send_keys(path + "\\out\\finv.png")

    l = driver.find_element("xpath", "//button[@class='btn btn-primary']")
    driver.execute_script("arguments[0].click();", l)


if __name__ == "__main__":
    main()
