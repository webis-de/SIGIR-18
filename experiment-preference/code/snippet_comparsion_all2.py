#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs, csv, pickle
import numpy as np
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import nltk.data
import sys
from scipy import stats


_sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
lmtzr = WordNetLemmatizer()

snippet_dir = '../data/'

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

def get_two_sample_one_side_power(d1,d2,alpha=0.05):
    mean1 = np.mean(d1)
    var1 = np.var(d1)
    
    mean2 = np.mean(d2)
    var2 = np.var(d2)
    
    k = len(d1)/len(d2)
    
    z = (mean1-mean2) / np.sqrt(var1+var2/k) * np.sqrt(len(d1))
    power=stats.norm.cdf(z-stats.norm.ppf(1-alpha))
    
    return power

def get_cohen_d(d1,d2,alpha=0.05):
    mean1 = np.mean(d1)
    std_all = np.std([d1,d2])
    
    mean2 = np.mean(d2)
        
    return (mean1-mean2)/std_all

with codecs.open(snippet_dir+'snippet_compare_answer_part1.tsv','r', encoding="utf-8") as f:
    lines = [line for line in f]


ansDic = {}
wikiDic = {}
wikicount = 0
for line in lines:
    case = line.split('\t')[0]
    ans = line.split('\t')[-1]
    ansDic[int(case)] = int(ans)
    title = line.split('\t')[2]
    if title[-9:] == 'Wikipedia':
        wikiDic[int(case)] = True
        wikicount += 1
    else:
        wikiDic[int(case)] = False

with codecs.open(snippet_dir+'snippet_compare_answer_part2.tsv','r', encoding="utf-8") as f:
    lines = [line for line in f]    
        
for line in lines:
    case = int(line.split('\t')[0])+600
    ans = line.split('\t')[-1]
    ansDic[case] = int(ans)
    title = line.split('\t')[2]
    if title[-10:] == 'Wikipedia"':
        wikiDic[case] = True
        wikicount += 1
    else:
        wikiDic[case] = False

print 'wiki:',wikicount

part1File = snippet_dir+'snippet_compare_result_part1.csv'
part2File = snippet_dir+'snippet_compare_result_part2.csv'

part3File = snippet_dir+'snippet_compare_result_part3.csv'


reader1 = unicode_csv_reader(open(part1File))
reader2 = unicode_csv_reader(open(part2File))

reader3 = unicode_csv_reader(open(part3File))

par1 = []
ori1 = []
par2 = []
ori2 = []

b1 = []
w1 = []
b2 = []
w2 = []

l1 = []
s1 = []
l2 = []
s2 = []

p1_wi = []
p1_nw = []
o1_wi = []
o1_nw = []

p2_wi = []
p2_nw = []
o2_wi = []
o2_nw = []


# (better-reuse, worse-paraphrase) 
# (better-paraphrase, worse-reuse)
# (long-reuse, short-paraphrase) 
# (long-paraphrase, short-reuse)

br1 = []
wp1 = []
bp1 = []
wr1 = []

br2 = []
wp2 = []
bp2 = []
wr2 = []

lr1 = []
sp1 = []
lp1 = []
sr1 = []

lr2 = []
sp2 = []
lp2 = []
sr2 = []

labeltypes = np.zeros(4)


times = []
ansLen = 1500

check = np.zeros(ansLen)
answer = []
snippet_lens = []
longs = []
shorts = []
for i in range(ansLen):
    answer.append([])
    snippet_lens.append([])

for cols in reader1:
    if cols[0] == 'AssignmentStatus':
        for hid, header in enumerate(cols):
            if header == 'AssignmentStatus':
                statusid = hid
            if header == 'Answer.better':
                ansid = hid
            if header == 'Input.case':
                caseid = hid
            if header == 'WorkTimeInSeconds':
                timeid = hid 
            if header == 'Input.snippet_A':
                said = hid
            if header == 'Input.snippet_B':
                sbid = hid         
    else:
        case = int(cols[caseid])
        status = cols[statusid]
        ans = cols[ansid]
        time = int(cols[timeid])
        sa = cols[said].replace('</p><p>',' ').replace('<p>','').replace('</p>','')
        sb = cols[sbid].replace('</p><p>',' ').replace('<p>','').replace('</p>','')
        
        if status == 'Approved':
            check[case] += 1
            answer[case].append(ans)
            times.append(time)
            
            lena = len(nltk.word_tokenize(sa))
            lenb = len(nltk.word_tokenize(sb))
            
            if lena>lenb:
                longs.append(lena)
                shorts.append(lenb)
            elif lenb>lena:
                longs.append(lenb)
                shorts.append(lena)
            snippet_lens[case] = [lena,lenb]
            
for cols in reader2:
    if cols[0] == 'AssignmentStatus':
        for hid, header in enumerate(cols):
            if header == 'AssignmentStatus':
                stausid = hid
            if header == 'Answer.better':
                ansid = hid
            if header == 'Input.case':
                caseid = hid
            if header == 'WorkTimeInSeconds':
                timeid = hid 
            if header == 'Input.snippet_A':
                said = hid
            if header == 'Input.snippet_B':
                sbid = hid    
    else:
        case = int(cols[caseid])
        status = cols[statusid]
        ans = cols[ansid]
        time = int(cols[timeid])
        sa = cols[said].replace('</p><p>',' ').replace('<p>','').replace('</p>','')
        sb = cols[sbid].replace('</p><p>',' ').replace('<p>','').replace('</p>','')
        
        if status == 'Approved':
            check[case] += 1
            answer[case].append(ans)
            times.append(time)
            
            lena = len(nltk.word_tokenize(sa))
            lenb = len(nltk.word_tokenize(sb))
            if lena>lenb:
                longs.append(lena)
                shorts.append(lenb)
            elif lenb>lena:
                longs.append(lenb)
                shorts.append(lena)
            snippet_lens[case] = [lena,lenb]

