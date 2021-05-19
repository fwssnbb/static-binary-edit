import os.path
import shutil
import os
import time
import sys

sharelist_ka="..\\..\\sharelist\\share-ka"
sharelist_360="..\\..\\sharelist\\share-360"
if os.path.isdir(sharelist_ka+"\\malware"):
    shutil.rmtree(sharelist_ka+"\\malware")
if os.path.isdir(sharelist_360+"\\malware"):
    shutil.rmtree(sharelist_360+"\\malware")
if os.path.exists(sharelist_ka+"\\BenignNum.txt"):
    os.remove(sharelist_ka+"\\BenignNum.txt")
if os.path.exists(sharelist_360+"\\360BenignNum.txt"):
    os.remove(sharelist_360+"\\360BenignNum.txt")

print(sys.argv[1])
malwarelist=sys.argv[1]
print('is scaning...')
sys.stdout.flush()
if os.path.isdir(malwarelist):
    print('the path exists')
    sys.stdout.flush()
    shutil.copytree(malwarelist, sharelist_ka+"\\malware")
    shutil.copytree(malwarelist, sharelist_360+"\\malware")
    sourcefilenum=len([lists for lists in os.listdir(malwarelist) if os.path.isfile(os.path.join(malwarelist, lists))])
    completednum=0
    while(completednum<2):
        if os.path.exists(sharelist_ka+"\\BenignNum.txt"):
            with open(sharelist_ka+"\\BenignNum.txt","r") as f:
                benignnum_ka=f.read()
                
                print("Kaspersky:  ")
                sys.stdout.flush()
                malwarenum_ka=int(float(sourcefilenum))-int(float(benignnum_ka))
                
                print("benign:",benignnum_ka,"   malware:",malwarenum_ka)
                sys.stdout.flush()
            os.remove(sharelist_ka+"\\BenignNum.txt")
            completednum=completednum+1
        if os.path.exists(sharelist_360+"\\360BenignNum.txt"):
            with open(sharelist_360+"\\360BenignNum.txt","r") as f:
                benignnum_360=f.read()
                
                print("360sd:  ")
                sys.stdout.flush()
                malwarenum_360=int(float(sourcefilenum))-int(float(benignnum_360))
               
                print("benign:",benignnum_360,"   malware:",malwarenum_360)
                sys.stdout.flush()
            os.remove(sharelist_360+"\\360BenignNum.txt")
            completednum=completednum+1
        time.sleep(10)
    sys.stdout.flush()
    print("completed")
    sys.stdout.flush()
else:
    
    print("path not exist")
    sys.stdout.flush()