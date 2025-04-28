import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from clean import clean_transactions
import json
import sqlite3


wallet_data = pd.read_csv('C:\Users\ayemi\OneDrive\Documents\The_Haritz\data\cleaned_wallet_transactions.csv')



wallet = [
        "Be9RC2UC4GkV97XHe31aEULMXpex5ZbDt1cUGiwZjoEg",
        "7HdZJzZV1Va6H2KvyYCym6q7j5BmEdHz7ikUkdNfuGcz",
        '9Y75YHyA8GBAaMsFNqfAEChfwxyvVhgVihkK9NPRWXkS',
        'Habp5bncMSsBC3vkChyebepym5dcTNRYeg2LVG464E96',
        'Be9RC2UC4GkV97XHe31aEULMXpex5ZbDt1cUGiwZjoEg',
        'fLiPgg2yTvmgfhiPkKriAHkDmmXGP6CdeFX9UF5o7Zc',
        '5Hr7wZg7oBpVhH5nngRqzr5W7ZFUfCsfEhbziZJak7fr',
        'GesXXhfSKt4Pt8uEmv4k9sCqmBaZUQJx8diYtsxY3ybi',
        '7uayHqA68uxnC6M4E96jgscL9X7ErtkdSUTU6qcxVkqj'
    ]



# geetting different features from the data to test for the model
def extract_native_transfers(wallet_address: list[str]) -> pd.DataFrame:
    with open(r'C:\Users\ayemi\OneDrive\Documents\The_Haritz\data\wallet_data.json', 'r') as f:
        data = json.load(f)
    records = []
    for transaction in data:
        transfers = transaction.get("nativeTransfers", [])
        for transfer in transfers:
            from_acct = transfer.get("fromUserAccount")
            to_acct = transfer.get("toUserAccount")
            amount = transfer.get("amount", 0)
            amount_sol = amount / 1e9
            
            if from_acct in wallet_address or to_acct in wallet_address:
                direction = (
                    'outflow' if wallet_address == from_acct else 'inflow'
                )
                records.append({
                    "signature": transaction.get("signature"),
                    "timestamp": transaction.get("timestamp"),
                    "slot": transaction.get("slot"),
                    "fee": transaction.get("fee"),
                    "type": transaction.get("type"),
                    "direction": direction,
                    "from": from_acct,
                    "to": to_acct,
                    "amount_sol": amount_sol,
                    "program_ids": [instr['programId'] for instr in transaction.get('instructions', [])]
                })
    return pd.DataFrame(records)


feaures_df = extract_native_transfers(wallet)

def mint_dump_logic(data: pd.DataFrame) -> pd.DataFrame:
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s', errors='coerce')
    # get mint transactions
    mint_df = data[data['amount'] > 0].copy()
    mint_df.rename(columns={'timestamp': 'mint_timestamp'}, inplace=True)

    first_mint = mint_df.groupby('token_mint')['mint_timestamp'].min().reset_index()

    # get dump transactions
    dump_df = data[data['amount'] < 0].copy()
    dump_df.rename(columns={'timestamp': 'dump_timestamp'}, inplace=True)

    dump_joined = pd.merge(dump_df, first_mint, on='token_mint', how='inner')
    dump_joined['mint_to_dump_time'] = (dump_joined['dump_timestamp'] - dump_joined['mint_timestamp']).dt.total_seconds() / 60

    mint_dump_summary = dump_joined.groupby('token_mint').agg({
        'token_mint': 'nununique',
        'mint_to_dump_time': 'mean'
    }).reset_index()

    mint_dump_summary.rename(columns={'token_mint': 'tokens_minted_and_dumped',
                                      'mint-to_dump_time':"avg_mint_to_dump_minutes"}, inplace=True)
    
    # merge the data with the feature df
    # feaures_df = pd.merge(feaures_df, mint_dump_summary, on='wallet', how='left')

def fast_dumper_logic(data: pd.DataFrame) -> pd.DataFrame:
    early_buy_mins = 10
    fast_dump_mins = 10

    first_mint_time = data[data['amount'] > 0].groupby('token_mint')['timestamp'].min().reset_index()
    first_mint_time.rename(columns={'timestamp': 'mint_timestamp'}, inplace=True)




def store_in_sqlite(data: pd.DataFrame, db_path="wallet_txn.db", table="transactions"):
    pass

