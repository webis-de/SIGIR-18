#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs, csv, sys, random, pickle
import numpy as np
from scipy import stats
import xml.etree.cElementTree as ET
from Crypto.Cipher import DES
from os.path import isfile
from sklearn.metrics import precision_recall_fscore_support
from collections import Counter
from scipy.stats import ttest_rel

snippet_dir = '../data/'
pickeDir = '../data/'

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

with open(pickeDir+'ans.pickle','r') as f:
    [ans,pool] = pickle.load(f)


part1File = snippet_dir+'para_part1.csv'
reader1 = unicode_csv_reader(open(part1File))

part2File = snippet_dir+'para_part2.csv'
reader2 = unicode_csv_reader(open(part2File))

oriDic = {}
for cols in reader1:
    if cols[0] == 'AssignmentStatus':
        for hid, header in enumerate(cols):
            print hid,header
            if header == 'AssignmentStatus':
                statusid = hid
            if header == 'Answer.answer':
                ansid = hid
            if header == 'Input.document':
                oriid = hid
            if header == 'Input.case':
                caseid = hid
            if header == 'WorkTimeInSeconds':
                timeid = hid 
    else:
        case = int(cols[caseid])
        status = cols[statusid]
        par = '<p>'+cols[ansid].replace('\r','').replace('\n','</p><p>')+'</p>'
        ori = cols[oriid]
        
        if status == 'Approved':
            oriDic[ori] = len(oriDic)

for cols in reader2:
    if cols[0] == 'AssignmentStatus':
        for hid, header in enumerate(cols):
            if header == 'AssignmentStatus':
                statusid = hid
            if header == 'Answer.answer':
                ansid = hid
            if header == 'Input.document':
                oriid = hid
            if header == 'Input.case':
                caseid = hid
            if header == 'WorkTimeInSeconds':
                timeid = hid 
    else:
        case = int(cols[caseid])
        case -= 6
        if case < 48:
            continue        
        status = cols[statusid]
        par = '<p>'+cols[ansid].replace('\r','').replace('\n','</p><p>')+'</p>'
        ori = cols[oriid]
        
        if status == 'Approved':
            oriDic[ori] = len(oriDic)


ansDic = {}

amtFile = snippet_dir+'rel_sel_AMT_part1.csv'
reader1 = unicode_csv_reader(open(amtFile))

