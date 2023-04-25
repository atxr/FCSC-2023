def ror(n, rot=1, width=64):
    n = tobin(n)[2:]
    n = n.rjust(width, "0")
    n = n[-rot:] + n[:-rot]
    return int(n, 2)


def rol(n, rot=1, width=64):
    return ror(n, -rot, width)


def tohex(a, nbits=64):
    return hex((a + (1 << nbits)) % (1 << nbits))


def tobin(a, nbits=64):
    return bin((a + (1 << nbits)) % (1 << nbits))


def mul(a, b, nbits=128):
    return ((a * b + (1 << nbits)) % (1 << nbits)) & (2**64 - 1)


def test(inp1):
    r = mul(-0x7E1A385F7AC6B561, (inp1 ^ 0xE32ABD8EE510E5B0) + 0x208D4BFC30FA998B)

    a = ror(-r + 0xC28F3F183BA05D, 0x34)
    r = mul(0x70717B53945B0533, a - -0x301D4459AB90D946)

    a = ror((r + 2) ^ -0x7C89CAFD210BEEF2, 0x22)
    r = mul(-0xE76D6D13715FBB9, rol(a - 0x28EEAAF50204F377, 0x15))
    r = mul(-0x4210C4BCC7A81D17, r - -0x748706FB000D9C62)
    r = mul(
        -0x6844F790DD0D434F,
        -(
            rol(
                ror(
                    -(
                        (ror(-(-(r) + 1), 2) ^ 0x201826A9A4E513F3 ^ 0x60CD0371AEBC755C)
                        - -0x6CA56CC652FD38B2
                    ),
                    0x2A,
                )
                + 0x530CE73BA46DCC81,
                1,
            )
        ),
    )

    r = mul(
        0x112E7FE34821799D,
        -(
            -(
                -(
                    ror(
                        ((r ^ 0x83A79DA815BEE394) + 0xF749D32CF04694D)
                        ^ 0x7E9F6916BF02E6D3,
                        7,
                    )
                    + 1
                )
                + 1
            )
        )
        - 0x1FD1BC12B7E6DD8C,
    )

    r = mul(0x43ED814A5E004AA9, r + 0x2A15AED18FE41ED7)
    r = mul(-0x72E0FC0A3F6E39F5, r - 1)
    r = mul(
        -0x753136FAA69CB887,
        ror((r - -0x635F86A96045C266) ^ 0xA91EE3D67D08DF61, 0x13) - 1,
    )

    r = (
        -0x23E7ABA53669BB76
        ^ ror(
            -(
                ror(
                    (
                        (
                            -(
                                (
                                    (
                                        -(
                                            rol(
                                                ror(
                                                    -(ror(r, 0x11) - 1)
                                                    - 0x2EA56B0EBE823585,
                                                    5,
                                                )
                                                + 0x7FCC3EACE4EBA8D1,
                                                0x3E,
                                            )
                                        )
                                        - -0x4C5698B156858997
                                    )
                                    ^ 0x972878F59896CB1C
                                )
                                - 0x44684873B593128A
                            )
                            + 0x3896EB4AA778987A
                        )
                        ^ 0x483429977C450318
                    )
                    + 2,
                    0x1B,
                )
                + 1
            )
            - 0x6DAD8FCF4FA51900,
            5,
        )
        ^ 0xA860153B86C8CAE2
    )
    return r


def rev():
    r = 0
    r += 0x23E7ABA53669BB76
    r ^= 0xA860153B86C8CAE2
    r = rol(r, 5)
    r += 0x6DAD8FCF4FA51900
    r = -r
    r -= 1
    r = rol(r, 0x1B)
    r -= 2
    r ^= 0x483429977C450318
    r += 0x3896EB4AA778987A
    r = -r
    r += 0x44684873B593128A
    r ^= 0x972878F59896CB1C
    r -= 0x4C5698B156858997
    r = -r
    r = ror(r, 0x3E)
    r -= 0x7FCC3EACE4EBA8D1
    r = rol(r, 5)
    r += 0x2EA56B0EBE823585
    r = -r
    r += 1
    r = rol(r, 0x11)


for i in range(2**64):
    if i % 0x10000 == 0:
        print(hex(i))
    if test(i) == 0:
        print(hex(i))
        break
