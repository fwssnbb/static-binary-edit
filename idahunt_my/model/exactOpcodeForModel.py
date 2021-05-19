# -*- coding = utf-8 -*-
import os
import time
import subprocess
import sys
import shlex
import shutil
import time
import random
import pandas as pd
import argparse

GBK = 'gbk'
UTF8 = 'utf-8'
current_encoding = UTF8


def exec_intime(cmd_str):
    cmd_tmp = shlex.split(cmd_str)
    # print cmd_tmp
    tmp1 = subprocess.Popen(cmd_tmp,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            bufsize=1
                            )

    while tmp1.poll() is None:
        r = tmp1.stdout.readline().decode(current_encoding)
        sys.stdout.write(r)
        sys.stdout.flush()
    if tmp1.poll() != 0:
        err = tmp1.stderr.read().decode(current_encoding)
        sys.stdout.write(err)
        sys.stdout.flush()


def random_str(str_length):
    randomlength = str_length
    str = ''
    chars = 'abcdefghijklmnopqrstuvwxyz0123456'
    length = len(chars) - 1
    random1 = random.Random()
    for i in range(randomlength):
        str += chars[random1.randint(0, length)]
    return str


def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


def count_addr_file(path):
    count_addr_f = 0
    for root, dirs, files in os.walk(path):
        for dir1 in dirs:
            if dir1 == 'ADDR':
                # print root + "\\" + dir1
                count_addr_f += len(os.listdir(root + "\\" + dir1))

    return count_addr_f


def copy_crafted_file(path):
    for file1 in os.listdir(path):
        # print path+file1
        if os.path.isfile(path + file1) and file1.endswith('.call'):
            # print file1, 'is a file'
            for i in range(9):
                shutil.copy(path + file1, path + file1 + str(i))


def delete_copy_file(path):
    for file1 in os.listdir(path):
        if file1.endswith('.call0') or file1.endswith('.call1') or file1.endswith('.call2') \
                or file1.endswith('.call3') or file1.endswith('.call4') or file1.endswith('.call5') \
                or file1.endswith('.call6') or file1.endswith('.call7') or file1.endswith('.call8'):
            os.remove(path + file1)


def mov_exe_for_upx(in_path, to_path):
    for root, dirs, files in os.walk(in_path):
        for dir1 in dirs:
            if dir1 == 'EXE':
                for each in os.listdir(root + '\\' + dir1):
                    shutil.move(root + '\\' + dir1 + '\\' + each, to_path)
                    # print root+ '\\' + dir1


def do_upx(input_dir, output_dir, num_to_generate):
    files = os.listdir(input_dir)
    for file1 in files:
        print("Deal with file:" + file1)
        for i in range(num_to_generate):
            random_key = random_str(10)
            tmp = os.popen("something\\shell_new.exe " + input_dir + file1 + " -o " + output_dir + file1 + '_' + random_key).read()
            #print tmp


def copy_ops_for_GA(from_dir, to_dir):
    files = os.listdir(from_dir)
    # print files
    for file1 in files:
        if file1.endswith('.ops'):
            # print from_dir + '\\' + file1
            shutil.copy(from_dir + '\\' + file1, to_dir)

def delete_ops(in_dir):
    files = os.listdir(in_dir)
    for file1 in files:
        if file1.endswith('.ops'):
            # print from_dir + '\\' + file1
            os.remove(os.path.join(in_dir,file1))

def delete_dir_files(in_dir):
    files = os.listdir(in_dir)
    for file1 in files:
        os.remove(os.path.join(in_dir, file1))

def delete_craftedcall_files(in_dir):
    if os.path.exists(in_dir):
        files = os.listdir(in_dir)
        for file1 in files:
            if file1.endswith(".crafted.call"):
                os.remove(os.path.join(in_dir, file1))
    else:
        print "no %s dir"%in_dir

def delete_dir_csv_files(in_dir):
    files = os.listdir(in_dir)
    for file1 in files:
        if file1.endswith(".csv"):
            os.remove((os.path.join(in_dir, file1)))


def mov_csv_from_GA(in_dir, to_dir, csv_name):
    for file1 in os.listdir(in_dir):
        if file1 == csv_name:
            shutil.move(os.path.join(in_dir, csv_name), to_dir)

def calc_the_input_exe_num(in_dir):
    files_in_dir = os.listdir(in_dir)
    input_exe_list = []
    for file1 in files_in_dir:
        if file1.endswith(".exe"):
            input_exe_list.append(file1)
    return len(input_exe_list)
'''
def handle_csv(csv_path, ref_dir, number):
    files_ref_dir = os.listdir(ref_dir)
    input_files_list = []
    for file1 in files_ref_dir:
        if file1.endswith(".exe"):
            input_files_list.append(file1)
    df_150csv = pd.read_csv(os.path.join(csv_path,"150.csv"))
    operation_list = df_150csv['code'].tolist()

    result_op_list = []
    result_file_list = []
    for i in range(int(number)):
        result_file_list.append(random.choice(input_files_list))
        result_op_list.append(random.choice(operation_list))

    df_new = pd.DataFrame({'ori_file':result_file_list,'code':result_op_list})
    df_new.to_csv(os.path.join(csv_path,"initial.csv"))
    print "already handle csv"
'''

def add_exe_suffix(in_dir):
    files = os.listdir(in_dir)
    for file1 in files:
        if not file1.endswith('.exe') and os.path.isfile(file1):
            os.rename(in_dir + file1,in_dir + file1+'.exe')