for cols in reader1:
    if cols[0] == 'case':
        for hid, header in enumerate(cols):
            if header == 'case':
                caseid = hid
            if header == 'check':
                checkid = hid
            if header == 'query1':
                q1id = hid
            if header == 'title1-1':
                t11id = hid
            if header == 'link1-1':
                l11id = hid
            if header == 'snippet1-1':
                s11id = hid
            if header == 'title1-2':
                t12id = hid
            if header == 'link1-2':
                l12id = hid
            if header == 'snippet1-2':
                s12id = hid
            if header == 'title1-3':
                t13id = hid
            if header == 'link1-3':
                l13id = hid
            if header == 'snippet1-3':
                s13id = hid
            if header == 'query2':
                q2id = hid
            if header == 'title2-1':
                t21id = hid
            if header == 'link2-1':
                l21id = hid
            if header == 'snippet2-1':
                s21id = hid
            if header == 'title2-2':
                t22id = hid
            if header == 'link2-2':
                l22id = hid
            if header == 'snippet2-2':
                s22id = hid
            if header == 'title2-3':
                t23id = hid
            if header == 'link2-3':
                l23id = hid
            if header == 'snippet2-3':
                s23id = hid
            if header == 'query3':
                q3id = hid
            if header == 'title3-1':
                t31id = hid
            if header == 'link3-1':
                l31id = hid
            if header == 'snippet3-1':
                s31id = hid
            if header == 'title3-2':
                t32id = hid
            if header == 'link3-2':
                l32id = hid
            if header == 'snippet3-2':
                s32id = hid
            if header == 'title3-3':
                t33id = hid
            if header == 'link3-3':
                l33id = hid
            if header == 'snippet3-3':
                s33id = hid
            if header == 'query4':
                q4id = hid
            if header == 'title4-1':
                t41id = hid
            if header == 'link4-1':
                l41id = hid
            if header == 'snippet4-1':
                s41id = hid
            if header == 'title4-2':
                t42id = hid
            if header == 'link4-2':
                l42id = hid
            if header == 'snippet4-2':
                s42id = hid
            if header == 'title4-3':
                t43id = hid
            if header == 'link4-3':
                l43id = hid
            if header == 'snippet4-3':
                s43id = hid
            if header == 'query5':
                q5id = hid
            if header == 'title5-1':
                t51id = hid
            if header == 'link5-1':
                l51id = hid
            if header == 'snippet5-1':
                s51id = hid
            if header == 'title5-2':
                t52id = hid
            if header == 'link5-2':
                l52id = hid
            if header == 'snippet5-2':
                s52id = hid
            if header == 'title5-3':
                t53id = hid
            if header == 'link5-3':
                l53id = hid
            if header == 'snippet5-3':
                s53id = hid
    else:
        case = int(cols[caseid])
        check= cols[checkid]
        q1 = cols[q1id]
        t11 = cols[t11id]
        l11 = cols[l11id]
        s11 = cols[s11id]
        t12 = cols[t12id]
        l12 = cols[l12id]
        s12 = cols[s12id]
        t13 = cols[t13id]
        l13 = cols[l13id]
        s13 = cols[s13id]
        q2 = cols[q2id]
        t21 = cols[t21id]
        l21 = cols[l21id]
        s21 = cols[s21id]
        t22 = cols[t22id]
        l22 = cols[l22id]
        s22 = cols[s22id]
        t23 = cols[t23id]
        l23 = cols[l23id]
        s23 = cols[s23id]
        q3 = cols[q3id]
        t31 = cols[t31id]
        l31 = cols[l31id]
        s31 = cols[s31id]
        t32 = cols[t32id]
        l32 = cols[l32id]
        s32 = cols[s32id]
        t33 = cols[t33id]
        l33 = cols[l33id]
        s33 = cols[s33id]
        q4 = cols[q4id]
        t41 = cols[t41id]
        l41 = cols[l41id]
        s41 = cols[s41id]
        t42 = cols[t42id]
        l42 = cols[l42id]
        s42 = cols[s42id]
        t43 = cols[t43id]
        l43 = cols[l43id]
        s43 = cols[s43id]
        q5 = cols[q5id]
        t51 = cols[t51id]
        l51 = cols[l51id]
        s51 = cols[s51id]
        t52 = cols[t52id]
        l52 = cols[l52id]
        s52 = cols[s52id]
        t53 = cols[t53id]
        l53 = cols[l53id]
        s53 = cols[s53id]
        
        order = ['','','','','']
        
        # find check
        checkPage = int(check[0])
        order[checkPage-1] = 'check'
        
        # find s only
        if l11 == '' and t11 == '' and l12 == '' and t12 == '' and l13 == '' and t13 == '':
            sonlyPage = 0
        elif l21 == '' and t21 == '' and l22 == '' and t22 == '' and l23 == '' and t23 == '':
            sonlyPage = 1
        elif l31 == '' and t31 == '' and l32 == '' and t32 == '' and l33 == '' and t33 == '':
            sonlyPage = 2
        elif l41 == '' and t41 == '' and l42 == '' and t42 == '' and l43 == '' and t43 == '':
            sonlyPage = 3
        elif l51 == '' and t51 == '' and l52 == '' and t52 == '' and l53 == '' and t53 == '':
            sonlyPage = 4
        else:
            sys.exit('error: cannot find s only')
        order[sonlyPage] = 'sonly' 
        
        # find no s
        if s11 == '' and s12 == '' and s13 == '':
            nosPage = 0
        elif s21 == '' and s22 == '' and s23 == '':
            nosPage = 1
        elif s31 == '' and s32 == '' and s33 == '':
            nosPage = 2
        elif s41 == '' and s42 == '' and s43 == '':
            nosPage = 3
        elif s51 == '' and s52 == '' and s53 == '':
            nosPage = 4
        else:
            sys.exit('error: cannot find no s')
        order[nosPage] = 'nos'

        # find ori
        if s11 in oriDic and s12 in oriDic and s13 in oriDic:
            oriPage = 0
        elif s21 in oriDic and s22 in oriDic and s23 in oriDic:
            oriPage = 1
        elif s31 in oriDic and s32 in oriDic and s33 in oriDic:
            oriPage = 2
        elif s41 in oriDic and s42 in oriDic and s43 in oriDic:
            oriPage = 3
        elif s51 in oriDic and s52 in oriDic and s53 in oriDic:
            oriPage = 4
        else:
            sys.exit('error: cannot find ori')
        order[oriPage] = 'ori'
        
        order[order.index('')] = 'par'
        
        assert order[0] != ''
        assert order[1] != ''
        assert order[2] != ''
        assert order[3] != ''
        assert order[4] != ''
        
        ansDic[case] = (order,[q1,q2,q3,q4,q5])

