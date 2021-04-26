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

if _platform == "win32":
    sys.path.insert(1, '..\..\prediction\lstm\\')
else:
    sys.path.insert(1, '../../prediction/lstm//')    

# from LSTMpredict import LSTMpredict
from LSTMpredict_copy import LSTMpredict

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

df_test = pd.read_csv(fileutils.get_latest_file_with_path(test_data_path, 'lipdverse_test_*.csv'))
# df_test = pd.read_csv('D:\\annotating_paleoclimate_data\\paleorec\\data\\csv\\lipdverse_test_1234.csv')
df_test = df_test.replace(np.nan, 'NA', regex=True)
df_test = df_test.replace(',', '', regex=True)
df_test_list = df_test.values.tolist()
len_dict = predict_obj.len_dict

inverse_ref_dict = {v:k for k,v in predict_obj.reference_dict.items()}

ground_truth_label_file = fileutils.get_latest_file_with_path(ground_truth_label_path, 'ground_truth_label_*.json')
with open(ground_truth_label_file, 'r') as json_file:
    ground_truth = json.load(json_file)
    
ground_truth_label_dict = ground_truth['ground_truth']
accuracy_list = []
precision_list = []
recall_list = []
good_list = []
total_acc, total_pres, total_rec = 0,0,0

avg_mrr = {"1": [], "2": [], "3": [], "3_units": [], "4": [], "5": [], "6": []}
avg_rec = {"1": [], "2": [], "3": [], "3_units": [], "4": [], "5": [], "6": []}
avg_dcg = {"1": [], "2": [], "3": [], "3_units": [], "4": [], "5": [], "6": []}

# Yi = ground truth set for input
# hxi = predicted set for the input
# xi = input label for which next word is predicted
# resi = ground truth value from chain

def get_mrr_score(resi,hxi):
    
    if hxi[0] == 'NA' or hxi[0] == 'NotApplicable':
            hxi = hxi[:1]

    if resi == hxi[0]:
        return 1
    elif resi in hxi:
        return 1/hxi.index(resi)
    else:
        return 0

def get_dcg_score(resi, hxi):

    if hxi[0] == 'NA' or hxi[0] == 'NotApplicable':
            hxi = hxi[:1]

    
    if resi in hxi:
        val = 1 if resi == hxi[0] else hxi.index(resi)
        return 1/math.log((val + 1),2)
    else:
        return 0

def get_recall_score(resi, hxi):

    if hxi[0] == 'NA' or hxi[0] == 'NotApplicable':
            hxi = hxi[:1]
    
    if resi in hxi:
        return 1
    else:
        return 0

