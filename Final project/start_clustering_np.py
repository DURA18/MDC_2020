#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 20:49:02 2020

@author: isabel
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:52:08 2020

@author: isabel
"""
import numpy as np
import pandas as pd
import datetime as dt
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
slice_trans =sorted_transactions#[n_slice:3*n_slice]
unique_trans = slice_trans["transaction_id"].unique()
unique_keys = slice_trans["inputs.input_pubkey_base58"].unique()

inputkeys = pd.DataFrame(index = slice_trans["transaction_id"].unique(), columns = ['keys'])
for i in range(len(unique_trans)):
    if i%1000 == 0:
        print(dt.datetime.now())
        print("at transaction: " + str(i))
    inputkeys.iloc[i]['keys'] = slice_trans["inputs.input_pubkey_base58"][slice_trans["transaction_id"][:]==unique_trans[i]].values

#%%

users = pd.DataFrame(columns = ['user', 'keys']) #use dataframe?

#users_np = np.zeros((0,0), dtype="object")
#users_np = np.chararray((0,0))
#users_np = np.array([[],[]])
users_np = np.genfromtxt('np_user_keys_untill_sorted_transaction' + str(gebleven) + '.csv', delimiter=',', dtype = str)
for i in range(gebleven, len(unique_trans)):
    if i%1000 == 0:
        print(dt.datetime.now())
        print("at transaction: " + str(i))
    if i%10000 == 0:
        np.savetxt("np_user_keys_untill_sorted_transaction" + str(i) + ".csv", users_np, delimiter=",", fmt='%s')
    
    user_keys = np.unique(inputkeys.iloc[i][0])
    existing_keys = np.intersect1d(user_keys,users_np)
    if len(user_keys) == 1 and len(existing_keys) == 1:
        continue
    for key in existing_keys:
        #print("here")
        if key in users_np:
            old_user_i = np.argwhere(users_np == key)[0,0]
            user_keys = np.union1d(user_keys,users_np[old_user_i,:])
            user_keys = user_keys[user_keys != '']
            users_np = np.delete(users_np, old_user_i, axis = 0)
    #print(user_keys)
    n_users = users_np.shape[0]
    max_n_keys = users_np.shape[1]
    n_user_keys = len(user_keys)
    new_max_n_keys = max(max_n_keys, n_user_keys)
    
    new_users = np.zeros((n_users+1,new_max_n_keys), dtype="object")
    new_users[:,:] = ''
    new_users[:n_users,:max_n_keys] = users_np
    new_users[-1,:n_user_keys] = user_keys
    
    users_np = new_users
    #print(users_np.dtype)


np.savetxt("np_user_keys.csv", users_np, delimiter=",", fmt='%s')