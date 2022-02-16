from dotenv import load_dotenv
import os
import sqlite3
from typing import List
import pandas as pd
import numpy as np
import sys
from dateutil.parser import parse

load_dotenv('tools/utils/.env')
DB_CONN_PATH = 'my_wallet_app/db.sqlite3'
excel_path = os.environ.get('transactions_file_path')
csv_path = os.environ.get('csv_file_path')
print('excel_path', excel_path)
user_name = 'nabeel'

if '--csv' in sys.argv:
    transactions = pd.read_csv(csv_path, sep=';')
else:
    transactions = pd.read_excel(excel_path)

conn = sqlite3.connect(DB_CONN_PATH)


def get_account_list(table: pd.DataFrame):
    return table['account'].unique()


def populate_user_accounts(account_list: List[str]):
    for account in account_list:
        query = f'INSERT INTO wallet_useraccount(name, user_id) VALUES("{account}", "{user_id}")'
        conn.execute(query)
    conn.commit()


def find_account_by_name(name):
    query = f'SELECT * FROM wallet_useraccount WHERE name == "{name}"'
    account = conn.execute(query).fetchall()[0]
    return {
        "id": account[0],
        "name": account[1],
        "user_user_id": account[2]
    }


def insert_transaction_to_account(row: pd.Series, account_id: int):
    category = row['category']
    currency = row['currency']
    amount = int(row['amount'])
    tran_type = row['type']
    note = 'NULL' if (row['note'] is np.nan) else row['note']
    date = row['date']
    is_transfer = bool(row['transfer'])

    query = 'INSERT INTO wallet_transactions ' \
            '(category, currency, amount, type, note, date, is_transfer, account_id) ' \
            f'values("{category}", "{currency}", "{amount}", "{tran_type}", ' \
            f'"{note}", "{date}", "{is_transfer}", "{account_id}")'
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


if __name__ == '__main__':
    # Find user's id
    find_user_query = "SELECT id from app_user_user"
    user_id = conn.execute(find_user_query).fetchall()[0][0]

    # create user accounts
    accounts = get_account_list(transactions)
    # populate_user_accounts(accounts)
    populate_transactions(accounts)
