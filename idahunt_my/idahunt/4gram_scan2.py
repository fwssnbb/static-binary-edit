#-*- coding = utf-8 -*-
import os
import os
import pandas as pd
import time
import argparse
from random import Random
import random
from multiprocessing import Pool
import multiprocessing

ngram = []
count_ngram = []
index_change = []
feature_dimen = 0

def random_str():
	randomlength = 10
	str=''
	chars  = 'abcdefghijklmnopqrstuvwxyz0123456'
	length = len(chars) - 1
	random = Random()
	for i in range(randomlength):
		str+=chars[random.randint(0, length)]
	return str

def int2bin(n, count):
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])

def scan_pe(file_opcode, file_opcode_addr, ngram_feature, subcode, list_change_location):
    #print("0000")
    ngram_feature_list = ngram_feature.split()
    #print(ngram_feature_list)
    fourG = ['', '', '', '']
    fourG_addr = [0, 0, 0, 0]
    weizhi = []

    print_count = 0
    for x, each_step_opcode in enumerate(file_opcode):
        fourG[0] = fourG[1]
        fourG_addr[0] = fourG_addr[1]
        fourG[1] = fourG[2]
        fourG_addr[1] = fourG_addr[2]
        fourG[2] = fourG[3]
        fourG_addr[2] = fourG_addr[3]
        fourG[3] = each_step_opcode
        fourG_addr[3] = file_opcode_addr[x]

        if len(ngram_feature_list) == 2 and fourG[0] == ngram_feature_list[0] and fourG[1] == ngram_feature_list[1]:
            if print_count <= 1:
                print(ngram_feature, "0x%x" % fourG_addr[0], fourG[0], fourG[1])
                print(list_change_location)
                print_count += 1
                print(subcode)
            for j, c in enumerate(subcode):
                if c == '1':
                    if print_count < 2:
                        print(fourG[list_change_location[j]], "0x%x" % fourG_addr[list_change_location[j]])
                        print('666')
                    weizhi.append(fourG_addr[list_change_location[j]])
        if len(ngram_feature_list) == 3 and \
                fourG[0] == ngram_feature_list[0] and \
                fourG[1] == ngram_feature_list[1] and \
                fourG[2] == ngram_feature_list[2]:
            if print_count <= 1:
                print(ngram_feature, "0x%x" % fourG_addr[0], fourG[0], fourG[1], fourG[2])
                print(list_change_location)
                print_count += 1
                print(subcode)
            for j, c in enumerate(subcode):
                if c == '1':
                    if print_count < 2:
                        print(fourG[list_change_location[j]], "0x%x" % fourG_addr[list_change_location[j]])
                        print('777')
                    weizhi.append(fourG_addr[list_change_location[j]])
        if len(ngram_feature_list) == 4 and \
                fourG[0] == ngram_feature_list[0] and \
                fourG[1] == ngram_feature_list[1] and \
                fourG[2] == ngram_feature_list[2] and \
                fourG[3] == ngram_feature_list[3]:
            if print_count <= 1:
                print(ngram_feature, "0x%x" % fourG_addr[0], fourG[0], fourG[1], fourG[2], fourG[3])
                print(list_change_location)
                print_count += 1
                print(subcode)
            for j, c in enumerate(subcode):
                if c == '1':
                    if print_count < 2:
                        print(fourG[list_change_location[j]], "0x%x" % fourG_addr[list_change_location[j]])
                        print('888')
                    weizhi.append(fourG_addr[list_change_location[j]])

    return weizhi

def decode(file_opcode, file_opcode_addr, sample_code, feature_dimen, ngram, count_ngram, index_change):
    #print(file_opcode_addr)
    #print(type(sample_code))
    addr_to_fix = []
    #print(feature_dimen)
    bin_code = int2bin(int(sample_code), feature_dimen)
    #print(ngram)
    print(bin_code)
    m = 0
    n = 0
    for i, cnt in enumerate(count_ngram):
        n += cnt
        sub_code = bin_code[m:n]
        if sub_code.find('1') != -1:
            print(sub_code)
            addr_to_fix = addr_to_fix + scan_pe(file_opcode, file_opcode_addr, ngram[i], sub_code, index_change[i])
        m = n
    return addr_to_fix

