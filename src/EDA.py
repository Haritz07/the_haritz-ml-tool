import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from clean import clean_transactions
import json

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

print(extract_native_transfers(wallet_address=wallet))
