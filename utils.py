import operator

import jieba
import jieba.posseg as pseg
import pandas as pd
jieba.load_userdict('D:\\code\\network_safe\\papersimilarity\\自定义词典.txt')
# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r',encoding='utf-8').readlines()]
    return stopwords
stopwords = stopwordslist('D:\\code\\network_safe\\papersimilarity\\stopwords\\cn_stopwords.txt')
def getSpyderData():
    data = pd.read_csv('../spyder_net_data/网络安全-FU/result.csv')
    print(data.columns)
    print(data.shape)
    return data

def getSplitNodeData():
    data = pd.read_csv('../generateNet/output/网络安全.csv')
    print(data.columns)
    print(data.shape)
    return data
def getNodeDict(title):
    '''
    获取嵌入切点
    :param title: 论文题目
    :return: 论文的嵌入节点
    '''
    data = getSplitNodeData()
    data['keywordsOfabstract'] = data['keywords'] + data['abstract']
    data = data[data['title'].isin(title)]
    data1 = data.groupby("title").apply(
        lambda x: str(x['node_id'].values).replace('[', '').replace(']', ''))  # ''.join( str(x['node_id']) )
    data2 = pd.DataFrame(data1)

    data2.to_csv('dict.csv')
    data = pd.read_csv('dict.csv')
    data.columns = ['title', 'authors']
    nodedict = dict(zip(data['title'], data['authors']))
    return nodedict

# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r',encoding='utf-8').readlines()]
    return stopwords


def gettitlelit(path,cluster):
    '''
    获取每个社团的论文题目列表
    :param path: 路劲
    :param cluster: 社团标签 -1返回所有
    :return:
    '''
    data = pd.read_csv(path)
    data = data.dropna(axis=0, subset=["title", "Cluster"])
    if cluster == -1:
        return list(set(data['title']))
    data = data[data['Cluster']== cluster]
    data = list(set(data['title']))
    return data

def getAbstract(path,cluster):
    '''
    获取每个社团的摘要
    :param path: 路劲
    :param cluster: 社团标签
    :return:
    '''
    data = pd.read_csv(path)
    data = data.dropna(axis=0, subset=["title", "Cluster"])
    data = data[data['Cluster']== cluster]
    data = list(set(data['title']))
    return data

def getNodeName(nodelist):
    '''
    通过节点id返回姓名字典
    :param nodelist:
    :return:
    '''
    data = pd.read_csv('./generateNet/output/网络安全.csv')
    data = data[data['node_id'].isin(nodelist)]
    namelist = data.set_index('node_id')['author'].to_dict()
    # namelist = data.set_index('node_id')['organ'].to_dict()
    sort_key_namelist = dict(sorted(namelist.items(), key=operator.itemgetter(0)))  # 按照key值升序
    return sort_key_namelist


# 中文分词
def tokenize(text):
    # words = jieba.lcut(text)
    words = pseg.lcut(text)
    # 保留名词和单词
    n_words = [word for word, pos in words if pos.startswith(('n','eng'))]
    outstr = []
    for word in n_words:
        if word not in stopwords:
            outstr.append(word)
    print(outstr)
    return outstr


import urllib.parse, urllib.request
import hashlib
import urllib
import random
import json

'''
翻译工具
'''
appid = '20230131001545872'
secretKey = 'NYnzX74ltxLbB6eiWfdR'
url_baidu = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
def translateBaidu(text, f='zh', t='en'):
    '''
     # 翻译
    :param text:
    :param f:
    :param t:
    :return:
    '''
    salt = random.randint(32768, 65536)
    sign = appid + text + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    url = url_baidu + '?appid=' + appid + '&q=' + urllib.parse.quote(text) + '&from=' + f + '&to=' + t + \
             '&salt=' + str(salt) + '&sign=' + sign
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    data = json.loads(content)
    result = str(data['trans_result'][0]['dst'])
    return result

def translate_list(input_list, source_language='zh', target_language='en', batch_size=100):
    '''
    分批次翻译
    :param input_list:
    :param source_language:
    :param target_language:
    :param batch_size:
    :return:
    '''
    translated_list = []
    num_batches = len(input_list) // batch_size + 1
    num = 1
    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = (i + 1) * batch_size
        # if end_idx > len(input_list):
        #     end_idx = len(input_list)
        batch_texts = input_list[start_idx:end_idx]
        print('进行到第{}批次'.format(num))
        # batch_translations = [translateBaidu(text, source_language, target_language) for text in batch_texts]
        batch_texts_str = '='.join(batch_texts)
        batch_translations = translateBaidu(batch_texts_str, source_language, target_language).split('=')
        num += 1
        translated_list.extend(batch_translations)
    return translated_list







# if __name__ == '__main__':
#     path = '.\keywordsImpatAuthor\input\diff_calculate.csv'
#     data = gettitlelit(path,0)
#     # print(data.columns,data.head())
#     print(data)


'''
if __name__ == '__main__':
    # nodelist = [962, 355, 611, 901, 1416, 329, 204, 2317, 2316, 1136, 1072, 242, 2484, 313, 411, 3390, 2591]
    # name = getNodeName(nodelist)
    # print(name)
    # print(name.values())
    path = 'D:\\code\\network_safe\\keywordsImpatAuthor\\input\\diff_calculate.csv'
    cluster = 0
    title = gettitlelit(path, cluster)
'''