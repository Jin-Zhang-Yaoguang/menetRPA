
import pandas as pd
from lxml import etree
from tqdm import tqdm
import os

folder_path_root = '/Users/jin/Desktop/project/python/menetRPA/spider/data/'
source = '4001-5000'
target = 'final'

folder_path = folder_path_root + source
target_path = folder_path_root + target + '/' + source + '.csv'

all_item = os.listdir(folder_path)
all_files = [folder_path + '/' + i for i in all_item]
all_files.sort()


def read_txt(file_path):
    f = open(file_path)
    line = f.readline().strip()  # 读取第一行
    txt = []
    txt.append(line)
    while line:  # 直到读取完文件
        line = f.readline().strip()  # 读取一行文件，包括换行符
        txt.append(line)
    f.close()  # 关闭文件

    page_source_txt = ''.join(txt)
    return page_source_txt


def extract_data(page_source):
    page_source = etree.HTML(page_source)
    header = page_source.xpath('*//div[@class="el-table-layout"]/table/tr')[0]
    data = page_source.xpath('*//div[@class="el-table-layout"]/table/tr')[1:]

    header_list = []
    data_list = []
    for i in header.xpath('*'):
        header_list.append(i.xpath('span/text()')[0])

    for line in data:
        line_list = []
        for i in line.xpath('*'):
            try:
                cell = i.xpath('span/text()')[0]
            except:
                cell = ''
            line_list.append(cell)
        data_list.append(line_list)

    df = pd.DataFrame(data=data_list, columns=header_list)
    return df


for i, file in enumerate(tqdm(all_files)):
    page_source_txt = read_txt(file)
    if i == 0:
        df_final = extract_data(page_source_txt)
    else:
        df = extract_data(page_source_txt)
        df_final = pd.concat([df_final, df])

df_final.to_csv(target_path, index=False)