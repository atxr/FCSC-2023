from fnvhash import fnv1_64
from uuid import uuid4

for i in range(0xffffffff): 
    #s = b"9be4a60f645f-" + str(uuid4()).encode()
    s = b"9be4a60f645f-e36d8fbc-9482-4f00-96c6-ae5370d04e08"
    h = hex(fnv1_64(s))[2:].rjust(16, "0")
    ok = True 
    ok &= h[:5] == "0000e"
       
    if ok:
        print(f"win {s=} {h=}")

        for j in range(0xffffff):
            n = len(s)
            p = (str(uuid4()) + str(uuid4()) + str(uuid4())).encode()[:n]
            assert(len(p) == n)
            hp = hex(fnv1_64(p))[2:].rjust(16, "0")
            ok = True 
            ok &= hp[:5] == "0000e"
            if ok:
                print(f"win2prek {p=} {hp=}")