def do_multiprocess(file_name, file_opcode, file_opcode_addr, sample_code, feature_dimen, ngram,count_ngram, index_change):

    tmp_addr_to_fix = decode(file_opcode, file_opcode_addr, int(sample_code), feature_dimen, ngram,count_ngram, index_change)
    print(tmp_addr_to_fix)
    with open("..\\..\\sample\\crafted\\"+file_name[:-4]+"\\ADDR\\"+file_name[:-4]+"_"+random_str(), 'w') as f:
        for each in tmp_addr_to_fix:
            f.write(str(each))
            f.write('\n')

def get_file_opcode(work_dir,file1):
    df_tmp_each_ops = pd.read_csv(os.path.join(work_dir, file1))
    opcode_sequence = df_tmp_each_ops['ops'].tolist()
    return opcode_sequence

def get_file_opaddr(work_dir,file1):
    df_tmp_each_ops = pd.read_csv(os.path.join(work_dir, file1))
    opcode_sequence_addr = df_tmp_each_ops['addr'].tolist()
    return opcode_sequence_addr


if __name__ == '__main__':
    #input parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--numberOut', dest='numberOut', default=5,
                        help='number of virus times of what you want generate')
    args = parser.parse_args()
    numberOut = int(args.numberOut)

    #for multiprocess
    N_cpu = multiprocessing.cpu_count()
    print(N_cpu)
    pool = Pool()

    work_dir = "..\\..\\sample"

    start_time = time.time()
    #get the feaeture vector
    with open(r'something\feature_my.txt', 'r') as f:
        for line in f.readlines():
            tmp_ngram = line.strip()
            tmp_ngram_list = tmp_ngram.split()
            ngram.append(line.strip())
            count = 0
            tmp_index_list = []
            for i in range(len(tmp_ngram_list)):
                if tmp_ngram_list[i] == 'mov' or tmp_ngram_list[i] == 'call' or tmp_ngram_list[i] == 'jz':
                    count += 1
                    tmp_index_list.append(i)
            count_ngram.append(count)
            index_change.append(tmp_index_list)


    for each in count_ngram:
        feature_dimen += each
    print(feature_dimen)

    df_addr_to_fix = pd.read_csv('something\\150.csv')
    # print df_addr_to_fix.head()
    l_code = df_addr_to_fix['code'].tolist()


    #do_dir
    input_file_list = []
    for file1 in os.listdir(work_dir):
        if file1.endswith(".ops"):
            input_file_list.append(file1)
    #file1 = "1351a37a500251438fb253baa24c7c8d3acab88724f7179ee8b6b0dbf9d1ec3f.exe.ops"



    work_list = [] #[[filename1,code1],[filename2,code2],....]
    for file1 in input_file_list:
        l_code_tmp = []
        l_code_tmp = random.sample(l_code, numberOut)
        for tmp_code in l_code_tmp:
            tmp_list = [file1, tmp_code]
            work_list.append(tmp_list)


    #print(opcode_sequence)
    #print(hex(opcode_sequence_addr[0]))

    #print(l_code_tmp)
    for i, each_item in enumerate(work_list):
        df_tmp_each_ops = pd.read_csv(os.path.join(work_dir, work_list[i][0]))
        opcode_sequence = df_tmp_each_ops['ops'].tolist()
        opcode_sequence_addr = df_tmp_each_ops['addr'].tolist()
        pool.apply_async(do_multiprocess, (work_list[i][0], opcode_sequence, opcode_sequence_addr, work_list[i][1], feature_dimen, ngram, count_ngram, index_change))

    pool.close()
    pool.join()
    print("exe %s one time multiprocess" % file1)


    #df_ops = pd.read_csv("..\\..\\sample\\")