def calculate_score_for_test_data_chain():

    global accuracy_list, precision_list, recall_list, df_test_list
    global total_acc, total_pres, total_rec

    df = pd.DataFrame(np.nan, index = [0,1,2,3],columns=['archiveType', 'proxyObsType', 'units', 'interpretation/variable', 'interpretation/variableDetail', 'inferredVariable', 'inferredVarUnits', 'accuracy_score', 'precision_score', 'recall_score'])
    
    c = 0
    chain_count = 1
    for lis in df_test_list:
        lis = [val.replace(" ", "") for val in lis]
        i = 1
        
        while i < 7:
            
            ref_word = inverse_ref_dict[lis[i-1]] if lis[i-1] in inverse_ref_dict else ''
            if c < 12:
                print('ref word {} for lis item {}'.format(ref_word, lis[i-1]))
            actual_len = len(ground_truth_label_dict[ref_word]) if ref_word in ground_truth_label_dict else -1

            if i < 2:
                input_sent_list = lis[:i]
                results = predict_obj.predictForSentence(sentence=','.join(input_sent_list))['0']
                received_len = len(results)
                if not results:
                    results = ['NA']


                avg_mrr['2'].append(get_mrr_score(lis[i], results))
                avg_rec['2'].append(get_recall_score(lis[i], results))
                avg_dcg['2'].append(get_dcg_score(lis[i], results))

                values_to_add = {'archiveType': lis[i-1], 'proxyObsType': lis[i], 'Recall' : avg_rec['2'][-1], 'MRR' : avg_mrr['2'][-1], 'NDCG' : avg_dcg['2'][-1]}
                row_to_add = pd.Series(values_to_add, name = chain_count)
                df = df.append(row_to_add)
                chain_count += 1

            elif i == 2:
                input_sent_list = lis[:i]
                results_units =  predict_obj.predictForSentence(sentence=','.join(input_sent_list))['0']
                results = predict_obj.predictForSentence(sentence=','.join(input_sent_list))['1']
                
                received_len = len(results)

                if not results_units:
                    results_units = ['NA']
                if not results:
                    results = ['NA']

                avg_mrr['3_units'].append(get_mrr_score(lis[i], results_units))
                avg_rec['3_units'].append(get_recall_score(lis[i], results_units))
                avg_dcg['3_units'].append(get_dcg_score(lis[i], results_units))


                values_to_add = {'archiveType': lis[i-2], 'proxyObsType': lis[i-1], 'units': lis[i], 'Recall' : avg_rec['3_units'][-1], 'MRR' : avg_mrr['3_units'][-1], 'NDCG' : avg_dcg['3_units'][-1]}
                row_to_add = pd.Series(values_to_add, name = chain_count)
                df = df.append(row_to_add)
                chain_count += 1

                avg_mrr['3'].append(get_mrr_score(lis[i+1], results))
                avg_rec['3'].append(get_recall_score(lis[i+1], results))
                avg_dcg['3'].append(get_dcg_score(lis[i+1], results))

                values_to_add = {'archiveType': lis[i-2], 'proxyObsType': lis[i-1],'interpretation/variable' : lis[i+1], 'Recall' : avg_rec['2'][-1], 'MRR' : avg_mrr['2'][-1], 'NDCG' : avg_dcg['2'][-1]}
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

                avg_mrr[str(i)].append(get_mrr_score(lis[i], results))
                avg_rec[str(i)].append(get_recall_score(lis[i], results))
                avg_dcg[str(i)].append(get_dcg_score(lis[i], results))

                values_to_add = {'archiveType': lis[0], 'proxyObsType': lis[1], 'interpretation/variable': lis[3], 'Recall' : avg_rec[str(i)][-1], 'MRR' : avg_mrr[str(i)][-1], 'NDCG' : avg_dcg[str(i)][-1]}
                if i == 4:
                    values_to_add['interpretation/variableDetail'] = lis[i]
                elif i == 5:
                    values_to_add['interpretation/variableDetail'] = lis[4]
                    values_to_add['inferredVariable'] = lis[i]
                elif i == 6:
                    values_to_add['interpretation/variableDetail'] = lis[4]
                    values_to_add['inferredVariable'] = lis[5]
                    values_to_add['inferredVarUnits'] = lis[i]

                row_to_add = pd.Series(values_to_add, name = chain_count)
                df = df.append(row_to_add)
                chain_count += 1

            i += 1             
            c += 1
            if c < 13:
                print('actual length = {}, received length = {}'.format(actual_len, received_len))        

    print('**************************************************************************************')
    for val in ['2', '3', '3_units', '4', '5', '6']:

        print('Chain Length = {} Recall = {}'.format(val, sum(avg_rec[val])/len(avg_rec[val])))
        print('Chain Length = {} MRR = {}'.format(val, sum(avg_mrr[val])/len(avg_mrr[val])))
        print('Chain Length = {} NDCG = {}'.format(val, sum(avg_dcg[val])/len(avg_dcg[val])))
        print('**************************************************************************************')

    accuracy_data_path = os.path.join(test_data_path, 'accuracy_prediction_fang_metrics_1.csv')
    df = df.replace(np.nan, '', regex=True)
    df.to_csv(accuracy_data_path, sep = ',', encoding = 'utf-8',index = False)

def store_results_to_csv():
    '''
    Append the accuracy score for each row.
    Also append the information which signifies whether LSTM is a fit for predictions for this archiveType.
    Store this information back to a csv file.

    Returns
    -------
    None.

    '''
    global df_test
    
    accuracy_data_path = os.path.join(test_data_path, 'accuracy_prediction_fang_metrics.csv')
    df_test = df_test.assign(accuracy_score=pd.Series(accuracy_list).values)
    df_test = df_test.assign(precision_score=pd.Series(precision_list).values)
    df_test = df_test.assign(recall_score=pd.Series(recall_list).values)
    df_test.to_csv(accuracy_data_path, sep = ',', encoding = 'utf-8',index = False)
    
if __name__ == "__main__":
    calculate_score_for_test_data_chain()