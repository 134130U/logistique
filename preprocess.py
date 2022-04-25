import pandas as pd
from collect import get_data
import numpy as np
import schedule
import time
import datetime as t

# Data preprocessing

def prepar():
    df_old = pd.read_csv('Data/prev_data.csv')
    df_stock = pd.read_csv('Data/stock.csv')
    df_price = pd.read_csv('Data/price.csv')
    df_remove = pd.read_csv('Data/to_remove.csv')
    df_age = pd.read_csv('Data/age.csv')
    df_age_old = pd.read_csv('Data/age_prev.csv')

    df_stock = df_stock[~df_stock['true_serial'].isnull()]
    df_stock.drop_duplicates(inplace=True)

    df_system = df_stock[df_stock['is_main_system'] == True]
    df_value_age = df_system.merge(df_age, on='product_id', how='inner')
    value_cond = (df_value_age['etat'].isin(['Endommagé', 'waste', 'canceled']) | df_value_age['is_archived'] == True)
    df_value_age['valeur'] = np.where(value_cond, 0, df_value_age['cost_price'])
    df_age_new = df_value_age[['date_at', 'mois', 'category', 'product_type', 'bucket', 'country', 'valeur']].groupby(
        ['date_at', 'mois', 'bucket', 'product_type', 'category', 'country']).sum().reset_index()

    df_system.loc[:, 'group'] = 'system'

    df_compo = df_stock[df_stock['is_main_system'] == False]
    df_price.columns = ['product_type', 'type', 'Cout']
    df_compo1 = df_compo.merge(df_price, on='product_type', how='left')
    df_system_decom = df_compo1[df_compo1['Cout'].isnull()]
    df_system_decom.loc[:, 'group'] = 'principal'

    df_system_decom = df_system_decom.merge(df_remove, on='product_type', how='left')
    df_system_decom.head()
    df_system_decom['cost_price'] = df_system_decom['cost_price'] - df_system_decom['prix']
    col = list(df_system.columns)
    df_system_decom = df_system_decom[col]

    df_composant = df_compo1[df_compo1['Cout'].notnull()]
    df_composant.loc[:, 'group'] = 'composant'
    df_composant.loc[:, 'cost_price'] = df_composant.loc[:, 'Cout']
    df_composant = df_composant[col]
    data = pd.concat([df_system, df_system_decom, df_composant], axis=0)

    value_condition = (data['etat'].isin(['Endommagé', 'waste', 'canceled']) | data['is_archived'] == True)
    loss_condition = (
                data['etat'].isin(['Endommagé', 'waste', 'canceled']) | ~data['stock_name'].str.lower().str.startswith(
            'zzz'))
    reimburse_condition = (
                data['etat'].isin(['Endommagé', 'waste', 'canceled']) | ~data['stock_name'].str.lower().str.startswith(
            'yyy'))

    data['valeur'] = np.where(value_condition, 0, data['cost_price'])
    data['loss'] = np.where(loss_condition, 0, data['cost_price'])
    data['reimburse'] = np.where(reimburse_condition, 0, data['cost_price'])

    df_new = data[['date_at', 'mois', 'category', 'product_type', 'country', 'valeur', 'loss', 'reimburse']].groupby(
        ['date_at', 'mois', 'product_type', 'category', 'country']).sum().reset_index()
    finale = pd.concat([df_old,df_new],axis=0)
    finale_age = pd.concat([df_age_old, df_age_new], axis=0)
    if t.date.today().day ==1:
        finale.to_csv('Data/prev_data.csv', index=False)
        finale_age.to_csv('Data/age_prev.csv', index=False)
        finale.to_csv('Data/final_data.csv', index=False)
        finale_age.to_csv('Data/age_data.csv', index=False)

        today = t.date.today()

        jour = today.strftime("%Y%m%d")

        daily_save = 'Data/data'+jour+'.csv'

        df_new.to_csv(daily_save,index=False)
        print('The data have been well updated')

    print ('Tout est bon. Cava bien')
    return ''


schedule.every().day.at("11:55").do(get_data)
schedule.every().day.at("12:00").do(prepar)

while True:
    schedule.run_pending()
    time.sleep(1)