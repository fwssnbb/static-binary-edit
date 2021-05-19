# -*- coding = utf-8 -*-
from idaapi import *
import idautils
import pandas as pd
import struct
import lief
import pefile
import os
import idc

opcode_sequence = []
opcode_sequence_addr = []
opcode_sequence_length_each = []
def scan_pe():
    text_start = text_end = 0
    for seg in Segments():
        if idc.SegName(seg) == ".text":
            text_start = idc.SegStart(seg)
            text_end = idc.SegEnd(seg)

    for each_step in idautils.Heads(text_start, text_end):
        opcode = idc.GetMnem(each_step)
        op_length = idaapi.decode_insn(each_step)
        if opcode != '':
            opcode_sequence.append(opcode)
            opcode_sequence_addr.append(each_step)
            opcode_sequence_length_each.append(op_length)


    #print  type(opcode_sequence[100])
    #print 'ops:', len(opcode_sequence)
    #print 'addr:', len(opcode_sequence_addr)
    out = pd.DataFrame({'ops': opcode_sequence, 'addr': opcode_sequence_addr, 'op_length':opcode_sequence_length_each})
    out.to_csv(INPUT_PE + '.ops', index=0)
if __name__ == '__main__':
    idaapi.autoWait()
    INPUT_PATH, INPUT_PE = os.path.split(ida_nalt.get_input_file_path())
    scan_pe()
    if "DO_EXIT" in os.environ:
        idc.qexit(1)