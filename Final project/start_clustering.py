#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:52:08 2020

@author: isabel
"""
import numpy as np
import pandas as pd
from datetime import datetime

#%%from bitcoin_transaction_dataset.ipynb
transaction_dataframe = pd.read_csv("~/Documents/Studie/AP/ModDat/Bitcoin/bitcoin_transactions.csv", sep =";")
transaction_dataframe["output_bitcoin_value"] = 0
transaction_dataframe["outputs.output_satoshis"] = pd.to_numeric(transaction_dataframe["outputs.output_satoshis"], errors='coerce')
transaction_dataframe["output_bitcoin_value"] = 0.00000001 * transaction_dataframe["outputs.output_satoshis"]

#drop rows with incomplete transaction data
transaction_dataframe_without_null = transaction_dataframe.dropna()
transaction_dataframe_without_null = transaction_dataframe_without_null.reset_index(drop = True)

number_of_compelte_transactions = len(transaction_dataframe_without_null)

df_transactioncounts_inputkeys = transaction_dataframe_without_null["inputs.input_pubkey_base58"].value_counts()
unique_addresses = transaction_dataframe_without_null["inputs.input_pubkey_base58"].nunique()

number_of_unique_transactioIDs = len(transaction_dataframe_without_null["transaction_id"].value_counts())

#%%
n_slice = 1000
sorted_transactions = transaction_dataframe_without_null.sort_values(by ='timestamp')
slice_trans =sorted_transactions[n_slice:3*n_slice]
unique_trans = slice_trans["transaction_id"].unique()
unique_keys = slice_trans["inputs.input_pubkey_base58"].unique()

inputkeys = pd.DataFrame(index = slice_trans["transaction_id"].unique(), columns = ['keys'])
for i in range(len(unique_trans)):
    inputkeys.iloc[i]['keys'] = slice_trans["inputs.input_pubkey_base58"][slice_trans["transaction_id"][:]==unique_trans[i]].values

#%%

users = pd.DataFrame(columns = ['user', 'keys']) #use dataframe?
for i in range(len(unique_trans)):
    trans_keys = np.unique(inputkeys.iloc[i][0])
    user = -1
    dropped = 0
    for k in range(len(users)):
        j = k-dropped
        user_keys = users.iloc[j]['keys']
        if len(np.intersect1d(trans_keys,user_keys))>0:
            if user < 0:
                user = j
                users.at[user,'keys'] = np.union1d(user_keys,trans_keys)
            else:
                users.at[user,'keys'] = np.union1d(users.iloc[user]['keys'],user_keys)
                users = users.drop([j])
                dropped += 1
    if user < 0:
        users = users.append({'user':len(users),'keys':trans_keys},ignore_index=True)