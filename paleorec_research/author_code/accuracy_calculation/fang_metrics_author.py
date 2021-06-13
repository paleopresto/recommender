# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 11:50:34 2021

@author: shrav
"""

import pandas as pd
import numpy as np
import sys
import os
import json
from sys import platform as _platform
import math

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import seaborn as sns

if _platform == "win32":
    sys.path.insert(1, '..\..\prediction\lstm\\')
else:
    sys.path.insert(1, '../../prediction/lstm//')    

from LSTMpredictAuthor_copy import LSTMpredict

if _platform == "win32":
    sys.path.insert(1, '..\..\\')
else:
    sys.path.insert(1, '../../')
from utils import fileutils

if _platform == "win32":
    predict_obj = LSTMpredict(model_file_path='..\..\data\model_lstm\\', ground_truth_file_path='..\..\data\ground_truth_info\\', topk=5)
    test_data_path = '..\..\data\csv\\'
    ground_truth_label_path = '..\..\data\ground_truth_info\\'
else:
    predict_obj = LSTMpredict(model_file_path='../../data/model_lstm/', ground_truth_file_path='../../data/ground_truth_info/', topk=5)
    test_data_path = '../../data/csv/'
    ground_truth_label_path = '../../data/ground_truth_info/'

df_test = pd.read_csv(fileutils.get_latest_file_with_path(test_data_path, 'lipdverse_test_auth_*.csv'))
# df_test = pd.read_csv('D:\\annotating_paleoclimate_data\\paleorec\\data\\csv\\lipdverse_test_1234.csv')
df_test = df_test.replace(np.nan, 'NA', regex=True)
df_test = df_test.replace(',', '', regex=True)
df_test_list = df_test.values.tolist()
len_dict = predict_obj.len_dict

inverse_ref_dict = {v:k for k,v in predict_obj.reference_dict.items()}

ground_truth_label_file = fileutils.get_latest_file_with_path(ground_truth_label_path, 'ground_truth_label_auth_*.json')
with open(ground_truth_label_file, 'r') as json_file:
    ground_truth = json.load(json_file)
    
ground_truth_label_dict = ground_truth['ground_truth']
accuracy_list = []
precision_list = []
recall_list = []
good_list = []
total_acc, total_pres, total_rec = 0,0,0

avg_rec_3 = {"3": [], "4": [], "4_units": [], "5": [], "6": [], "7": []}
avg_rec_5 = {"3": [], "4": [], "4_units": [], "5": [], "6": [], "7": []}
avg_rec_7 = {"3": [], "4": [], "4_units": [], "5": [], "6": [], "7": []}
avg_rec_10 = {"3": [], "4": [], "4_units": [], "5": [], "6": [], "7": []}
avg_rec_12 = {"3": [], "4": [], "4_units": [], "5": [], "6": [], "7": []}
avg_rec_14 = {"3": [], "4": [], "4_units": [], "5": [], "6": [], "7": []}
avg_rec_16 = {"3": [], "4": [], "4_units": [], "5": [], "6": [], "7": []}

avg_mrr_3 = {"3": [], "4": [], "4_units": [], "5": [], "6": [], "7": []}
avg_mrr_5 = {"3": [], "4": [], "4_units": [], "5": [], "6": [], "7": []}
avg_mrr_7 = {"3": [], "4": [], "4_units": [], "5": [], "6": [], "7": []}
avg_mrr_10 = {"3": [], "4": [], "4_units": [], "5": [], "6": [], "7": []}
avg_mrr_12 = {"3": [], "4": [], "4_units": [], "5": [], "6": [], "7": []}
avg_mrr_14 = {"3": [], "4": [], "4_units": [], "5": [], "6": [], "7": []}
avg_mrr_16 = {"3": [], "4": [], "4_units": [], "5": [], "6": [], "7": []}

# Yi = ground truth set for input
# hxi = predicted set for the input
# xi = input label for which next word is predicted
# resi = ground truth value from chain

def get_mrr_score(grnd_truth_i,hxi):
    
    '''
    Formula from https://arxiv.org/pdf/1808.06414.pdf 'Next Item Recommendation with Self-Attention' pg 6
    '''

    if hxi[0] == 'NA' or hxi[0] == 'NotApplicable':
            hxi = hxi[:1]

    res = []
    for lim in [3,5,7,10,12,14,16]:
        temp_hxi = hxi[:lim]
        if grnd_truth_i == temp_hxi[0]:
            res.append(1)
        elif grnd_truth_i in temp_hxi:
            res.append(1/(temp_hxi.index(grnd_truth_i)+1))
        else:
            res.append(0)
    return res

def get_recall_score(grnd_truth_i, hxi):

    '''
    Formula from https://arxiv.org/pdf/1808.06414.pdf 'Next Item Recommendation with Self-Attention' pg 5 
    '''
    if hxi[0] == 'NA' or hxi[0] == 'NotApplicable':
            hxi = hxi[:1]

    r3 = 1 if grnd_truth_i in hxi[:3] else 0
    r5 = 1 if grnd_truth_i in hxi[:5] else 0
    r7 = 1 if grnd_truth_i in hxi[:7] else 0
    r10 = 1 if grnd_truth_i in hxi[:10] else 0
    r12 = 1 if grnd_truth_i in hxi[:12] else 0
    r14 = 1 if grnd_truth_i in hxi[:14] else 0
    r16 = 1 if grnd_truth_i in hxi[:16] else 0

    return r3, r5, r7, r10, r12, r14, r16

def mean_recall(val):
    '''
    Method to calculate the average recall for all the examples in the test data for a particular chain length across all the recommendation set size.(3, 5, 7, 10 ,12, 14, 16)

    Parameters
    ----------
    val : int
        Chain length across which mean is calculated.

    Returns
    -------
    res : list
        List containing the average recall across a particular chain size for different recommendation set sizes.

    '''
    objs_list = [avg_rec_3[val], avg_rec_5[val], avg_rec_7[val], avg_rec_10[val], avg_rec_12[val], avg_rec_14[val], avg_rec_16[val] ]
    res = []
    for obj in objs_list:
        res.append(sum(obj)/len(obj))
    return res

def mean_mrr(val):
    '''
    Method to calculate the MRR for a chain sizes across different recommendation set sizes.(3, 5, 7, 10)

    Parameters
    ----------
    val : int
        Chain length across which mean is calculated

    Returns
    -------
    res : list
        list containing the average MRR across a particular chain length for different recommendation set sizes.

    '''
    
    objs_list = [avg_mrr_3[val], avg_mrr_5[val], avg_mrr_7[val], avg_mrr_10[val], avg_mrr_12[val], avg_mrr_14[val], avg_mrr_16[val]]
    res = []
    for obj in objs_list:
        res.append(sum(obj)/len(obj))
    return res

def calculate_score_for_test_data_chain():

    global accuracy_list, precision_list, recall_list, df_test_list
    global total_acc, total_pres, total_rec

    df = pd.DataFrame(np.nan, index = [0,1,2,3],columns=['authorName','archiveType', 'proxyObsType', 'units', 'interpretation/variable', 'interpretation/variableDetail', 'inferredVariable', 'inferredVarUnits', 'accuracy_score', 'precision_score', 'recall_score'])
    
    c = 0
    chain_count = 1
    for lis in df_test_list:
        lis = [val.replace(" ", "") for val in lis]
        i = 2
        
        while i < 8:
            
            ref_word = inverse_ref_dict[lis[i-1]] if lis[i-1] in inverse_ref_dict else ''
            
            actual_len = len(ground_truth_label_dict[ref_word]) if ref_word in ground_truth_label_dict else -1

            if i < 3:
                input_sent_list = lis[:i]
                results = predict_obj.predictForSentence(sentence=','.join(input_sent_list))['0']
                received_len = len(results)
                if not results:
                    results = ['NA']

                r3, r5, r7, r10, r12, r14, r16 = get_recall_score(lis[i], results)
                m3, m5, m7, m10, m12, m14, m16 = get_mrr_score(lis[i], results)

                # avg_mrr['2'].append(get_mrr_score(lis[i], results))
                avg_mrr_3['3'].append(m3)
                avg_mrr_5['3'].append(m5)
                avg_mrr_7['3'].append(m7)
                avg_mrr_10['3'].append(m10)
                avg_mrr_12['3'].append(m12)
                avg_mrr_14['3'].append(m14)
                avg_mrr_16['3'].append(m16)

                # avg_rec['2'].append(get_recall_score(lis[i], results))
                avg_rec_3['3'].append(r3)
                avg_rec_5['3'].append(r5)
                avg_rec_7['3'].append(r7)
                avg_rec_10['3'].append(r10)
                avg_rec_12['3'].append(r12)
                avg_rec_14['3'].append(r14)
                avg_rec_16['3'].append(r16)

                values_to_add = {'authorName': lis[i-2], 'archiveType': lis[i-1], 'proxyObsType': lis[i]}
                row_to_add = pd.Series(values_to_add, name = chain_count)
                df = df.append(row_to_add)
                chain_count += 1

            elif i == 3:
                input_sent_list = lis[:i]
                results_units =  predict_obj.predictForSentence(sentence=','.join(input_sent_list))['0']
                results = predict_obj.predictForSentence(sentence=','.join(input_sent_list))['1']
                
                received_len = len(results)

                if not results_units:
                    results_units = ['NA']
                if not results:
                    results = ['NA']

                r3, r5, r7, r10, r12, r14, r16 = get_recall_score(lis[i], results_units)
                m3, m5, m7, m10, m12, m14, m16 = get_mrr_score(lis[i], results_units)

                # avg_mrr['3_units'].append(get_mrr_score(lis[i], results_units))
                avg_mrr_3['4_units'].append(m3)
                avg_mrr_5['4_units'].append(m5)
                avg_mrr_7['4_units'].append(m7)
                avg_mrr_10['4_units'].append(m10)
                avg_mrr_12['4_units'].append(m12)
                avg_mrr_14['4_units'].append(m14)
                avg_mrr_16['4_units'].append(m16)

                # avg_rec['3_units'].append(get_recall_score(lis[i], results_units))
                avg_rec_3['4_units'].append(r3)
                avg_rec_5['4_units'].append(r5)
                avg_rec_7['4_units'].append(r7)
                avg_rec_10['4_units'].append(r10)
                avg_rec_12['4_units'].append(r12)
                avg_rec_14['4_units'].append(r14)
                avg_rec_16['4_units'].append(r16)


                values_to_add = {'authorName': lis[0],'archiveType': lis[1], 'proxyObsType': lis[i-1], 'units': lis[i]}
                row_to_add = pd.Series(values_to_add, name = chain_count)
                df = df.append(row_to_add)
                chain_count += 1

                r3, r5, r7, r10, r12, r14, r16 = get_recall_score(lis[i+1], results)
                m3, m5, m7, m10, m12, m14, m16 = get_mrr_score(lis[i], results)

                # avg_mrr['3'].append(get_mrr_score(lis[i+1], results))
                avg_mrr_3['4'].append(m3)
                avg_mrr_5['4'].append(m5)
                avg_mrr_7['4'].append(m7)
                avg_mrr_10['4'].append(m10)
                avg_mrr_12['4'].append(m12)
                avg_mrr_14['4'].append(m14)
                avg_mrr_16['4'].append(m16)

                # avg_rec['3'].append(get_recall_score(lis[i+1], results))
                avg_rec_3['4'].append(r3)
                avg_rec_5['4'].append(r5)
                avg_rec_7['4'].append(r7)
                avg_rec_10['4'].append(r10)
                avg_rec_12['4'].append(r12)
                avg_rec_14['4'].append(r14)
                avg_rec_16['4'].append(r16)

                values_to_add = {'authorName': lis[0], 'archiveType': lis[i-2], 'proxyObsType': lis[i-1],'interpretation/variable' : lis[i+1]}
                row_to_add = pd.Series(values_to_add, name = chain_count)
                df = df.append(row_to_add)
                chain_count += 1

                i += 1
            else:
                temp = lis[:2]
                temp.extend(lis[3:i])
                input_sent_list = temp
                results = predict_obj.predictForSentence(sentence=','.join(input_sent_list))['0']
                received_len = len(results)
                if not results:
                    results = ['NA']

                r3, r5, r7, r10, r12, r14, r16 = get_recall_score(lis[i], results)
                m3, m5, m7, m10, m12, m14, m16 = get_mrr_score(lis[i], results)

                # avg_mrr[str(i)].append(get_mrr_score(lis[i], results))
                avg_mrr_3[str(i)].append(m3)
                avg_mrr_5[str(i)].append(m5)
                avg_mrr_7[str(i)].append(m7)
                avg_mrr_10[str(i)].append(m10)
                avg_mrr_12[str(i)].append(m12)
                avg_mrr_14[str(i)].append(m14)
                avg_mrr_16[str(i)].append(m16)

                # avg_rec[str(i)].append(get_recall_score(lis[i], results))
                avg_rec_3[str(i)].append(r3)
                avg_rec_5[str(i)].append(r5)
                avg_rec_7[str(i)].append(r7)
                avg_rec_10[str(i)].append(r10)
                avg_rec_12[str(i)].append(r12)
                avg_rec_14[str(i)].append(r14)
                avg_rec_16[str(i)].append(r16)

                values_to_add = {'authorName': lis[0], 'archiveType': lis[1], 'proxyObsType': lis[2], 'interpretation/variable': lis[4]}
                if i == 5:
                    values_to_add['interpretation/variableDetail'] = lis[i]
                elif i == 6:
                    values_to_add['interpretation/variableDetail'] = lis[5]
                    values_to_add['inferredVariable'] = lis[i]
                elif i == 7:
                    values_to_add['interpretation/variableDetail'] = lis[5]
                    values_to_add['inferredVariable'] = lis[6]
                    values_to_add['inferredVarUnits'] = lis[i]

                row_to_add = pd.Series(values_to_add, name = chain_count)
                df = df.append(row_to_add)
                chain_count += 1

            i += 1             
            c += 1
            if c < 13:
                print('actual length = {}, received length = {}'.format(actual_len, received_len))        

    print('**************************************************************************************')
    
    accuracy_data_path = os.path.join(test_data_path, 'accuracy_prediction_fang_metrics_1.csv')
    df = df.replace(np.nan, '', regex=True)
    df.to_csv(accuracy_data_path, sep = ',', encoding = 'utf-8',index = False)

    # seaborn plotting data
    x = [3,5,7,10,12,14,16]
    y2 = mean_recall('3')
    y3 = mean_recall('4')
    y3_u = mean_recall('4_units')
    y4 = mean_recall('5')
    y5 = mean_recall('6')
    y6 = mean_recall('7')

    num_rows = 7
    a4_dims = (8, 6)
    fig, ax = plt.subplots(figsize=a4_dims)
    
    data_preproc = pd.DataFrame({
        'Recommendation Set Size(3,5,7,10,12,14,16)': x, 
        'Proxy Observation(chain len = 2)': y2,
        'Interpretation Var(chain len = 3)': y3,
        'Proxy Units(chain len = 3)': y3_u,
        'Interpretation Var Detail(chain len = 4)': y4,
        'Inferred Var(chain len = 5)': y5,
        'Inferred Var Units(chain len = 6)': y6})
    
    sns.lineplot(ax=ax, x='Recommendation Set Size(3,5,7,10,12,14,16)', y='value', hue='variable', style="variable",
             data=pd.melt(data_preproc, ['Recommendation Set Size(3,5,7,10,12,14,16)']), markers=True, dashes=False, markersize=10)
    sns.set_style("white")
    ax.set(ylabel='Hit Ratio')
    lgd = ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0)         
    plt.ylim(0, 1.1)
    fig.savefig('auth_hr_06_12.png', dpi=300, bbox_extra_artists=(lgd,), bbox_inches='tight')

    print('*************************************************************************************************')

    fig, ax = plt.subplots(figsize=a4_dims)
    x = [3,5,7,10,12,14,16]
    y2 = mean_mrr('3')
    y3 = mean_mrr('4')
    y3_u = mean_mrr('4_units')
    y4 = mean_mrr('5')
    y5 = mean_mrr('6')
    y6 = mean_mrr('7')
    data_preproc = pd.DataFrame({
        'Recommendation Set Size(3,5,7,10,12,14,16)': x, 
        'Proxy Observation(chain len = 2)': y2,
        'Interpretation Var(chain len = 3)': y3,
        'Proxy Units(chain len = 3)': y3_u,
        'Interpretation Var Detail(chain len = 4)': y4,
        'Inferred Var(chain len = 5)': y5,
        'Inferred Var Units(chain len = 6)': y6})

    sns.set_style("white")
    sns.lineplot(ax=ax, x='Recommendation Set Size(3,5,7,10,12,14,16)', y='value', hue='variable', style="variable", 
             data=pd.melt(data_preproc, ['Recommendation Set Size(3,5,7,10,12,14,16)']), markers=True, dashes=False, markersize = 10)
    ax.set(ylabel='MRR')
    plt.ylim(0, 1.1) 
    lgd = ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0)         
    fig.savefig('auth_mrr_06_12.png', dpi=300, bbox_extra_artists=(lgd,), bbox_inches='tight')


    
if __name__ == "__main__":
    calculate_score_for_test_data_chain()