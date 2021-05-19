import os
import random
from time import sleep
def random_str(str_length):
    randomlength = str_length
    str = ''
    chars = 'abcdefghijklmnopqrstuvwxyz0123456'
    length = len(chars) - 1
    random1 = random.Random()
    for i in range(randomlength):
        str += chars[random1.randint(0, length)]
    return str
def count_addr_file(path):
    count_addr_f = 0
    for root, dirs, files in os.walk(path):
        for dir1 in dirs:
            if dir1 == 'ADDR':
                # print root + "\\" + dir1
                count_addr_f += len(os.listdir(root + "\\" + dir1))

    return count_addr_f

while(1):
    print count_addr_file("..\\sample\\crafted\\")
    sleep(10)