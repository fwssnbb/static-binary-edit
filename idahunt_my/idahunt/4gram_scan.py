# -*- coding = utf-8 -*-
from idaapi import *
import idautils
import struct
import lief
import pefile
import os
import idc
import random
#import pandas as pd


(INPUT_PATH,INPUT_PE) = os.path.split(ida_nalt.get_input_file_path())#
addr_to_fix = []
list_feature_my = ['mov xor mov call','mov test','call mov call']
#list_feature_my = []
list_dict = [{} for i in range(len(list_feature_my))]

def generate_dictlist():
    for each in list_dict:
        key_num = len(list(each.keys()))
        if key_num == 1:
            each[0] = []
        if key_num == 2:
            each[0] = []
            each[3] = list(set(each[2]+each[1]))
        if key_num == 3:
            each[0] = []
            each[3] = list(set(each[2]+each[1]))
            each[5] = list(set(each[4]+each[1]))
            each[6] = list(set(each[4]+each[2]))
            each[7] = list(set(each[4]+each[2]+each[1]))
        if key_num == 4:
            each[0] = []
            each[3] = list(set(each[2]+each[1]))
            each[5] = list(set(each[4]+each[1]))
            each[6] = list(set(each[4]+each[2]))
            each[7] = list(set(each[4]+each[2]+each[1]))
            each[9] = list(set(each[8]+each[1]))
            each[10] = list(set(each[8]+each[2]))
            each[11] = list(set(each[8]+each[2]+each[1]))
            each[12] = list(set(each[8]+each[4]))
            each[13] = list(set(each[8]+each[4]+each[1]))
            each[14] = list(set(each[8]+each[4]+each[2]))
            each[15] = list(set(each[8]+each[4]+each[2]+each[1]))