resDic = {}
times = []
part1File = snippet_dir+'rel_sel_batch_part1.csv'
reader1 = unicode_csv_reader(open(part1File))

for cols in reader1:
    if cols[0] == 'AssignmentStatus':
        for hid, header in enumerate(cols):
            print hid,header
            if header == 'AssignmentStatus':
                statusid = hid
            if header == 'Input.case':
                caseid = hid
            if header == 'Answer.result1-1':
                r11id = hid
            if header == 'Answer.result1-2':
                r12id = hid
            if header == 'Answer.result1-3':
                r13id = hid
            if header == 'Answer.result2-1':
                r21id = hid
            if header == 'Answer.result2-2':
                r22id = hid
            if header == 'Answer.result2-3':
                r23id = hid
            if header == 'Answer.result3-1':
                r31id = hid
            if header == 'Answer.result3-2':
                r32id = hid
            if header == 'Answer.result3-3':
                r33id = hid
            if header == 'Answer.result4-1':
                r41id = hid
            if header == 'Answer.result4-2':
                r42id = hid
            if header == 'Answer.result4-3':
                r43id = hid
            if header == 'Answer.result5-1':
                r51id = hid
            if header == 'Answer.result5-2':
                r52id = hid
            if header == 'Answer.result5-3':
                r53id = hid
            if header == 'WorkTimeInSeconds':
                timeid = hid 
    else:
        case = int(cols[caseid])
        status = cols[statusid]
        
        if status == 'Approved':
            r11 = cols[r11id]
            r12 = cols[r12id]
            r13 = cols[r13id]
            r21 = cols[r21id]
            r22 = cols[r22id]
            r23 = cols[r23id]
            r31 = cols[r31id]
            r32 = cols[r32id]
            r33 = cols[r33id]
            r41 = cols[r41id]
            r42 = cols[r42id]
            r43 = cols[r43id]
            r51 = cols[r51id]
            r52 = cols[r52id]
            r53 = cols[r53id]
            
            res = ((r11,r12,r13),(r21,r22,r23),(r31,r32,r33),(r41,r42,r43),(r51,r52,r53))
                     
            if case in resDic:
                resDic[case].append(res)
            else:
                resDic[case] = [res]
            time = int(cols[timeid])
            times.append(time)

part2File = snippet_dir+'rel_sel_batch_part2.csv'
reader2 = unicode_csv_reader(open(part2File))