def filter_sample(in_dir,ref_dir,out_dir):
    files_in_dir = os.listdir(in_dir)
    files_ref_dir = os.listdir(ref_dir)
    for file1 in os.listdir(in_dir):
        if file1[4:] in files_ref_dir:
            shutil.move(os.path.join(ref_dir,file1[4:]),out_dir)

def filter_upx_sample(in_dir,ref_dir,out_dir):
    files_in_dir = os.listdir(in_dir)
    files_ref_dir = os.listdir(ref_dir)
    for file1 in os.listdir(in_dir):
        if file1[4:-11] in files_ref_dir:
            shutil.move(os.path.join(ref_dir, file1[4:-11]), out_dir)

# ********************************************
# origin script by qiu
# ********************************************
def exe_qiu():

    if not os.path.exists("..\\..\\sample\\crafted"):
        os.system("mkdir " + "..\\..\\sample\\crafted")

    os.popen(r'python3 .\idahunt.py --inputdir ..\..\sample\ --cleanup --temp-cleanup').read()
    os.popen(r'python3 .\idahunt.py --inputdir ..\..\sample\crafted --cleanup --temp-cleanup').read()

    tmp1 = subprocess.Popen(['python3',r'.\idahunt.py',
    '--inputdir',r'..\..\sample',
    '--scripts',r'flatten_instrument.py',
    '--analyse','--max-ida','50'],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
    bufsize = 1
    )

    while tmp1.poll() is None:
        r = tmp1.stdout.readline().decode(current_encoding)
        sys.stdout.write(r)
        sys.stdout.flush()
    if tmp1.poll() != 0:
        err = tmp1.stderr.read().decode(current_encoding)
        sys.stdout.write(err)
        sys.stdout.flush()

    if not os.path.exists("..\\..\\sample\\crafted\\EXE"):
        os.system("mkdir " + "..\\..\\sample\\crafted\\EXE")

    tmp2 = subprocess.Popen(['python3',r'.\idahunt.py',
    '--inputdir',r'..\..\sample\crafted',
    '--scripts',r'recover_env.py',
    '--analyse','--max-ida','50'],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
    bufsize = 1)

    while tmp2.poll() is None:
        r = tmp2.stdout.readline().decode(current_encoding)
        sys.stdout.write(r)
        sys.stdout.flush()
    if tmp2.poll() != 0:
        err = tmp2.stdout.readline().decode(current_encoding)
        sys.stdout.write(err)
        sys.stdout.flush()
#*********************************************
#upx
#*************************************************
def exe_upx(number):
    # mov generated exe to upx
    print "upx num is ",number
    os.system("mkdir " + "..\\..\\sample\\output")
    os.system("mkdir " + "..\\..\\sample\\output\\origin")
    os.system("mkdir " + "..\\..\\sample\\output\\after")
    mov_exe_for_upx('..\\..\\sample\\crafted\\', '..\\..\\sample\\output\\origin\\')

    do_upx('..\\..\\sample\\output\\origin\\', '..\\..\\sample\\output\\after\\', number)
#*****************************************************
#GA
#*****************************************************


# ****************************************************
# new script by me
# ****************************************************
def exe_liu():
    pass





if __name__ == '__main__':
    os.chdir("..\\idahunt\\")
    tmp_path = os.getcwd()
    print tmp_path
    sys.stdout.flush()
    start_time = time.time()


    print os.popen(r'python3 ..\idahunt\idahunt.py --inputdir ..\..\exe_sample\goodware --cleanup --temp-cleanup').read()
    print os.popen(r'python3 ..\idahunt\idahunt.py --inputdir ..\..\exe_sample\malware --cleanup --temp-cleanup').read()


    tmp = os.popen(r'python3 ..\idahunt\idahunt.py --inputdir ..\..\exe_sample\goodware --scripts .\exactOpSequence.py --analyse').read()
    print tmp
    tmp = os.popen(r'python3 ..\idahunt\idahunt.py --inputdir ..\..\exe_sample\malware --scripts .\exactOpSequence.py --analyse').read()
    print tmp
    print os.popen(r'python3 ..\idahunt\idahunt.py --inputdir ..\..\exe_sample\goodware --cleanup --temp-cleanup').read()
    print os.popen(r'python3 ..\idahunt\idahunt.py --inputdir ..\..\exe_sample\malware --cleanup --temp-cleanup').read()

    delete_dir_files("..\\GA\\GA_initial_data\\")
    copy_ops_for_GA("..\\..\\exe_sample\\malware", "..\\GA\\GA_initial_data\\")

    delete_dir_files("..\\..\\opcode_sample\\goodware_feature")
    copy_ops_for_GA("..\\..\\exe_sample\\goodware", "..\\..\\opcode_sample\\goodware_feature\\")
    delete_ops("..\\..\\exe_sample\\goodware")

    delete_dir_files("..\\..\\opcode_sample\\malware_feature")
    copy_ops_for_GA("..\\..\\exe_sample\\malware", "..\\..\\opcode_sample\\malware_feature\\")
    delete_ops("..\\..\\exe_sample\\malware")

    #print os.getcwd()
    #os.chdir("..\\GA\\")
    #exec_intime('python3 ./GA.py -s 20 -c 0.8 -m 0.1 -g 5')
    #os.chdir("..\\idahunt\\")

    end_time = time.time()
    print "Took {} to execute this".format(hms_string(end_time - start_time))

print "feature exact over!"