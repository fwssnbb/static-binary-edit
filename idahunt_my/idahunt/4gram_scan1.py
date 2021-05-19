# -*- coding = utf-8 -*-
from idaapi import * 
import idautils
import idc
import os
import pandas as pd
from random import Random
from multiprocessing import Pool
import multiprocessing
import pickle
ngram = []
count_ngram = []
index_change = []
feature_dimen = 0



#code = 86324984056451907503742825152019487712381337587467513401756785949515946741922972271839800182373589831717401902131077688311497772841081312893334326519207894349456516448439709750270701008648882193832966524778914932475372156496983971622409819163641542921762315963808514710683708734091160007922815994031449816857936737670319725138335139337886539408353491204872423276293175072434269169609171695539126705643040068476060264944409052728875352567900294130938322668346799751185390537480990071543516628709809246512219885637075743319598251752512955209649577287606976322295053847306605894157404100199069236563163722849148175635404348528089121251845523451946047610337007878575539075185374058582819746493412453944936938671727279704267656368513524886337462964895366586206677304733494726230694412889549240544029777380410099574644467829024044427439357042467281550827296860444073583598506885611932035308455913232335734182416286641072164146932764686981683669133649218725744088930024040139250430579119720822750481547458444174436639019487396204952794729345952899383644313403731124485960426399602752948081668435417602658263623992173132575488438141428844221353921588482627329102528430428858035730002375750367318075371988229471844700532470367996191528320891979348525507065617119929406906229314506990006394944264577673092617924648776079606129684571274612104527674389794831243455312125165918213993575548946101908806084580351560720947695274422434330537813785066156209729180749841034724876669915202858669172962773823120069528270574446275076384276299685682517722118101111073832181246476684170588994779101534057397827532873706445835925940526447350910064676891113780840385073484412324690512098761420194

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
    """returns the binary of integer n, using count number of digits"""
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])

def scan_pe(ngram_feature,subcode,list_change_location):
    for seg in Segments():
        if idc.SegName(seg) == ".text":
            text_start = idc.SegStart(seg)
            text_end = idc.SegEnd(seg)

    ngram_feature_list = ngram_feature.split()

    fourG = ['', '', '', '']
    fourG_addr = [0, 0, 0, 0]
    weizhi = []

    print_count = 0

    for each_step in idautils.Heads(text_start, text_end):
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

        if len(ngram_feature_list) == 2 and fourG[0] == ngram_feature_list[0] and fourG[1] == ngram_feature_list[1]:
            if print_count <= 1:
                print ngram_feature, "0x%x" % fourG_addr[0], idc.GetDisasm(fourG_addr[0]), idc.GetMnem(fourG_addr[1]), idc.GetMnem(fourG_addr[2]), idc.GetMnem(fourG_addr[3])
                print list_change_location
                print_count += 1
                print subcode
            for i,c in enumerate(subcode):
                if c == '1':
                    if print_count < 2:
                        print fourG[list_change_location[i]],"0x%x"%fourG_addr[list_change_location[i]]
                        print '666'
                    weizhi.append(fourG_addr[list_change_location[i]])
        if len(ngram_feature_list) == 3 and fourG[0] == ngram_feature_list[0] and fourG[1] == ngram_feature_list[1] and fourG[2] == ngram_feature_list[2]:
            if print_count <= 1:
                print ngram_feature,"0x%x" % fourG_addr[0],idc.GetDisasm(fourG_addr[0]),idc.GetMnem(fourG_addr[1]),idc.GetMnem(fourG_addr[2]),idc.GetMnem(fourG_addr[3])
                print list_change_location
                print_count += 1
                print subcode
            for i,c in enumerate(subcode):
                if c == '1':
                    if print_count < 2:
                        print fourG[list_change_location[i]],"0x%x"%fourG_addr[list_change_location[i]]
                        print '777'
                    weizhi.append(fourG_addr[list_change_location[i]])
        if len(ngram_feature_list) == 4 and fourG[0] == ngram_feature_list[0] and fourG[1] == ngram_feature_list[1] and fourG[2] == ngram_feature_list[2] and fourG[3] == ngram_feature_list[3]:
            if print_count <= 1:
                print ngram_feature, "0x%x" % fourG_addr[0], idc.GetDisasm(fourG_addr[0]), idc.GetMnem(fourG_addr[1]), idc.GetMnem(fourG_addr[2]),idc.GetMnem(fourG_addr[3])
                print list_change_location
                print_count += 1
                print subcode
            for i,c in enumerate(subcode):
                if c == '1':
                    if print_count < 2:
                        print fourG[list_change_location[i]], "0x%x" % fourG_addr[list_change_location[i]]
                        print '888'
                    weizhi.append(fourG_addr[list_change_location[i]])

    return weizhi
def decode(sample_code):
    addr_to_fix = []
    #bincode = sample_code
    bin_code = int2bin(sample_code,feature_dimen)
    print bin_code
    #print len(bin_code)
    m = 0
    n = 0
    for i,cnt in enumerate(count_ngram):
        n += cnt
        sub_code = bin_code[m:n]
        if sub_code.find('1') != -1:
            addr_to_fix = addr_to_fix + scan_pe(ngram[i],sub_code,index_change[i])
        m = n    
    return addr_to_fix

def do_multiprocess(each_code):
    tmp_addr_to_fix = decode(int(each_code))
    with open(origin_INPUT_PE + "\\ADDR\\" + origin_INPUT_PE + '_' + random_str(), 'w') as f:
        for each in tmp_addr_to_fix:
            f.write(str(each))
            f.write('\n')

if __name__ == '__main__':
    idaapi.autoWait()

    N_cpu = multiprocessing.cpu_count()
    print N_cpu
    pool = Pool(1)

    (INPUT_PATH, INPUT_FILE) = os.path.split(ida_nalt.get_input_file_path())
    origin_INPUT_PE = INPUT_FILE.split('.')[0]+'.'+INPUT_FILE.split('.')[1]
    print INPUT_FILE
    #initial ngram count_ngram index_change
    with open(r'..\..\idahunt_my\idahunt\something\feature_my.txt','r') as f:
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
    #print ngram
    #print count_ngram
    for each in count_ngram:
        feature_dimen += each
    
    print feature_dimen
    #decode the genetic code
    df_addr_to_fix = pd.read_csv('..\\..\\idahunt_my\\idahunt\\something\\initial.csv')
    #print df_addr_to_fix.head()
    l_ori_file = df_addr_to_fix['ori_file'].tolist()
    l_code = df_addr_to_fix['code'].tolist()
    #print type(l_code[0])
    for i, each_code in enumerate(l_code):
        if origin_INPUT_PE == l_ori_file[i]:
            pool.apply_async(do_multiprocess,(each_code,))
    pool.close()
    pool.join()
    print "one time multiprocess"


    #name = ['operation','address']
    #os.system("mkdir "+"crafted\\"+origin_INPUT_PE)

    
    if "DO_EXIT" in os.environ:
        idc.qexit(1)
