#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 23:42:30 2020

@author: isabel
"""

import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime

transaction_dataframe2 = pd.read_csv("bitcoin_transactions_dt.csv", sep =";")
transaction_dataframe2["output_bitcoin_value"] = 0
transaction_dataframe2["outputs.output_satoshis"] = pd.to_numeric(transaction_dataframe2["outputs.output_satoshis"], errors='coerce')
transaction_dataframe2["output_bitcoin_value"] = 0.00000001 * transaction_dataframe2["outputs.output_satoshis"]
transaction_dataframe2["timestamp"] = pd.to_datetime(transaction_dataframe2["timestamp"], format = '%d %b %Y')

#drop rows with incomplete transaction data
transaction_dataframe_without_null2 = transaction_dataframe2.dropna()
transaction_dataframe_without_null2 = transaction_dataframe_without_null2.reset_index(drop = True)

number_of_compelte_transactions = len(transaction_dataframe_without_null2)

df_transactioncounts_inputkeys = transaction_dataframe_without_null2["inputs.input_pubkey_base58"].value_counts()
unique_addresses = transaction_dataframe_without_null2["inputs.input_pubkey_base58"].nunique()

number_of_unique_transactioIDs = len(transaction_dataframe_without_null2["transaction_id"].value_counts())

#%%
n_slice = 1000
sorted_transactions2 = transaction_dataframe_without_null2.sort_values(by ='timestamp')


date_after = dt.datetime(2015,2,1)
date_before = dt.datetime(2015,7,1)
df_half = sorted_transactions2[sorted_transactions2["timestamp"]>=date_after]
slice_trans = df_half = df_half[df_half["timestamp"]<date_before]
unique_trans = slice_trans["transaction_id"].unique()
unique_keys = slice_trans["inputs.input_pubkey_base58"].unique()

users_feb_jun_15 = np.genfromtxt("np_user_keys_feb_jun_15.csv",delimiter=',',dtype=str)

"""
inputkeys = pd.DataFrame(index = slice_trans["transaction_id"].unique(), columns = ['keys'])
for i in range(len(unique_trans)):
    if i%1000 == 0:
        print(dt.datetime.now())
        print("at transaction: " + str(i))
    inputkeys.iloc[i]['keys'] = slice_trans["inputs.input_pubkey_base58"][slice_trans["transaction_id"][:]==unique_trans[i]].values
"""

max_user = users_feb_jun_15.shape[0]

transactions = pd.DataFrame(index = slice_trans["transaction_id"].unique(), columns = ['date', 'input_keys', 'output_keys', 'input_users', 'output_users']) #inputkeys
#outputkeys = pd.DataFrame(index = slice_trans["transaction_id"].unique(), columns = ['keys'])
for i in range(len(unique_trans)):
    if i%1000 == 0:
        print("at transaction: " + str(i))
        print(dt.datetime.now())
    transactions.iloc[i]['date'] = slice_trans["timestamp"][slice_trans["transaction_id"][:]==unique_trans[i]].iloc[0]
    input_keys_non_uni = slice_trans["inputs.input_pubkey_base58"][slice_trans["transaction_id"][:]==unique_trans[i]].values
    input_keys = np.unique(input_keys_non_uni)
    output_keys_non_uni = slice_trans["outputs.output_pubkey_base58"][slice_trans["transaction_id"][:]==unique_trans[i]].values
    output_keys = np.unique(output_keys_non_uni)
    transactions.iloc[i]['input_keys'] = input_keys
    input_users = np.zeros((len(input_keys)))
    for j in range(len(input_keys)):
        input_key = input_keys[j]
        input_users[j] =  np.argwhere(users_feb_jun_15 == input_key)[0,0]
    transactions.iloc[i]['input_users'] = np.unique(input_users)
    
    transactions.iloc[i]['output_keys'] = output_keys
    output_users = np.zeros((len(output_keys)))
    for j in range(len(output_keys)):
        output_key = output_keys[j]
        if output_key in users_feb_jun_15:
            output_users[j] =  np.argwhere(users_feb_jun_15 == output_key)[0,0]
        else:
            output_users[j] = max_user
            max_user += 1
    transactions.iloc[i]['output_users'] = np.unique(output_users)
    


#%%
delta_days = (date_before - date_after).days

graph = np.zeros((max_user,max_user, delta_days))

for i in range(len(unique_trans)):
    date = transactions.iloc[i]["date"]
    day = (date - date_after).days
    for input_user in transactions.iloc[i]["input_users"]:
        for output_user in transactions.iloc[i]["output_users"]:
            graph[int(input_user),int(output_user),day] += 1


#np.savetxt("user_graph_temporal_feb_jun_15.csv", graph, delimiter=",", fmt='%s')
#np.save("user_graph_temporal_feb_jun_15.npy", graph)
