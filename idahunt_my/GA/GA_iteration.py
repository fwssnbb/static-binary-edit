# coding:utf-8
import random
import os
import pickle
import pandas as pd
import multiprocessing
from multiprocessing import  Pool
from multiprocessing import Manager
asm_dir="./GA_initial_data/"
gram={}
ngrams=[]
all_count=[]
ngram_opcode=[]
sum_count=0
features=0
def place(zi,mu):
    """查询子字符串在大字符串中的所有位置"""
    len1 = len(zi)
    pl = []
    for each in range(len(mu)-len1):
        if mu[each:each+len1] == zi:   #找出与子字符串首字符相同的字符位置
            pl.append(each)
    return pl



def int2bin(n, count):
    """returns the binary of integer n, using count number of digits"""
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])


def find_all(sub, s):
    index_list=[]
    for i in range(len(s)):
        length = len(sub)
        if s[i:i + length] == sub:
            index_list.append(i)
    if len(index_list) > 0:
        return index_list
    else:
        return -1

def modify(ops,binary,all_count,ngram_opcode,ngrams):
    weizhi=[]
    t=0
    j=0
    for k,i in enumerate(all_count):
        j+=i
        #print(type(binary[t:j]))
        #print("ta")
        if binary[t:j].find('1')!=-1:
            xiugai=binary[t:j]
            #print(ngram_opcode)
            #print("buzhidao")
            gram=ngram_opcode[k]
            #print(type(gram))
            #print("zheyangba")
            gram=gram.split(" ")
            ngram_list=find_all(gram,ops)
            #print(ngram_list)
            if ngram_list!=-1:
                #print(ngram_list)
                for w in  ngram_list:
                    #print(w)
                    #print("ganmeshi")
                    for m,n in enumerate(xiugai):
                        #print(m)
                        #print(n)
                        if n=='1':
                            weizhi.append(w+ngrams[k][m])
                            #print(weizhi)
        t=j
    weizhi = list(set(weizhi))
    ##print(weizhi)
    #print("liyin")
    return weizhi

def del_opSequence(files,labels,opsequences,each,sum_count,all_count,ngram_opcode,ngrams):
    #print(locations[1])
    #print(type(locations[1]))
    #print(i)
    #location = int(each.split("+")[1])
    #print(location)
    #print("nihaoma")
    #print(i[7])
    # pd.set_option('display.width',1000)

    initial_path="./pkl/initial.pkl"
    f=open(initial_path,"rb")
    initial = pickle.load(f)
    f.close()


    #print(i.split("+")[0])
    #print(initial)
    ops = initial[each.split("+")[0]]

    location = int(each.split("+")[1])
    #print(ops)
    #print(ops)
    #print('nihaoya')
    ops = str(ops).split(" ")
    #print(ops)
    #print(sum_count)
    binary = int2bin(location, sum_count)
    #print(binary)
    weizhi = modify(ops, binary,all_count,ngram_opcode,ngrams)
    #print(weizhi)
    # print(len(weizhi))
    for j in weizhi:
        if ops[j] == 'mov':
            ops[j] = 'call'
        elif ops[j] == 'call':
            ops[j] = 'jmp'
        elif ops[j] == 'jz':
            ops[j] = 'call'
        else:
            print("mycode is error")
    ops = " ".join(ops)
    file = each
    label = 1
    files.append(file)
    labels.append(label)
    opsequences.append(ops)

    #print(len(opse))




def del_gram():
    global all_count
    global ngram_opcode
    global ngrams
    feature_path = '../pkl/corpus.pkl'
    loaded_vec = pickle.load(open(feature_path, "rb"))
    #print(loaded_vec)
    for each in loaded_vec:
        ngram=[]
        #print(each)
        count=0
        nmov=0
        ncall=0
        njz=0
        each=each.strip("\n")
        ngram_opcode.append(each)
        for i,opcode in enumerate(each.split(" ")):
            if opcode=='mov':
                nmov+=1
                ngram.append(i)
            if opcode=='call':
                ncall+=1
                ngram.append(i)
            if opcode=='jz':
                njz+=1
                ngram.append(i)

            '''
            if opcode=='xor':
                nxor+=1
                ngram.append(i)
            '''
        count=nmov+ncall+njz
        #print(count)
        ngrams.append(ngram)
        all_count.append(count)
    global sum_count
    sum_count = sum(all_count)
    #print(all_count)
    #print(sum_count)
    #print(gram)
    global features
    features = 2**sum_count-1
    return sum_count, all_count, ngram_opcode, ngrams
    #print(features)


def main(samples,locations):
    global features
    sum_count, all_count, ngram_opcode, ngrams=del_gram()
    #print(locations)
    #print(samples)
    manager = Manager()
    files = manager.list()
    labels = manager.list()
    opsequences = manager.list()
    N = multiprocessing.cpu_count()
    #print(N)
    pool = Pool()
    # return_list = manager.list() 也可以使用列表list
    for each in samples:
        pool.apply_async(del_opSequence, (files, labels, opsequences, each, sum_count, all_count, ngram_opcode, ngrams,))
    pool.close()
    pool.join()
    #print('finish too')

    #print(type(files))
    #print(type(labels))
    #print(len(opsequences))
    files = list(files)
    labels = list(labels)
    opsequences = list(opsequences)
    #print(len(opsequence))
    out=pd.DataFrame({'Id': files, 'Class': labels, 'feature': opsequences})
    locations=locations+1
    #out.set_index(["Id"], inplace=True)
    #pickle.dump(out, open("./GA_iteration/"+str(locations)+".pkl", "wb"))
    out.to_csv("./GA_iteration/"+str(locations)+".csv")
    #print('jiesu')




if __name__ == '__main__':
    main([1,2],0)
