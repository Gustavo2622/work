import re

ops = {
"000000": "Rfmt",
"001000": "addi",
"010000": "TLB",
"100000": "lb",
"101000": "sb",
"110000": "lwc0",
"111000": "swc0",

"000001": "Bltz/gez",
"001001": "addiu",
"010001": "FLPt",
"100001": "lh",
"101001": "sh",
"110001": "lwcl",
"111001": "swcl",

"000010": "j",
"001010": "slti",
"100010": "lwl",
"101010": "swl",

"000011": "jal",
"001011": "sltiu",
"100011": "lw",
"101011": "sw",

"000100": "beq",
"001100": "ANDi",
"100100": "lbu",

"000101": "bne",
"001101": "ORi",
"100101": "lhu",

"000110": "blez",
"001110": "xORi",
"100110": "lwr",
"101110": "swr",

"000111": "bgtz",
"001111": "lui"
}

funct = {
"000000": "shll",
"001000": "jr",
"010000": "mfhi",
"011000": "mult",
"100000": "add",

"001001": "jalr",
"010001": "mthi",
"011001": "multu",
"100001": "addu",

"000010": "shrl",
"010010": "mflo",
"011010": "div",
"100010": "sub",
"101010": "slt",

"000011": "sra",
"010011": "mtlo",
"011011": "divu",
"100011": "subu",
"101011": "sltu",

"000100": "sllv",
"001100": "syscall",
"100100": "and",

"001101": "break",
"100101": "or",

"000110": "srlv",
"100110": "xor",

"000111": "srav",
"100111": "nor"
}

regs = {
0: "$zero",
2: "$v0",
3: "$v1",
24: "$t8",
25: "$t9",
28: "$gp",
29: "$sp",
30: "$fp",
31: "$ra"
}

for i in range(4, 8):
  regs[i] = "$a{}".format(i-4)

for i in range(8, 16):
  regs[i] = "$t{}".format(i-8)

for i in range(16, 23):
  regs[i] = "$s{}".format(i-16)

ops2 = {v: k for k, v in ops.items()}
funct2 = {v: k for k, v in funct.items()}
regs2 = {v:k for k, v in regs.items()}

def process(instr):
  # If its in Rfmt
  if instr[:6] == "0"*6:
    op, rs, rt, rd, shamt, func = r_split(instr)
    if funct[func] == "jalr":
      print("{} {}, {}".format(funct[func], regs[int(rs, 2)], regs[int(rd, 2)]))
    elif funct[func][0] == 'j':
      print("{} {}".format(funct[func], regs[int(rs, 2)]))
    else:
      print("{}  {}, {}, {}".format(funct[func], regs[int(rd, 2)], regs[int(rs, 2)], regs[int(rt, 2)]))
  # If instruction is a jump
  elif ops[instr[:6]][0] == "j":
    op, tgt = j_split(instr)
    print("{} {}".format(ops[op], hex(int(tgt, 2))))
  elif ops[instr[:6]][0] == "l" or "sw" in ops[instr[:6]]:
    op, rs, rt, off = i_split(instr)
    print ("{} {}, {}({})".format(ops[op], regs[int(rt,2)], hex(int(off, 2)), regs[int(rs,2)]))
  else:
    op, rs, rt, imm = i_split(instr)
    print("{} {}, {}, {}".format(ops[op], regs[int(rs,2)], regs[int(rt,2)], hex(int(imm,2))))

def r_split(instr):
  return instr[:6], instr[6:11], instr[11:16], instr[16:21], instr[21:26], instr[26:32]

def i_split(instr):
  return instr[:6], instr[6:11], instr[11:16], instr[16:32]

def j_split(instr):
  return instr[:6], instr[6:]

def get_reg_bin(reg):
  return bin(regs2[reg]).lstrip('0b').rjust(5,"0")

def inv_process(instr):
  instr = re.sub(r'  *', ' ', instr)
  if '(' in instr:
    instr, rt, last = [a.strip(' ').strip(',') for a in instr.strip().split(' ')]
    off, rs = last.split('(')
    rs = rs.split(')')[0]
    ret = ops2[instr] + "|" + bin(regs2[rs]).lstrip('0b').rjust(5,"0") + "|" + bin(regs2[rt]).lstrip('0b').rjust(5,"0") + "|" + bin(int(off)).lstrip('0b').rjust(16, "0")
    print(ret)
  elif re.match('j[a-zA-Z]* ', instr) != None:
    if "j " in instr:
      ret = ops2["j"] + bin(int((instr.strip().split(' '))[-1].strip().strip(','))).lstrip('0b').rjust(26, "0")
      print(ret)
  else:
    parts = [a.strip(' ').strip(',') for a in instr.split(' ')]
    for part in parts:
      print("|", part)
    if len(parts) == 4:
      opr, rs, rt, rd = parts
      if opr in funct2.keys():
        ret = "000000" + "|" + get_reg_bin(rs) + "|" + get_reg_bin(rt) + "|" + get_reg_bin(rd) + "|" + "00000" + "|" + funct2[opr]
        print(ret)
      else:
        imm = rd.strip()
        ret = ops2[opr] + "|" + get_reg_bin(rs) + "|" + get_reg_bin(rt) + "|"
        ret += bin(int(imm)).lstrip('0b').rjust(16, "0")
        print(ret)
