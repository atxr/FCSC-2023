from bitstring import *

key = [-31, 78, 87, -98, -81, -100, 28, 61, -62, 68, -2, 69, 41, -2, -14, 17, 43, -120, 33, 112, 57, -107, -87, 57, -79, 72, -43, -53, -109, -43, -20, -71, -100, -33, -84, -105, 58, 26, -125, -29, 52, -19, -25, 52, -94, -69, -118, -115, -38, 26, -65, -47, 99, 34, 37, 104, -91, 23, 64, 62, -34, -75, -104, -103]

def to_int64(k):
    t = [[Bits(int=x, length=8).bytes for x in k[i*8:(i+1)*8]] for i in range(8)]
    return [int.from_bytes(b''.join(sub), 'little') for sub in t]

res = []
res_int = []
k64 = to_int64(key)
for i in range(len(k64)):
    for j in range(56, -1, -8):
        res.append((k64[i] >> j) & 0xff)
        res_int.append(Bits(uint=(k64[i] >> j) & 0xff, length=8).int)

print(res)
print(res_int)
