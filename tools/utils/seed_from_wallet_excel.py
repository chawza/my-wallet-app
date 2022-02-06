import sqlite3
from typing import List

import pandas as pd
import numpy as np

DB_CONN_PATH = 'my_wallet_app/db.sqlite3'
excel_path = "C:/Users/Nabeel/OneDrive/Documents/finance records/Wallet Rep Aug 2019 4 Dec 2021.xls"
user_name = 'nabeel'

transactions = pd.read_excel(excel_path)
conn = sqlite3.connect(DB_CONN_PATH)


def get_account_list(table: pd.DataFrame):
    return table['account'].unique()


def populate_user_accounts(account_list: List[str]):
    for account in account_list:
        query = f'INSERT INTO app_user_useraccount(name, user_id_id) VALUES("{account}", "{user_id}")'
        conn.execute(query)
    conn.commit()


def find_account_by_name(name):
    query = f'SELECT * FROM app_user_useraccount WHERE name == "{name}"'
    account = conn.execute(query).fetchall()[0]
    return {
        "id": account[0],
        "name": account[1],
        "user_user_id": account[2]
    }


def insert_transaction_to_account(row: pd.Series, account_id: int):
    category = row['category']
    currency = row['currency']
    amount = row['amount']
    tran_type = row['type']
    note = 'NULL' if (row['note'] is np.nan) else row['note']
    date = row['date']
    is_transfer = row['transfer']
    account_id_id = account_id

    query = 'INSERT INTO wallet_transactions ' \
            '(category, currency, amount, type, note, date, is_transfer, account_id) ' \
            f'values("{category}", "{currency}", "{amount}", "{tran_type}", ' \
            f'"{note}", "{date}", "{is_transfer}", "{account_id_id}")'
    conn.execute(query)


def populate_transactions(account_list: List[str]):
    print('Populating Transactions')
    for account in account_list:
        account = find_account_by_name(account)
        print(f'inserting account {account["name"]}')

        account_transactions = transactions.loc[transactions['account'] == account['name']]
        n_success = 0
        n_failed = 0
        for idx, tran in account_transactions.iterrows():
            try:
                insert_transaction_to_account(tran, account['id'])
                n_success += 1
            except Exception as e:
                print(e)
                n_failed += 1

        print(f'success: {n_success}\tfailed: {n_failed}')
    conn.commit()
    print('Transactions committed')


# Find user's id
find_user_query = "SELECT id from app_user_user"
user_id = conn.execute(find_user_query).fetchall()[0][0]

# create user accounts
accounts = get_account_list(transactions)
print(accounts)
# populate_user_accounts(accounts)
populate_transactions(accounts)
