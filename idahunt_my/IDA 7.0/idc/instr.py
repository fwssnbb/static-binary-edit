from idaapi import *
import idautils 
import idc
import idaapi
import pandas as pd
import struct
import lief
import pefile


ori_op = []
ori_address = []
ori_length = []
args0 = []
args1 = []
ins_index = 0
NEW_SECTION_ADDRESS = 0
INPUT_PE = 'test.py'
#idc.GetInputFilePath() #'test.exe'


POP_DIC = {'eax':'\x58','ecx':'\x59','ebx':'\x5b','edx':'\x5a','esp':'\x5c','ebp':'\x5d','esi':'\x5e','edi':'\x5f'}

#pop eax   58
#pop ebx   5b
#pop ecx   59
#pop edx   5a
#pop esp   5c
#pop ebp   5d
#pop esi   5e
#pop edi   5f

def insert_section(length,data):
    global NEW_SECTION_ADDRESS
    bin = lief.parse('test.exe')
    pe = pefile.PE('test.exe')
    section = lief.PE.Section('.test')
    section.virtual_address = (((pe.sections[-1].VirtualAddress + (pe.sections[-1].Misc_VirtualSize)-1)/0x1000+1)*0x1000)
    
    NEW_SECTION_ADDRESS = section.virtual_address

    section.virtual_size = section.size = length
    section.offset = (((pe.sections[-1].PointerToRawData + (pe.sections[-1].SizeOfRawData)-1)/0x200+1)*0x200)
    section.characteristics = 0x60000020
    insert_data = []
    for each in data:
        insert_data.append(ord(each))
    section.content = insert_data
    #set random address closed
    bin.optional_header.dll_characteristics =  bin.optional_header.dll_characteristics & 0xffbf

    bin.add_section(section)
    bin.write(INPUT_PE + ".crafted")

    
def build_section_data(args0,args1):
    push = '\x68' 
    #print args1
    
    tmp = struct.pack("I", args1)
    print args1,'pack:',tmp
    pop = POP_DIC[args0]
    print args0,pop
    retn = '\xc3'
    return push+tmp+pop+retn    

def instrument(origin_op, origin_address):
    if origin_op.startswith('mov'):
        if idc.GetOpType(origin_address, 0) == 1 and idc.GetOpType(origin_address, 1) == 5:

        	#print hex(origin_address)
            op_length=idaapi.decode_insn(origin_address)
            if op_length != 5: return
            ori_op.append(origin_op)
            ori_address.append(hex(origin_address))
            ori_length.append(op_length)
            args0.append(idc.GetOpnd(origin_address,0))
            args1.append(int(idc.Dword(origin_address+1)))
            #call address


def instrument_retrieve(origin_op, origin_address):
    global ins_index
    if origin_op.startswith('mov'):
        if idc.GetOpType(origin_address, 0) == 1 and idc.GetOpType(origin_address, 1) == 5:
            op_length=idaapi.decode_insn(origin_address)
            if op_length != 5: return
            #print hex(origin_address)
            #print index
            PatchByte(origin_address, 0xe8)
            PatchDword(origin_address + 1 ,NEW_SECTION_ADDRESS - origin_address - 5  + 7 * index)
            print NEW_SECTION_ADDRESS - origin_address - 5  + 7 * index
            ins_index += 1

            #print hex(origin_address)
            
            ori_op.append(origin_op)
            ori_address.append(hex(origin_address))
            ori_length.append(op_length)
            args0.append(idc.GetOpnd(origin_address,0))
            args1.append(int(idc.Dword(origin_address+1)))

def create_pe():
    for func in idautils.Functions():
        start_address = func
        end_address = idc.FindFuncEnd(func)
        #print hex(start_address)
        for each_step in idautils.Heads(start_address, end_address):
            #print hex(each_step)
            op = idc.GetDisasm(each_step)
            instrument(op,each_step)

    section_data = ''
    for index in range(len(ori_op)):
        section_data += build_section_data(args0[index],args1[index])

    section_file = open('newSectionData','wb')
    section_file.write(section_data)
    section_file.close()
    section_size = len(section_data)
    insert_section(len(section_data),section_data)

    ref = pd.DataFrame({'addr':ori_address,"ins":ori_op,'args0':args0,'args1':args1,'length':ori_length})
    ref.to_csv('ref.txt',index=0)

def scan_instrument():
    for func in idautils.Functions():
        start_address = func
        end_address = idc.FindFuncEnd(func)
        #print hex(start_address)
        for each_step in idautils.Heads(start_address, end_address):
            #print hex(each_step)
            op = idc.GetDisasm(each_step)
            #instrument(op,each_step)
            instrument_retrieve(op, each_step)
            #print op

if __name__ == '__main__':
    idc.Wait()
	#need IDA
    create_pe()
    #need IDA
    #object INPUT_PE + ".crafted"
    #scan_instrument()
    idc.Exit(0)