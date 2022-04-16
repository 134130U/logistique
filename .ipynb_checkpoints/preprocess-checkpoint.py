import pandas as pd
import matplotlib.pyplot as plt
from collect import get_data
import numpy as np
import re


def prepar():
    
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

    df_composant= df_compo1[df_compo1['Cout'].notnull()]
    df_composant['group'] = 'composant'
    df_composant['cost_price'] = df_composant['Cout']
    df_composant = df_composant[col]
    data = pd.concat([df_system,df_system_decom,df_composant],axis=0)

    value_condition = (data['etat'].isin(['Endommagé','waste','canceled']) | data['is_archived']==True)
    loss_condition = (data['etat'].isin(['Endommagé','waste','canceled']) | data['stock_name'].str.lower().str.startswith('zzz'))

    data['valeur'] = np.where(value_condition,0,data['cost_price'])
    data['loss'] = np.where(loss_condition,0,data['cost_price'])
    
    data.to_csv('Data/final_data.csv',index=False)
    
    print('Data are ready for analysis')
    
    return ''