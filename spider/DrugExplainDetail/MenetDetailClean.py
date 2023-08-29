
import pandas as pd
from lxml import etree
from tqdm import tqdm
import os

folder_path_root = '/Users/jin/Desktop/project/python/menetRPA/spider/spider/DrugExplainDetail/data/'
source = '100001-150000'
target = 'final'

folder_path = folder_path_root + source
target_path = folder_path_root + target + '/' + source + '.csv'

all_item = os.listdir(folder_path)
all_files = [folder_path + '/' + i for i in all_item if '.txt' in i]
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
    drug_name = page_source.xpath('*//div[@class="detail"]/h2/text()')[0]

    drug_details = page_source.xpath('*//div[@class="detail"]/div[@class="detail-list"]/ul')


    result = {}
    for drug_detail in drug_details:
        key = drug_detail.xpath('li')[0].xpath('text()')[0].replace('：', '')
        value = ''
        try:
            value = drug_detail.xpath('li')[1].xpath('text()')[0]
        except:
            value = ''
        result[key] = value

    header_list = ['drug_details']
    data_list = [str(result)]
    df = pd.DataFrame(data=data_list, columns=header_list)
    return df


for i, file in enumerate(tqdm(all_files)):
    page_source_txt = read_txt(file)
    if i == 0:
        df_final = extract_data(page_source_txt)
    else:
        try:
            df = extract_data(page_source_txt)
            df_final = pd.concat([df_final, df])
        except:
            pass


df_final.to_csv(target_path, index=False)