for cols in reader2:
    if cols[0] == 'AssignmentStatus':
        for hid, header in enumerate(cols):
            if header == 'AssignmentStatus':
                statusid = hid
            if header == 'Input.case':
                caseid = hid
            if header == 'Answer.result1-1':
                r11id = hid
            if header == 'Answer.result1-2':
                r12id = hid
            if header == 'Answer.result1-3':
                r13id = hid
            if header == 'Answer.result2-1':
                r21id = hid
            if header == 'Answer.result2-2':
                r22id = hid
            if header == 'Answer.result2-3':
                r23id = hid
            if header == 'Answer.result3-1':
                r31id = hid
            if header == 'Answer.result3-2':
                r32id = hid
            if header == 'Answer.result3-3':
                r33id = hid
            if header == 'Answer.result4-1':
                r41id = hid
            if header == 'Answer.result4-2':
                r42id = hid
            if header == 'Answer.result4-3':
                r43id = hid
            if header == 'Answer.result5-1':
                r51id = hid
            if header == 'Answer.result5-2':
                r52id = hid
            if header == 'Answer.result5-3':
                r53id = hid
            if header == 'WorkTimeInSeconds':
                timeid = hid 
    else:
        case = int(cols[caseid])
        status = cols[statusid]
        
        if status == 'Approved':
            r11 = cols[r11id]
            r12 = cols[r12id]
            r13 = cols[r13id]
            r21 = cols[r21id]
            r22 = cols[r22id]
            r23 = cols[r23id]
            r21 = cols[r31id]
            r32 = cols[r32id]
            r33 = cols[r33id]
            r41 = cols[r41id]
            r42 = cols[r42id]
            r43 = cols[r43id]
            r51 = cols[r51id]
            r52 = cols[r52id]
            r53 = cols[r53id]
            
            res = ((r11,r12,r13),(r21,r22,r23),(r31,r32,r33),(r41,r42,r43),(r51,r52,r53))
            
            if case in resDic:
                resDic[case].append(res)
            else:
                resDic[case] = [res]
            
            time = int(cols[timeid])
            times.append(time)

                
part3File = snippet_dir+'rel_sel_batch_part3.csv'
reader3 = unicode_csv_reader(open(part3File))

for cols in reader3:
    if cols[0] == 'AssignmentStatus':
        for hid, header in enumerate(cols):
            if header == 'AssignmentStatus':
                statusid = hid
            if header == 'Input.case':
                caseid = hid
            if header == 'Answer.result1-1':
                r11id = hid
            if header == 'Answer.result1-2':
                r12id = hid
            if header == 'Answer.result1-3':
                r13id = hid
            if header == 'Answer.result2-1':
                r21id = hid
            if header == 'Answer.result2-2':
                r22id = hid
            if header == 'Answer.result2-3':
                r23id = hid
            if header == 'Answer.result3-1':
                r31id = hid
            if header == 'Answer.result3-2':
                r32id = hid
            if header == 'Answer.result3-3':
                r33id = hid
            if header == 'Answer.result4-1':
                r41id = hid
            if header == 'Answer.result4-2':
                r42id = hid
            if header == 'Answer.result4-3':
                r43id = hid
            if header == 'Answer.result5-1':
                r51id = hid
            if header == 'Answer.result5-2':
                r52id = hid
            if header == 'Answer.result5-3':
                r53id = hid
            if header == 'WorkTimeInSeconds':
                timeid = hid 
    else:
        case = int(cols[caseid])
        status = cols[statusid]
        
        if status == 'Approved':
            r11 = cols[r11id]
            r12 = cols[r12id]
            r13 = cols[r13id]
            r21 = cols[r21id]
            r22 = cols[r22id]
            r23 = cols[r23id]
            r21 = cols[r31id]
            r32 = cols[r32id]
            r33 = cols[r33id]
            r41 = cols[r41id]
            r42 = cols[r42id]
            r43 = cols[r43id]
            r51 = cols[r51id]
            r52 = cols[r52id]
            r53 = cols[r53id]
            
            res = ((r11,r12,r13),(r21,r22,r23),(r31,r32,r33),(r41,r42,r43),(r51,r52,r53))
            
            if case in resDic:
                resDic[case].append(res)
            else:
                resDic[case] = [res]

            time = int(cols[timeid])
            times.append(time)

print 'times:',np.mean(times)/15

golds_ori = []
golds_par = []
golds_sonly = []
golds_nos = []

pred_ori = []
pred_par = []
pred_sonly = []
pred_nos = []

