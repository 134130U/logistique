import pandas as pd
import matplotlib.pyplot as plt
from collect import get_data
import numpy as np
import re


get_data()

df_stock = pd.read_csv('Data/stock.csv')
df_price = pd.read_csv('Data/price.csv')

df_stock = df_stock[~df_stock['true_serial'].isnull()]
df_stock.drop_duplicates(inplace=True)

df_system = df_stock[df_stock['is_main_system']==True]
df_system['group'] = 'system'

df_compo = df_stock[df_stock['is_main_system']==False]
df_price.columns = ['product_type','type','Cout']
df_compo1 = df_compo.merge(df_price ,on='product_type',how='left') 
df_system_decom = df_compo1[df_compo1['Cout'].isnull()]
df_system_decom['group'] = 'decompo'
col = list(df_system.columns)
df_system_decom = df_system_decom[col]