def scan_pe():
    text_start = text_end = 0
    for seg in Segments():
        if idc.SegName(seg) == ".text":
            text_start = idc.SegStart(seg)
            text_end = idc.SegEnd(seg)

    fourG = ['','','','']
    fourG_addr = [0,0,0,0]
    
    for each_step in idautils.Heads(text_start,text_end):
        opcode = idc.GetMnem(each_step)
        #print type(each_step)
        #traverse 4 Gram
        fourG[0] = fourG[1]
        fourG_addr[0] = fourG_addr[1]
        fourG[1] = fourG[2]
        fourG_addr[1] = fourG_addr[2]
        fourG[2] = fourG[3]
        fourG_addr[2] = fourG_addr[3]
        fourG[3] = opcode
        fourG_addr[3] = each_step

        #scan every feature and append it in list of dict
        for each_feature in list_feature_my:
            each_feature_index = list_feature_my.index(each_feature)
            tmp_feature_list = each_feature.split()
            if len(tmp_feature_list) == 2:
                if fourG[0] == tmp_feature_list[0] and fourG[1] == tmp_feature_list[1]:
                    print each_feature,"0x%x" % fourG_addr[0],idc.GetDisasm(fourG_addr[0])
                    count_all_dimension = 0
                    for x in tmp_feature_list:
                        if x == 'mov' or x == 'call' or x == 'jz':
                            count_all_dimension += 1
                    if count_all_dimension == 1:
                        index_list_each_feature = []
                        for i in range(len(tmp_feature_list)):
                            if tmp_feature_list[i] == 'mov' or tmp_feature_list[i] == 'call' or tmp_feature_list[i] == 'jz':
                                index_list_each_feature.append(i)
                        
                        list_dict[each_feature_index].setdefault(1,[])
                        list_dict[each_feature_index][1].append(fourG_addr[index_list_each_feature[0]])
                    if count_all_dimension == 2:
                        index_list_each_feature = []
                        for i in range(len(tmp_feature_list)):
                            if tmp_feature_list[i] == 'mov' or tmp_feature_list[i] == 'call' or tmp_feature_list[i] == 'jz':
                                index_list_each_feature.append(i)
                        
                        list_dict[each_feature_index].setdefault(2,[])
                        list_dict[each_feature_index][2].append(fourG_addr[index_list_each_feature[0]])
                        list_dict[each_feature_index].setdefault(1,[])
                        list_dict[each_feature_index][1].append(fourG_addr[index_list_each_feature[1]])
            
            if len(tmp_feature_list) == 3:
                if fourG[0] == tmp_feature_list[0] and fourG[1] == tmp_feature_list[1] and fourG[2] == tmp_feature_list[2]:
                    print each_feature,"0x%x" % fourG_addr[0],idc.GetDisasm(fourG_addr[0])
                    count_all_dimension = 0
                    for x in tmp_feature_list:
                        if x == 'mov' or x == 'call' or x == 'jz':
                            count_all_dimension += 1
                    if count_all_dimension == 1:
                        index_list_each_feature = []
                        for i in range(len(tmp_feature_list)):
                            if tmp_feature_list[i] == 'mov' or tmp_feature_list[i] == 'call' or tmp_feature_list[i] == 'jz':
                                index_list_each_feature.append(i) 

                        list_dict[each_feature_index].setdefault(1,[])
                        list_dict[each_feature_index][1].append(fourG_addr[index_list_each_feature[0]])
                    if count_all_dimension == 2:
                        index_list_each_feature = []
                        for i in range(len(tmp_feature_list)):
                            if tmp_feature_list[i] == 'mov' or tmp_feature_list[i] == 'call' or tmp_feature_list[i] == 'jz':
                                index_list_each_feature.append(i)

                        list_dict[each_feature_index].setdefault(2,[])
                        list_dict[each_feature_index][2].append(fourG_addr[index_list_each_feature[0]])
                        list_dict[each_feature_index].setdefault(1,[])
                        list_dict[each_feature_index][1].append(fourG_addr[index_list_each_feature[1]])
                    if count_all_dimension == 3:
                        index_list_each_feature = []
                        for i in range(len(tmp_feature_list)):
                            if tmp_feature_list[i] == 'mov' or tmp_feature_list[i] == 'call' or tmp_feature_list[i] == 'jz':
                                index_list_each_feature.append(i) 
                        list_dict[each_feature_index].setdefault(4,[])
                        list_dict[each_feature_index][4].append(fourG_addr[index_list_each_feature[0]])
                        list_dict[each_feature_index].setdefault(2,[])
                        list_dict[each_feature_index][2].append(fourG_addr[index_list_each_feature[1]])
                        list_dict[each_feature_index].setdefault(1,[])
                        list_dict[each_feature_index][1].append(fourG_addr[index_list_each_feature[2]])

            if len(tmp_feature_list) == 4:
                if fourG[0] == tmp_feature_list[0] and fourG[1] == tmp_feature_list[1] and fourG[2] == tmp_feature_list[2] and fourG[3] == tmp_feature_list[3]:
                    print each_feature,"0x%x" % fourG_addr[0],idc.GetDisasm(fourG_addr[0])
                    count_all_dimension = 0
                    for x in tmp_feature_list:
                        if x == 'mov' or x == 'call' or x == 'jz':
                            count_all_dimension += 1
                    if count_all_dimension == 1:
                        index_list_each_feature = []
                        for i in range(len(tmp_feature_list)):
                            if tmp_feature_list[i] == 'mov' or tmp_feature_list[i] == 'call' or tmp_feature_list[i] == 'jz':
                                index_list_each_feature.append(i)

                        list_dict[each_feature_index].setdefault(1,[])
                        list_dict[each_feature_index][1].append(fourG_addr[index_list_each_feature[0]])
                    if count_all_dimension == 2:
                        index_list_each_feature = []
                        for i in range(len(tmp_feature_list)):
                            if tmp_feature_list[i] == 'mov' or tmp_feature_list[i] == 'call' or tmp_feature_list[i] == 'jz':
                                index_list_each_feature.append(i)

                        list_dict[each_feature_index].setdefault(2,[])
                        list_dict[each_feature_index][2].append(fourG_addr[index_list_each_feature[0]])
                        list_dict[each_feature_index].setdefault(1,[])
                        list_dict[each_feature_index][1].append(fourG_addr[index_list_each_feature[1]])
                    if count_all_dimension == 3:
                        index_list_each_feature = []
                        for i in range(len(tmp_feature_list)):
                            if tmp_feature_list[i] == 'mov' or tmp_feature_list[i] == 'call' or tmp_feature_list[i] == 'jz':
                                index_list_each_feature.append(i) 
                        
                        list_dict[each_feature_index].setdefault(4,[])
                        list_dict[each_feature_index][4].append(fourG_addr[index_list_each_feature[0]])
                        list_dict[each_feature_index].setdefault(2,[])
                        list_dict[each_feature_index][2].append(fourG_addr[index_list_each_feature[1]])
                        list_dict[each_feature_index].setdefault(1,[])
                        list_dict[each_feature_index][1].append(fourG_addr[index_list_each_feature[2]])
                    if count_all_dimension == 4:
                        index_list_each_feature = []
                        for i in range(len(tmp_feature_list)):
                            if tmp_feature_list[i] == 'mov' or tmp_feature_list[i] == 'call' or tmp_feature_list[i] == 'jz':
                                index_list_each_feature.append(i)  

                        list_dict[each_feature_index].setdefault(8,[])
                        list_dict[each_feature_index][8].append(fourG_addr[index_list_each_feature[0]])
                        list_dict[each_feature_index].setdefault(4,[])
                        list_dict[each_feature_index][4].append(fourG_addr[index_list_each_feature[1]])
                        list_dict[each_feature_index].setdefault(2,[])
                        list_dict[each_feature_index][2].append(fourG_addr[index_list_each_feature[2]])
                        list_dict[each_feature_index].setdefault(1,[])
                        list_dict[each_feature_index][1].append(fourG_addr[index_list_each_feature[3]])

    generate_dictlist()             
    #print "3 of 4",3*len(addr_to_fix)/4
    """
    name = ['operation','address']
    os.system("mkdir "+"crafted\\"+INPUT_PE)
    for i in range(0,1024):
        tmp_list = []
        tmp_list = random.sample(addr_to_fix,3*len(addr_to_fix)/4)

        df_tmp = pd.DataFrame(columns = name,data = tmp_list)
        df_tmp.to_csv("crafted\\"+INPUT_PE+"\\"+str(i),encoding = 'gbk')
    """
    '''
        tmp2 = open("crafted\\"+INPUT_PE+"\\"+str(i),'w')
        for each in tmp_list:
            tmp2.write(str(each[0])+','+str(each[1]))
            tmp2.write('\n')
        tmp2.close()
    '''
    #df_tmp1 = pd.DataFrame(columns = name,data = addr_to_fix)
    #df_tmp1.to_csv("crafted\\" + INPUT_PE+"\\" + INPUT_PE +"_addr_to_fix",encoding = 'gbk')
    '''
    tmp1 = open("crafted\\" + INPUT_PE + "_addr_to_fix",'w')
    for each in addr_to_fix:
        tmp1.write(str(each[0])+','+str(each[1]))
        tmp1.write('\n')
    tmp1.close()
    '''


if __name__ == "__main__":
    idaapi.autoWait()

    #with open(r'..\idahunt_my\idahunt\something\feature_my.txt','r') as f:
    #    for line in f.readlines():
    #        list_feature_my.append(line.strip())
    #print list_feature_my
    scan_pe()
    #print list_dict

    if "DO_EXIT" in os.environ:
        idc.qexit(1)