with open(snippet_dir + 'rel_label.txt','w') as flabel:
    for iCase,pageAns in enumerate(ans):
        pageOrder = ansDic[iCase][0]
        ori_idx = pageOrder.index('ori')
        par_idx = pageOrder.index('par')
        sonly_idx = pageOrder.index('sonly')
        nos_idx = pageOrder.index('nos')
        
        ori_g = pageAns[ori_idx]
        par_g = pageAns[par_idx]
        sonly_g = pageAns[sonly_idx]
        nos_g = pageAns[nos_idx]
        
        res = resDic[iCase]
        majorR = []
        for i in range(5):        # 5 pages
            subR = []
            for j in range(3):    # 3 results
                r = [res[0][i][j],res[1][i][j],res[2][i][j]]
                r_count = dict(Counter(r))
                if 'Relevant' in r_count:
                    if r_count['Relevant'] > 1:  # 2 or 3
                        subR.append(1)
                    else:
                        subR.append(0)
                else:
                    subR.append(0)
                
                if i != check_idx:
                    flabel.write('\t'.join(r) + '\n')
                
            majorR.append(subR)
            
        ori_r = majorR[ori_idx]
        par_r = majorR[par_idx]
        sonly_r = majorR[sonly_idx]
        nos_r = majorR[nos_idx]
                   
        golds_ori.extend(ori_g)
        golds_par.extend(par_g)
        golds_sonly.extend(sonly_g)
        golds_nos.extend(nos_g)
        
        pred_ori.extend(ori_r)
        pred_par.extend(par_r)
        pred_sonly.extend(sonly_r)
        pred_nos.extend(nos_r)

print 'ori:',precision_recall_fscore_support(golds_ori,pred_ori,labels=[1,0])
print 'par:',precision_recall_fscore_support(golds_par,pred_par,labels=[1,0])
print 'sonly:',precision_recall_fscore_support(golds_sonly,pred_sonly,labels=[1,0])
print 'nos:',precision_recall_fscore_support(golds_nos,pred_nos,labels=[1,0])

o_acc = []
oi_acc = []
for idx,ori in enumerate(pred_ori):
    if golds_ori[idx] != ori:
        o_acc.append(0)
        oi_acc.append(1)
    else:
        o_acc.append(1)
        oi_acc.append(0)

p_acc = []
pi_acc = []
for idx,par in enumerate(pred_par):
    if golds_par[idx] != par:
        p_acc.append(0)
        pi_acc.append(1)
    else:
        p_acc.append(1)
        pi_acc.append(0)
        
s_acc = []
si_acc = []
for idx,sonly in enumerate(pred_sonly):
    if golds_sonly[idx] != sonly:
        s_acc.append(0)
        si_acc.append(1)
    else:
        s_acc.append(1)
        si_acc.append(0)
        
n_acc = []
ni_acc = []
for idx,nos in enumerate(pred_nos):
    if golds_nos[idx] != nos:
        n_acc.append(0)
        ni_acc.append(1)
    else:
        n_acc.append(1)
        ni_acc.append(0)


# print o_acc
# print p_acc
# print s_acc
# print n_acc

# print np.mean(o_acc)
# print np.mean(p_acc)
# print np.mean(s_acc)
# print np.mean(n_acc)

# print 'ori vs par:',ttest_rel(o_acc,p_acc)
# print 'ori vs sonly:',ttest_rel(o_acc,s_acc)
# print 'ori vs nos:',ttest_rel(o_acc,n_acc)
# print 'par vs sonly:',ttest_rel(p_acc,s_acc)
# print 'par vs nos',ttest_rel(p_acc,n_acc)
# print 'sonly vs nos',ttest_rel(s_acc,n_acc)
# 
# 
# print 'ori vs par:',ttest_rel(oi_acc,pi_acc)
# print 'ori vs sonly:',ttest_rel(oi_acc,si_acc)
# print 'ori vs nos:',ttest_rel(oi_acc,ni_acc)
# print 'par vs sonly:',ttest_rel(pi_acc,si_acc)
# print 'par vs nos',ttest_rel(pi_acc,ni_acc)
# print 'sonly vs nos',ttest_rel(si_acc,ni_acc)
