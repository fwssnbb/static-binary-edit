# coding:utf-8
import random
import os
import pickle
import pandas as pd
import time
import multiprocessing
from multiprocessing import Lock
from multiprocessing import Manager,Pool
ops_dir="./GA_initial_data/"
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

def get_opSequence(f):
    ret = []
    name = f
    src_path = os.path.join(ops_dir, f)
    #print(src_path)
    df = pd.read_csv(src_path, header=None, names=['address', 'size', 'feature'])
    df_list = df['feature'].tolist()
    a = ' '
    ret=a.join(df_list)
    return ret

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
    #print(weizhi)
    #print("dajiahao")
    return weizhi

def del_opSequence(files,labels,opsequences,each,opsequence,location,sum_count,all_count,ngram_opcode,ngrams):
    ops = opsequence.split(" ")
    #print(sum_count)
    #print("niqushi")
    binary=int2bin(location,sum_count)
    #print(len(binary))
    #print(binary)
    #print("buhaole")
    t = 0
    j = 0
    weizhi=modify(ops,binary,all_count,ngram_opcode,ngrams)
    for j in weizhi:
        if ops[j]=='mov':
            ops[j]='call'
        elif ops[j]=='call':
            ops[j]='jmp'
        elif ops[j]=='jz':
            ops[j]='call'
        else:
            print("mycode is error")
    ops=" ".join(ops)
    file=each+"+"+str(location)
    label=1
    files.append(file)
    labels.append(label)
    opsequences.append(ops)





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
    global features
    features = 2**sum_count-1
    #print(features)
    return sum_count,all_count,ngram_opcode,ngrams

def random_init(size):
    global features
    locations=[]
    for i in range(0,size):
        location = random.randint(1,features)
        #print(location)
        locations.append(location)
    return locations

def main(size):
    global features
    initial={}
    sum_count,all_count,ngram_opcode,ngrams=del_gram()
    all_files = os.listdir(ops_dir)

    for i,each in enumerate(all_files):
       (filename, extension) = os.path.splitext(each)
       if extension=='.ops':
           print ('gen ops for %s'%each)
           opcodes=get_opSequence(each)
           initial[each]=opcodes

    k = []
    n = len(all_files)

    for i in range(size):
        key=[]
        location = random.randint(1, features)
        i = i % n
        key.append(all_files[i])
        key.append(location)
        k.append(key)
    #print(k)
    #print("nihao")
    manager = Manager()
    files = manager.list()
    labels = manager.list()
    opsequences = manager.list()
    jobs = []
    N = multiprocessing.cpu_count()
    #print(N)
    pool=Pool()
    # return_list = manager.list() 也可以使用列表list
    for i,key in enumerate(k):
         pool.apply_async(del_opSequence,(files,labels,opsequences,key[0],initial[key[0]],key[1],sum_count,all_count,ngram_opcode,ngrams,))
    pool.close()
    pool.join()
    #print('finish')


    #print(type(files))
    #print(type(labels))
    #print(len(opsequences))
    files=list(files)
    labels=list(labels)
    opsequences=list(opsequences)

    pickle.dump(initial, open("./pkl/initial.pkl", "wb"))

    out=pd.DataFrame({'Id': files, 'Class': labels, 'feature': opsequences})
    #out.set_index(["Id"], inplace=True)
    out.to_csv("./GA_iteration/0.csv")
    #pickle.dump(out, open("./GA_iteration/0.pkl", "wb"))
    #print(files)
    #out.to_csv("./GA_iteration/initial.csv")
    pickle.dump(files, open("./pkl/initial_file.pkl", "wb"))
    #print('jiesu')
    return  sum_count







if __name__ == '__main__':
    start=time.clock()

    main(100)
    end=time.clock()
    print("Running time: %s S"%(end-start))