for cols in reader3:
    if cols[0] == 'AssignmentStatus':
        for hid, header in enumerate(cols):
            if header == 'AssignmentStatus':
                stausid = hid
            if header == 'Answer.better':
                ansid = hid
            if header == 'Input.case':
                caseid = hid
            if header == 'WorkTimeInSeconds':
                timeid = hid 
            if header == 'Input.snippet_A':
                said = hid
            if header == 'Input.snippet_B':
                sbid = hid     
 
    else:
        case = int(cols[caseid])+600
        status = cols[statusid]
        ans = cols[ansid]
        time = int(cols[timeid])
        sa = cols[said].replace('</p><p>',' ').replace('<p>','').replace('</p>','')
        sb = cols[sbid].replace('</p><p>',' ').replace('<p>','').replace('</p>','')
        
        if status == 'Approved':
            check[case] += 1
            answer[case].append(ans)
            times.append(time)
            
            lena = len(nltk.word_tokenize(sa))
            lenb = len(nltk.word_tokenize(sb))
            if lena>lenb:
                longs.append(lena)
                shorts.append(lenb)
            elif lenb>lena:
                longs.append(lenb)
                shorts.append(lena)
            snippet_lens[case] = [lena,lenb]

better_and_wiki1 = 0
better_and_wiki2 = 0

for i in range(ansLen):
    if check[i] == 5:   # has 5 annotators
        this_answer = answer[i]
        sub_par = 0
        sub_ori = 0
        
        for a in this_answer:
            if a == '1':    # first is better
                if ansDic[i] == 0: # first is original
                    sub_ori += 1
                    labeltypes[0] += 1
                else:
                    sub_par += 1
                    labeltypes[1] += 1
            elif a == '2':
                if ansDic[i] == 0: # first is original
                    sub_par += 1
                    labeltypes[1] += 1
                else:
                    sub_ori += 1
                    labeltypes[0] += 1
            elif a == 'g':
                sub_par += 1
                sub_ori += 1
                labeltypes[2] += 1
            else:
                labeltypes[3] += 1
        if i % 2 == 0:
            ori1.append(sub_ori)
            par1.append(sub_par)
            
            
            if sub_ori > sub_par:
                br1.append(sub_ori)
                wp1.append(sub_par)
            elif sub_ori < sub_par:
                bp1.append(sub_par)
                wr1.append(sub_ori)
            
            if snippet_lens[i][0]>snippet_lens[i][1] and ansDic[i] == 0: # ori is longer
                lr1.append(sub_ori)
                sp1.append(sub_par)
            elif snippet_lens[i][0]>snippet_lens[i][1] and ansDic[i] == 1: # par is longer
                lp1.append(sub_par)
                sr1.append(sub_ori)
            elif snippet_lens[i][0]<snippet_lens[i][1] and ansDic[i] == 0: # par is longer
                lp1.append(sub_par)
                sr1.append(sub_ori)
            elif snippet_lens[i][0]<snippet_lens[i][1] and ansDic[i] == 1: # ori is longer
                lr1.append(sub_ori)
                sp1.append(sub_par)
            
        else:
            ori2.append(sub_ori)
            par2.append(sub_par)
            
            if sub_ori > sub_par:
                br2.append(sub_ori)
                wp2.append(sub_par)
            elif sub_ori < sub_par:
                bp2.append(sub_par)
                wr2.append(sub_ori)
            
            
            if snippet_lens[i][0]>snippet_lens[i][1] and ansDic[i] == 0: # ori is longer
                lr2.append(sub_ori)
                sp2.append(sub_par)
            elif snippet_lens[i][0]>snippet_lens[i][1] and ansDic[i] == 1: # par is longer
                lp2.append(sub_par)
                sr2.append(sub_ori)
            elif snippet_lens[i][0]<snippet_lens[i][1] and ansDic[i] == 0: # par is longer
                lp2.append(sub_par)
                sr2.append(sub_ori)
            elif snippet_lens[i][0]<snippet_lens[i][1] and ansDic[i] == 1: # ori is longer
                lr2.append(sub_ori)
                sp2.append(sub_par)
                

# better worse
print "sig test for better-reuse vs worse-paraphrase"
print np.mean(np.concatenate((br1,wp1)))
print np.mean(np.concatenate((bp1,wr1)))
print "sig1:", stats.ttest_ind(np.concatenate((br1,wp1)),np.concatenate((bp1,wr1)))

print np.mean(np.concatenate((br2,wp2)))
print np.mean(np.concatenate((bp2,wr2)))
print "sig2:", stats.ttest_ind(np.concatenate((br2,wp2)),np.concatenate((bp2,wr2)))


# long short
print "sig test for long-reuse vs short-paraphrase"
print np.mean(np.concatenate((lr1,sp1)))
print np.mean(np.concatenate((lp1,sr1)))
print "sig1:", stats.ttest_ind(np.concatenate((lr1,sp1)),np.concatenate((lp1,sr1)))

print np.mean(np.concatenate((lr2,sp2)))
print np.mean(np.concatenate((lp2,sr2)))
print "sig2:", stats.ttest_ind(np.concatenate((lr2,sp2)),np.concatenate((lp2,sr2)))


