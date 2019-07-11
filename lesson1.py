# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 13:11:55 2019

@author: ric
"""
网梗 = '''
网梗 = 问好 打招呼 自我介绍1 自我介绍2 自我介绍3 能力 爱好 爱好* 下手 不善 不善* 座右铭 句子
问好 = 各位观众 | 各位评委 | 江主席 | 各位学生 | Moss | 各位蜀军
打招呼 = 大家好 | 你们好 | 很高兴见到你们 | 感谢各位打开电梯 | 我有一言
自我介绍1 = 我是
自我介绍2 = 偶像练习生 | 香港记者 | 长者 | 西游记作者 | 中国航天员 | 铁道部发言人 | 给蓝猫配音的 | 王元姬的爷爷
自我介绍3 = 蔡徐坤 | 张宝华 | 成龙 | 六小龄童 | 吴京 | 特朗普 | 梁逸峰 | 贾君鹏 | 葛炮 | 王勇平 | 司徒王朗
能力 = 擅长
爱好 = null | 爱好 爱好*
爱好* = 唱 | 跳 | rap | 篮球 | 钦定 | 闷声发大财 | 听风就是雨 | 猴戏 | 英语 | 广告代言 | 绕口令
下手 = 不善长
不善 = null | 不善 不善*
不善* = 奔跑 | 学习一个 | 加特效 | 特殊的朗诵技巧 | 被水淹没 | 饶舌 | 回家吃饭 | 人群中认出光头 | 唱红日
座右铭 = 我的座右铭是
句子 = 爱慕拆尼斯 | duang | 亦可赛艇 | 什么叫国际巨星啊 | 没有人比我更懂贸易 | 八百标兵奔北坡 | 我反正是信了 | 岂不美哉
'''

影评 = '''
影评 = 称呼 分类 评价 最终评价
称呼 = 本片的 | 这片子的 | 本电影的 | 电影的 | 影片的
分类 = 剧情 | 特效 | 剧本 | 情节 | 画面 | 节奏 | 细节 | 演员 | 男主 | 女主 | 主人公 | 蔡徐坤 | 的的  
评价 = 一无是处啊 | 无能 | 情怀 | 好 | 很好 | 精彩 | 紧凑啊 | 莫名其妙 | 有趣呀 | 无趣 | 不好 | 神作啊 | 看不懂 | 无法理解 | 简单易懂 | 华丽
最终评价 = 值得一看 | 不值一看 | 厚颜无耻 | 超威蓝猫 | 爱慕安规
'''

import random
choice = random.choice

dict1 = {}
for i in 影评.split('\n')[1:-1]:
    
    dict1[i.split('=')[0].strip()] = [j.split() for j in i.split('=')[1].split('|')]

k = '影评'

def generate(dict1,k):
    if k not in dict1: return k
    expand =[generate(dict1,i) for i in choice(dict1[k])]
    return ''.join(i for i in expand if i != 'null')

def create_sentance(target,split_by):
    dict1 = {}
    for i in target.split('\n')[1:-1]:
        dict1[i.split(split_by)[0].strip()] = [j.split() for j in i.split('=')[1].split('|')]
    return dict1
dict1 = create_sentance(target=网梗,split_by='=')
generate(dict1,'网梗')

for i in range(10):
    print(generate(create_sentance(target=网梗,split_by='='),'网梗'))
    

import pandas as pd
train_csv = pd.read_csv(r'C:\Users\ric\Desktop\PBL\nlp\movie_comments.csv')
origin_text = train_csv['comment'].tolist()
len(origin_text)

import re
def token(string):
    return ''.join(re.findall('\w+',string))
string_clean = [''.join(token(str(a))) for a in origin_text]

import codecs
with codecs.open(r'C:\Users\ric\Desktop\PBL\nlp\article.txt', 'w',encoding='utf-8') as f:
    for i in string_clean:
        f.write(i+'\n')

volcub_list = []
import jieba

def cut(string):return list(jieba.cut(string))
for i,line in enumerate((codecs.open(r'C:\Users\ric\Desktop\PBL\nlp\article.txt',encoding='utf-8'))):
    if i % 100 == 0: print(i)
    volcub_list += cut(line)

from collections import Counter
words_count = Counter(volcub_list)
words_count.most_common(20)

def prob_1(word):
    return words_count[word]/len(volcub_list)

volcub_list = [str(t) for t in volcub_list]
volcub2_list = [''.join(volcub_list[i]+volcub_list[i+1]) for i in range(len(volcub_list[:-1]))]
words2_count = Counter(volcub2_list)

def prob_2(word_1,word_2):
    if word_1 + word_2 in words2_count:
        return words2_count[word_1+word_2]/len(volcub2_list)
    else:
        return 1/len(volcub2_list)

sentance = generate(create_sentance(target=影评,split_by='='),'影评')
def sentance_prob2(sentance):
    vol_list = cut(sentance)
    prob = 1
    for i in range(len(vol_list)-1):
        pro = prob_2(vol_list[i],vol_list[i+1])
        prob *= pro
    return prob

volcub3_list = [''.join(volcub2_list[i]+volcub_list[i+2]) for i in range(len(volcub_list[:-2]))]
words3_count = Counter(volcub3_list)
def prob_3(word_1,word_2,word_3):
    if word_1+word_2+word_3 in words3_count:return  words3_count[word_1+word_2+word_3]/len(volcub3_list)
    else:return 1/len(volcub3_list)

def sentance_prob3(sentance):
    vol_list = cut(sentance)
    prob = 1
    for i in range(len(vol_list)-2):
        pro = prob_3(vol_list[i],vol_list[i+1],vol_list[i+2])
        prob *= pro
    return prob

prob_score = []
sen_list = []
for k,sen in enumerate([generate(create_sentance(target=影评,split_by='='),'影评') for i in range(10)]):
    print('sen:{} pro2:{} pro3:{}'.format(sen,sentance_prob2(sen),sentance_prob3(sen)))
    prob_score.append((k,sentance_prob2(sen),sentance_prob3(sen),sen))

def generate_best(prob_score):
    print(sorted(prob_score,key = lambda x:x[2])[-1][-1])
generate_best(prob_score)

#模型问题 只考虑了三个词内的逻辑，然后现实中句子的逻辑跨度更大，比如实际情况下剧本好和不值一看不会同时出现

#============================================================================================================
train_txt = []
for i, sentence in enumerate((codecs.open(r'C:\Users\ric\Desktop\PBL\nlp\train.txt',encoding='utf-8'))):
    if i % 100 == 0: print(i)
    train_txt.append(sentence)


clean_txt = []
def clean_string(sen):
    return''.join(re.findall('\w+',sen.split('++$++')[2]))
for i in range(len(train_txt)):
    clean_txt.append(clean_string(train_txt[i]))

words_list = []
for i in clean_txt:
    words_list += [ word for word in (list(jieba.cut(i)))]

from collections import Counter
words_number_dict = Counter(words_list)
words_number_dict.most_common(10)
#——————————————————————————————————————————————————————————————————————————————————————————————————————————————
def is_variable(pat):
    return pat.startswith('?') and all(s.isalpha() for s in pat[1:])

def pat_match(pattern = 'My ?X told me something',saying= 'My mother is fuking you'):
    if not pattern or not saying: return []
    if is_variable(pattern[0]):
        try:
            return [(pattern[0],saying[0])] + pat_match(pattern[1:],saying[1:])
        except TypeError:
            return False
    else:
        if pattern[0] != saying[0]:return False
        else:
            return pat_match(pattern[1:],saying[1:])

pat_match('I want ?X a a'.split(),"I want holiday s s".split())

def pat_to_dict(patterns):
    return {k:v for k,v in patterns}

def subsitite(rule,parsed_rules):
    if not rule: return []
    return [parsed_rules.get(rule[0],rule[0])] + subsitite(rule[1:],parsed_rules)

got_patterns = pat_match("I wangt ?X".split(),"I wangt iPhone".split())
' '.join(subsitite("What if you mean if you got a ?X".split(), pat_to_dict(got_patterns)))

defined_patterns = {
    "I need ?X": ["Image you will get ?X soon", "Why do you need ?X ?"], 
    "My ?X told me something": ["Talk about more about your ?X", "How do you think about your ?X ?"]
}

def get_response(saying,defined_patterns):
    for rule in defined_patterns.keys():
        if pat_match('My ?X told me something'.split(),saying.split()):
            ans = choice(defined_patterns[rule])
            got_patterns = pat_match(rule.split(),saying.split())
            continue
    try:
        return ' '.join(subsitite(ans.split(), pat_to_dict(got_patterns)))
    except UnboundLocalError:
        return print('no matching rule')
    else:
        return ' '.join(subsitite(ans.split(), pat_to_dict(got_patterns)))
get_response('My mother is fuking you',defined_patterns)

#=============================================================================--
def is_pattern_segment(pattern):
    return pattern.startswith('?*') and all(a.isalpha() for a in pattern[2:])

from collections import defaultdict

fail = [True, None]

def pat_match_with_seg(pattern, saying):
    if not pattern or not saying: return []
    
    pat = pattern[0]
    
    if is_variable(pat):
        return [(pat, saying[0])] + pat_match_with_seg(pattern[1:], saying[1:])
    elif is_pattern_segment(pat):
        match, index = segment_match(pattern, saying)
        return [match] + pat_match_with_seg(pattern[1:], saying[index:])
    elif pat == saying[0]:
        return pat_match_with_seg(pattern[1:], saying[1:])
    else:
        return fail

def segment_match(pattern, saying):
    seg_pat, rest = pattern[0], pattern[1:]
    seg_pat = seg_pat.replace('?*', '?')

    if not rest: return (seg_pat, saying), len(saying)    
    
    for i, token in enumerate(saying):
        if rest[0] == token and is_match(rest[1:], saying[(i + 1):]):
            return (seg_pat, saying[:i]), i
    
    return (seg_pat, saying), len(saying)

def is_match(rest, saying):
    if not rest and not saying:
        return True
    if not all(a.isalpha() for a in rest[0]):
        return True
    if rest[0] != saying[0]:
        return False
    return is_match(rest[1:], saying[1:])

def strStr(source="aadf", target="a"):
    longth = len(target)
    for i in range(len(source)-longth+1):
#        print(i)
        if source[i:i+longth] == target:
            print(i)
            return i
    return -1

sorted([2,3,4,1,2])
