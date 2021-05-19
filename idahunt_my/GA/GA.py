# coding:utf-8
import math, random
import GA_initial as initial
import GA_iteration as iteration
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import time
class Population:
    # 种群的设计
    def __init__(self, size, chrom_size, cp, mp, gen_max):
        # 种群信息合
        self.individuals = []  # 个体集合
        #self.initials=[] #初始样本
        self.fitness = []  # 个体适应度集
        self.selector_probability = []  # 个体选择概率集合
        self.new_individuals = []  # 新一代个体集合

        self.elitist = {'chromosome': 0, 'fitness': 0, 'age': 0}  # 最佳个体的信息

        self.size = size  # 种群所包含的个体数
        self.chromosome_size = chrom_size  # 个体的染色体长度
        self.crossover_probability = cp  # 个体之间的交叉概率
        self.mutation_probability = mp  # 个体之间的变异概率

        self.generation_max = gen_max  # 种群进化的最大世代数
        self.age = 0  # 种群当前所处世代

        # 随机产生初始个体集，并将新一代个体、适应度、选择概率等集合以 0 值进行初始化
        v = 2 ** self.chromosome_size - 1
        for i in range(self.size):
            self.new_individuals.append(0)
            self.fitness.append(0)
            self.selector_probability.append(0)
        #self.individuals=initial.main()
        p=pickle.load(open("./pkl/initial_file.pkl", "rb"))
        self.individuals=p
        #print(len(self.individuals))
        #print("zmhuishi")
        #self.initials = pickle.load(open("./pkl/initial_opcode.pkl", "rb"))
        #print(len(self.initials))
    # 基于轮盘赌博机的选择


    def fitness_func(self):
        score=[]
        corpus=[]
        #print(age)
        #print("age")
        '''适应度函数，可以根据个体的两个染色体计算出该个体的适应度'''
        '''
        for i in range(self.size):
            score.append(0.3)
        '''
        df = pd.read_csv("./GA_iteration/"+str(self.age)+".csv")
        #df = pickle.load(open("./GA_iteration/"+str(self.age)+".pkl", "rb"))
        for i in df["feature"]:
            corpus.append(i)
        #print(df)

        feature_path = '../pkl/feature.pkl'
        loaded_vec = pickle.load(open(feature_path, "rb"))
        # 加载TfidfTransformer
        tfidftransformer_path = '../pkl/tfidftransformer.pkl'
        tfidftransformer = pickle.load(open(tfidftransformer_path, "rb"))
        #测试用transform，表示测试数据，为list
        test_tfidf = tfidftransformer.transform(loaded_vec.transform(corpus))
        word=loaded_vec.get_feature_names()#获取词袋模型中的所有词语  
        weight=test_tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
        #print(word)
        #print("nihao")
        np.set_printoptions(threshold=np.inf)
        #print(weight)
        newdata=pd.DataFrame(weight,columns=word)
        newdata["Class"]=df["Class"].tolist()
        newdata["Id"]=df["Id"].tolist()
        #print(newdata["Class"])
        model = pickle.load(open("../pkl/xgb_python3.pkl", "rb"))
        #print(newdata)
        xtest = newdata
        XX=xtest.copy()
        del XX['Id']
        del XX['Class']
        XX = np.array(XX)
        probability = model.predict_proba(XX)
        score = [i[0] for i in probability]
        #print(len(score))
        return score

    def evaluate(self):
        '''用于评估种群中的个体集合 self.individuals 中各个个体的适应度'''
        sp = self.selector_probability
        #print(self.individuals)
        #print("nihao")
        self.fitness = self.fitness_func() # 将计算结果保存在 self.fitness 列表中
        #print -1, max(self.fitness), sum(self.fitness) / self.size, min(self.fitness)
        ft_sum = sum(self.fitness)
        for i in range(self.size):
            sp[i] = self.fitness[i] / float(ft_sum)  # 得到各个个体的生存概率
        #print(sp)
        #print("fanweisong")
        for i in range(1, self.size):
            sp[i] = sp[i] + sp[i - 1]  # 需要将个体的生存概率进行叠加，从而计算出各个个体的选择概率
        #print(self.selector_probability)
        #print("fenkai")
        #print(sp)
        #print("shaoleishi")
    # 轮盘赌博机（选择）
    def select(self):
        (t, i) = (random.random(), 0)
        #print(t)
        for p in self.selector_probability:
            #print(p)
            if p > t:
                break
            i = i + 1
        #print("ddddd")
        #print(i)
        return i

    # 交叉
    def cross(self, chrom1, chrom2):
        #print(chrom1)

        chrom1 = initial.int2bin(chrom1, self.chromosome_size)
        chrom2 = initial.int2bin(chrom2, self.chromosome_size)
        #print(chrom1)
        #print(chrom2)
        p = random.random()  # 随机概率
        #print("ni")
        if chrom1 != chrom2 and p < self.crossover_probability:
            ts=[]
            chrom1 = list(chrom1)
            chrom2 = list(chrom2)
            for i in range(random.randint(1,5)):
                t = random.randint(1, self.chromosome_size - 1)  # 随机选择一点（单点交叉）
                ts.append(t)
            #print(ts)
            #print("tamenhao")
            for t in ts:
                temp= chrom1[t]
                chrom1[t]=chrom2[t]
                chrom2[t]=temp
            chrom1=''.join(chrom1)
            chrom2=''.join(chrom2)

            #print(chrom1)
            #print(chrom2)
        return (chrom1, chrom2)

    # 变异
    def mutate(self, chrom):
        p = random.random()
        #print(p)
        #print(chrom)
        #print("shaya")
        if p < self.mutation_probability:
            ts=[]
            chrom = list(str(chrom))
            #print(chrom)
            for i in range(random.randint(1, 5)):
                t = random.randint(1, self.chromosome_size-1)
                ts.append(t)
            #print(ts)
            #print("tamen")
            for t in ts:
                #print(len(chrom))
                #print(t)
                chrom[t]=str(1-int(chrom[t]))
            chrom = ''.join(chrom)
        #print(chrom)
        return chrom

    # 保留最佳个体
    def reproduct_elitist(self):
        # 与当前种群进行适应度比较，更新最佳个体
        j = -1
        for i in range(self.size):
            if self.elitist['fitness'] < self.fitness[i]:
                j = i
                self.elitist['fitness'] = self.fitness[i]
        if (j >= 0):
            self.elitist['chromosome']= self.individuals[j]
            self.elitist['age'] = self.age

    # 进化过程
    def evolve(self):
        indvs = self.individuals
        new_indvs = self.new_individuals
        # 计算适应度及选择概率
        self.evaluate()
        #print(self.individuals)
        #print(self.fitness)
        #print(max(self.fitness), sum(self.fitness) / self.size, min(self.fitness))
        #print("nimenhao")
        # 进化操作
        i = 0
        while True:
            # 选择两个个体，进行交叉与变异，产生新的种群
            idv1 = self.select()
            idv2 = self.select()
            # 交叉
            #print(idv1)
            idv1 = indvs[idv1]
            idv2 = indvs[idv2]
            #print(idv1)
            #print("tahao")
            biaozhi1 = idv1.split("+")[0]
            biaozhi2 = idv2.split("+")[0]
            idv1 = int(idv1.split("+")[1])
            idv2 = int(idv2.split("+")[1])
            (idv1, idv2) = self.cross(idv1, idv2)
            # 变异
            idv1 = self.mutate(idv1)
            idv2 = self.mutate(idv2)
            idv1=int(idv1, 2)
            idv2=int(idv2, 2)
            idv1=biaozhi1+"+"+str(idv1)
            idv2=biaozhi2+"+"+str(idv2)
            new_indvs[i]= idv1 # 将计算结果保存于新的个体集合self.new_individuals中
            new_indvs[i + 1] = idv2
            #print(new_indvs)
            #print("womenhao")
            # 判断进化过程是否结束
            i = i + 2  # 循环self.size/2次，每次从self.individuals 中选出2个
            if i >= self.size:
                break

        # 最佳个体保留
        # 如果在选择之前保留当前最佳个体，最终能收敛到全局最优解。
        self.reproduct_elitist()
        # 更新换代：用种群进化生成的新个体集合 self.new_individuals 替换当前个体集合
        for i in range(self.size):
            self.individuals[i] = self.new_individuals[i]
        iteration.main(self.individuals, self.age)
        #print(self.individuals)
        #print(self.initials)
        #print("chengkai")
    def run(self):
        age_list=[]
        max_fitness_list=[]
        avg_fitness_list=[]
        min_fitness_list=[]
        '''根据种群最大进化世代数设定了一个循环。
        在循环过程中，调用 evolve 函数进行种群进化计算，并输出种群的每一代的个体适应度最大值、平均值和最小值。'''
        for i in range(self.generation_max):
            self.age=i
            self.evolve()
            #print(self.individuals)

            #print(self.fitness)
            print(self.age, max(self.fitness), sum(self.fitness) / self.size, min(self.fitness))
            age_list.append(self.age)
            max_fitness_list.append(max(self.fitness))
            avg_fitness_list.append(sum(self.fitness)/self.size)
            min_fitness_list.append(min(self.fitness))
        plt.title('GA Result Analysis')
        plt.plot(age_list, max_fitness_list,color='green', label='Max Score')
        plt.plot(age_list, avg_fitness_list, color='red', label='Avg Score')
        plt.plot(age_list, min_fitness_list, color='blue', label='Min Score')
        plt.legend()  # 显示图例
        plt.xlabel('iteration times')
        plt.ylabel('score')
        plt.show()
        #print("liuyuanzhao")
        #print(self.elitist)


if __name__ == '__main__':
    # 种群的个体数量为 50，染色体长度为 25，交叉概率为 0.8，变异概率为 0.1,进化最大世代数为 150
    size = 500
    cross_probability = 0.8
    mutation_probability = 0.1
    generation_max = 100
    parser = argparse.ArgumentParser(prog="GA", description='Get GA iteration results.')
    parser.add_argument("-s", "--size", default=size, help="a number containing initial samples size",
                        type=int)
    parser.add_argument("-c", "--cross", default=cross_probability, help="a float containing cross probability",
                        type=float)
    parser.add_argument("-m","--mutation", default=mutation_probability,help="a float containing mutation probability",
                        type=float)
    parser.add_argument("-g", "--generation", default=generation_max,help="a number containing max generation",
                        type=int)
    # parser.add_argument("-m", "--multiprocess", help="the number of processes", type=int)
    args = parser.parse_args()
    if args.size%2!=0:
        args.size+=1
    count=initial.main(args.size)
    pop = Population(args.size, count, args.cross, args.mutation, args.generation)
    pop.run()
