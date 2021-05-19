#coding = utf-8
import pandas as pd
import argparse
import os



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--outputDir', dest='outputDir', default='..\\..\\..\\sample\\output\\filter_success\\',\
            help='the output dir you choose')
    args = parser.parse_args()
    outputDir = args.outputDir

    input_file_list = os.listdir(outputDir)
    print(input_file_list)
    df_success_av = pd.read_csv("..\\..\\..\\sharelist\\share-ka\\"+ "返回后文件名字.csv")
    print(df_success_av.head())

    for i, file1 in enumerate(input_file_list):
