# -*- coding: utf-8 -*-

"""
@author: ZCH
@project: NER
@function: Transformation between SRs
@time: 2021/8/30 :37
"""

import re
import itertools

def seg_rep_tra(sou_file,pro_file,tra_sch):
    """
    Transition between different segment representations, supports eight conversions, including
    'iob2-io'、'bmeos-iob2'、'iobes-iob2'、'iob2-bi'、'ioe2-ie'、'iobes-bies'、'iob2-ioe2'、'iob2-iobes'.
    """
    
    with open(sou_file,'r',encoding = 'utf-8') as f, open(pro_file,'w',encoding = 'utf-8') as g:
        char_list = []
        tag_list = []
        for i in f.readlines():
            if len(i) != 1:
                char,tag = i.strip().split()
            else:
                char,tag = '\n',''
            char_list.append(char),tag_list.append(tag)
            
        if tra_sch == 'iob2-io':  
            for j in range(len(tag_list)):
                if tag_list[j].startswith('B-'):
                    tag_list[j] = re.sub('B-','I-',tag_list[j]) 
        elif tra_sch == 'bmeos-iob2':
            for j in range(len(tag_list)):
                if tag_list[j].startswith('S-'):
                    tag_list[j] = re.sub('S-','B-',tag_list[j])
                elif tag_list[j].startswith('M-'):
                    tag_list[j] = re.sub('M-','I-',tag_list[j])
                elif tag_list[j].startswith('E-'):
                    tag_list[j] = re.sub('E-','I-',tag_list[j])  
        elif tra_sch == 'iobes-iob2':
            for j in range(len(tag_list)):
                if tag_list[j].startswith('S-'):
                    tag_list[j] = re.sub('S-','B-',tag_list[j])
                elif tag_list[j].startswith('E-'):
                    tag_list[j] = re.sub('E-','I-',tag_list[j])
        elif tra_sch == 'iob2-bi':
            for j in range(len(tag_list)):
                if tag_list[j] == 'O' and tag_list[j-1] == '':
                    tag_list[j] = 'BO'
                elif tag_list[j] == 'O' and tag_list[j-1].startswith('B-'):
                    tag_list[j] = 'BO'
                elif tag_list[j] == 'O' and tag_list[j-1].startswith('I-'):
                    tag_list[j] = 'BO'
                elif tag_list[j] == 'O':
                    tag_list[j] = 'IO'
            for k,v in enumerate(tag_list):
                if tag_list[k] == 'BO':
                    tag_list[k] = re.sub('BO','B-O',tag_list[k])
                elif tag_list[k] == 'IO':
                    tag_list[k] = re.sub('IO','I-O',tag_list[k])      
        elif tra_sch == 'ioe2-ie':
            for j in range(len(tag_list)):
                if tag_list[j] == 'O' and tag_list[j+1] == '':
                    tag_list[j] = 'E-O'
                elif tag_list[j] == 'O' and tag_list[j+1].startswith('E-'):
                    tag_list[j] = 'E-O'
                elif tag_list[j] == 'O' and tag_list[j+1].startswith('I-'):
                    tag_list[j] = 'E-O'
                elif tag_list[j] == 'O':
                    tag_list[j] = 'I-O'            
        elif tra_sch == 'iobes-bies':
            for j in range(len(tag_list)):
                if tag_list[j] == 'O' and tag_list[j-1] != 'O' and tag_list[j+1] != 'O':
                    tag_list[j] = 'S-O'
            for p in range(len(tag_list)):
                if tag_list[p] == 'O' and tag_list[p-1] != 'O' and tag_list[p-1] != 'B-O':
                    tag_list[p] = 'B-O'
            for k in range(len(tag_list)):
                if tag_list[k] == 'O' and tag_list[k-1] == 'O' and tag_list[k+1] != 'O':
                    tag_list[k] = 'E-O'
            for l in range(len(tag_list)):
                if tag_list[l] == 'O' and tag_list[l-1] == 'B-O' and tag_list[l+1] != 'O' and tag_list[l+1] != 'E-O':
                    tag_list[l] = 'E-O'
            for h in range(len(tag_list)):
                if tag_list[h] == 'O':
                    tag_list[h] = 'I-O'
        elif tra_sch == 'iob2-ioe2':
            for j in range(len(tag_list)):
                if tag_list[j].startswith('B-'):
                    if (tag_list[j+1].startswith('B-')) or (tag_list[j+1].startswith('O')) or (tag_list[j+1] == ''):
                        tag_list[j] = re.sub('B-','E-',tag_list[j])
                    else:
                        len_ent = [len(list(v)) for k,v in itertools.groupby(tag_list[j+1:])][0]
                        tag_list[j] = re.sub('B-','I-',tag_list[j])
                        tag_list[j + len_ent] = re.sub('I-','E-',tag_list[j + len_ent])
        elif tra_sch == 'iob2-iobes':
            for j in range(len(tag_list)):
                if tag_list[j].startswith('B-'):
                    if (tag_list[j+1].startswith('B-')) or (tag_list[j+1].startswith('O')) or (tag_list[j+1] == ''):
                        tag_list[j] = re.sub('B-','S-',tag_list[j])
                    else:
                        len_ent = [len(list(v)) for k,v in itertools.groupby(tag_list[j+1:])][0]
                        tag_list[j + len_ent] = re.sub('I-','E-',tag_list[j + len_ent])
        
        for ch,ta in zip(char_list,tag_list):
            if ch != '\n':
                g.write(ch + ' ' + ta + '\n')
            else:
                g.write(ch)   
    
    