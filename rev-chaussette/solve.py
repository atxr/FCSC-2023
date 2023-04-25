from pwn import *

p = process("./chaussette")
gdb.attach(
    p,
    gdbscript="""
b socket
detach
quit
""",
)
# set logging file /tmp/func.asm

p.sendline(b"9243637858070793867")
p.sendline(b"9243637858070793867")

gdb.attach(
    p,
    gdbscript="""
c
finish
x/2000i $rbx
""",
    # b *0x555555557195
    # c
    # set logging on
    # x/2000i $rbx
    # set logging off
    # detach
    # quit
)

p.interactive()
