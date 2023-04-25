#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


def clean(l):
    l = l[19:].strip().replace("abs", "   ")
    return l


def split_instruction(i):
    idx = i.find(" ")
    comma = [op.replace(" ", "").strip() for op in i[idx:].split(",")]
    if i[:3] == "ret":
        return []
    return [i[:idx]] + comma


def join_instruction(i):
    if len(i) == 3:
        return '"{} {}, {}\\n"'.format(i[0], i[1], i[2])
    else:
        return '"{} {}\\n"'.format(i[0], i[1])


lines = open("/tmp/gdb.log").readlines()
lines = list(map(clean, lines))

instructions = []
for l in lines:
    ins = split_instruction(l)
    if ins == []:
        break

    instructions.append(ins)

rev = []
i = len(instructions) - 1

while i >= 0:
    if i > 0 and instructions[i - 1][0] in ["shr", "shl", "or", "and"]:
        rev.append(instructions[i - 2])
        rev.append(instructions[i - 1])
        if instructions[i][0] == "sub":
            rev.append(["add"] + instructions[i][1:])
        elif instructions[i][0] == "add":
            rev.append(["sub"] + instructions[i][1:])
        elif instructions[i][0] == "xor":
            rev.append(instructions[i])
        else:
            print("New shr/l instruction: {}".format(instructions[i][0]))
            exit(1)
        i -= 3
    elif instructions[i][0] == "add":
        rev.append(instructions[i - 1])
        rev.append(["sub"] + instructions[i][1:])
        i -= 2
    elif instructions[i][0] == "sub":
        rev.append(instructions[i - 1])
        rev.append(["add"] + instructions[i][1:])
        i -= 2
    elif instructions[i][0] == "rol":
        rev.append(["ror"] + instructions[i][1:])
        i -= 1
    elif instructions[i][0] == "ror":
        rev.append(["rol"] + instructions[i][1:])
        i -= 1
    elif instructions[i][0] == "xor":
        if (
            i == len(instructions) - 1
            and instructions[i][1] == "rax"
            and instructions[i][2] == "rdi"
        ):
            rev.append(["mov", "rdi", instructions[i - 1][2]])
        else:
            rev.append(instructions[i - 1])
            rev.append(instructions[i])
        i -= 2
    elif instructions[i][0] in ["neg", "xchg"]:
        rev.append(instructions[i])
        i -= 1
    elif instructions[i][0] == "inc":
        rev.append(["dec"] + instructions[i][1:])
        i -= 1
    elif instructions[i][0] == "dec":
        rev.append(["inc"] + instructions[i][1:])
        i -= 1
    elif instructions[i][0] == "mov":
        d = int(instructions[i - 3][2], 16) | 1
        inv = pow(d, -1, 2**64)
        rev.append(["mov", "rax", hex(inv)])
        rev.append(instructions[i - 1])
        rev.append(instructions[i])
        i -= 4
    elif instructions[i][0] == "or" and i == len(instructions) - 1:
        rev.append(["mov", "rdi", instructions[i - 4][2]])
        rev.append(["mov", "rsi", instructions[i - 2][2]])
        print("rsi involved")
        i -= 5
    else:
        print("Unknown instruction: {}".format(instructions[i][0]))
        for k in range(i - 10, i + 10):
            print(instructions[k])
        exit(1)

rev1 = rev[:]
rev2 = rev[:]
rev1.append(["mov", "rax", "rdi"])
rev2.append(["mov", "rax", "rsi"])
rev1 = "\n".join(list(map(join_instruction, rev1)))
rev2 = "\n".join(list(map(join_instruction, rev2)))
rev1 = '__asm(\n".intel_syntax noprefix\\n"\n' + rev1 + '\n".att_syntax\\n"\n);'
rev2 = '__asm(\n".intel_syntax noprefix\\n"\n' + rev2 + '\n".att_syntax\\n"\n);'

mysolve = """
#include <stdio.h>

unsigned long long rev1() {{
    {0}
}};

unsigned long long rev2() {{
    {1}
}};

int main() {{
    printf("rev input 1: %llu\\n", rev1());
    printf("rev input 2: %llu\\n", rev2());
    return 0;
}}
"""

open("mysolve.c", "w").write(mysolve.format(rev1, rev2))
os.system("gcc mysolve.c -o mysolve")
os.system("chmod +x mysolve")
os.system("./mysolve >> log")
os.system("./mysolve")
