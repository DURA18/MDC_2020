#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 18:01:06 2020

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


inputkeys = pd.DataFrame(index = slice_trans["transaction_id"].unique(), columns = ['keys'])
for i in range(len(unique_trans)):
    if i%1000 == 0:
        print(dt.datetime.now())
        print("at transaction: " + str(i))
    inputkeys.iloc[i]['keys'] = slice_trans["inputs.input_pubkey_base58"][slice_trans["transaction_id"][:]==unique_trans[i]].values

users_feb_jun_15 = np.array([[],[]])

for i in range(len(unique_trans)):
    if i%1000 == 0:
        print(dt.datetime.now())
        print("at transaction: " + str(i))
    if i%10000 == 0:
        np.savetxt("np_user_keys_feb_jun_15_untill_sorted_transaction" + str(i) + ".csv", users_feb_jun_15, delimiter=",", fmt='%s')
    
    user_keys = np.unique(inputkeys.iloc[i][0])
    existing_keys = np.intersect1d(user_keys,users_feb_jun_15)
    if len(user_keys) == 1 and len(existing_keys) == 1:
        continue
    for key in existing_keys:
        #print("here")
        if key in users_feb_jun_15:
            old_user_i = np.argwhere(users_feb_jun_15 == key)[0,0]
            user_keys = np.union1d(user_keys,users_feb_jun_15[old_user_i,:])
            user_keys = user_keys[user_keys != '']
            users_feb_jun_15 = np.delete(users_feb_jun_15, old_user_i, axis = 0)
    #print(user_keys)
    n_users = users_feb_jun_15.shape[0]
    max_n_keys = users_feb_jun_15.shape[1]
    n_user_keys = len(user_keys)
    new_max_n_keys = max(max_n_keys, n_user_keys)
    
    new_users = np.zeros((n_users+1,new_max_n_keys), dtype="object")
    new_users[:,:] = ''
    new_users[:n_users,:max_n_keys] = users_feb_jun_15
    new_users[-1,:n_user_keys] = user_keys
    
    users_feb_jun_15 = new_users
    #print(users_feb_jun_15.dtype)


np.savetxt("np_user_keys_feb_jun_15.csv", users_feb_jun_15, delimiter=",", fmt='%s')