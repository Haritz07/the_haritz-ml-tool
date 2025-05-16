from dotenv import load_dotenv
import os
import json
import requests
from datetime import datetime
import sqlite3
import pandas as pd

load_dotenv()

HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")

def get_wallet_data(wallet_address, limit=10):
    url = f"https://api.helius.xyz/v0/addresses/{wallet_address}/transactions?api-key={HELIUS_API_KEY}&limit={limit}"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} \n{response.text}")
        return None


def parse_transaction(transactions: list[dict], wallet_address: str):
    parsed = []
    for tx in transactions:
        base = {
            "wallet": wallet_address,
            "signature": tx.get("signature"),
            "timestamp": tx.get("timestamp"),
            "slot": tx.get("slot"),
            "fee": tx.get("fee"),
            "type": tx.get("type"),
            "source": tx.get("source")
        }

        # Native Transfers
        for nat in tx.get("nativeTransfers", []):
            from_acc = nat.get("fromUserAccount")
            to_acc = nat.get("toUserAccount")

            direction = (
                "outflow" if from_acc == wallet_address
                else "inflow" if to_acc == wallet_address
                else "external"  # in case the transfer is between other wallets
            )

            parsed.append({
                **base,
                "transfer_type": "native",
                "from": from_acc,
                "to": to_acc,
                "amount": nat.get("amount") / 1e9,  # Convert lamports to SOL
                "token_mint": None,
                "direction": direction
            })

        # Token Transfers
        for acc in tx.get("accountData", []):
            for token in acc.get("tokenBalanceChanges", []):
                amt = token["rawTokenAmount"]
                parsed.append({
                    **base,
                    "transfer_type": "token",
                    "from": token.get("userAccount"),
                    "to": token.get("tokenAccount"),
                    "amount": int(amt["tokenAmount"]) / (10 ** int(amt["decimals"])),
                    "token_mint": token.get("mint"),
                    "direction": None  
                })
    return parsed

def store_in_sqlite(data: list[dict], db_path="wallet_txn.db", table="transactions"):
    df = pd.DataFrame(data)
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table, conn, if_exists="append", index=False)
    print(f"[INFO] Stored {len(df)} transactions in {db_path} -> {table}")

def process_wallets(wallets: list[str]):
    all_data = []
    for wallet in wallets:
        print(f"[INFO] Processing wallet: {wallet}")
        txs = get_wallet_data(wallet)
        if txs:
            parsed = parse_transaction(txs, wallet)
            all_data.extend(parsed)
    if all_data:
        df = pd.DataFrame(all_data)
        store_in_sqlite(df)
        return df
    else:
        print("[INFO] No data found.")
        return pd.DataFrame()

if __name__ == "__main__":
    wallet_address = [
        'Be9RC2UC4GkV97XHe31aEULMXpex5ZbDt1cUGiwZjoEg',
        '7HdZJzZV1Va6H2KvyYCym6q7j5BmEdHz7ikUkdNfuGcz',
        '9Y75YHyA8GBAaMsFNqfAEChfwxyvVhgVihkK9NPRWXkS',
        'Habp5bncMSsBC3vkChyebepym5dcTNRYeg2LVG464E96',
        'Be9RC2UC4GkV97XHe31aEULMXpex5ZbDt1cUGiwZjoEg',
        'fLiPgg2yTvmgfhiPkKriAHkDmmXGP6CdeFX9UF5o7Zc',
        '5Hr7wZg7oBpVhH5nngRqzr5W7ZFUfCsfEhbziZJak7fr',
        'GesXXhfSKt4Pt8uEmv4k9sCqmBaZUQJx8diYtsxY3ybi',
        '7uayHqA68uxnC6M4E96jgscL9X7ErtkdSUTU6qcxVkqj',
        '2bFRjjbGHwLHioHKePHxWcZmhgin2fJS7APagagTEn3k',
        '5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9',
        'D7T9BcL2rrPfzXkYMjNpWZ5JVoVbxz6Tfw8A5XotVCFj',
        'AeVFx7hScNvFKLZbdBSKMWkH7ktHLMoUmpHVPUU9pLZH',
        '2rptxFkDpPodk4kMpJ7YXXSkchfpJ9v2MDTxFJ2osHEX',
        '7ZypHtPBQjnf8r7VUaaFSurHdbagG6stmGaA9MsKcGXu',
        '9yj3zvLS3fDMqi1F8zhkaWfq8TZpZWHe6cz1Sgt7djXf',
        '5DaMdrRz7WYhwu273VdKV4f81VkKS7vnRRcS8LDyyxY',
        '9yj3zvLS3fDMqi1F8zhkaWfq8TZpZWHe6cz1Sgt7djXf',
        'G2w2VYdiJXe4PJDrfWGxtvpt4JMBfMmaq74YkQkj1RSS',
        '5DaMdrRz7WYhwu273VdKV4f81VkKS7vnRRcS8LDyyxY',
        '9yj3zvLS3fDMqi1F8zhkaWfq8TZpZWHe6cz1Sgt7djXf',
        '5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1',
        '73hZsLHDXkv9hVEUTGGeQtNSG5zaQUMnkRQMYRiqFfJY',
        '5FRGPJgGWbHwqNBzc3VPB9QJ8ZYHVfJf79dxhdBbdtfJ',
        '9di29gYZ5peS6WnzFxagv12s1ZY1cq7mbB6NppGr2bCg',
        '25S13Dzogrcq49EMUdhkhsfUBFSSAgTHJTgcWfcY51nG',
        '3wvf5bLwnHDfFfngobVJiyjstYeVAwWrHT1RrRbzUuyK',
        'FGJiPiTdKTCdpxLPnuBcXnhsfxzcJsMzqMRJbK9N7zvo',
        '3VoTsHVWApR4t4sKJHbRGs2YGzE7qGQEwU85GkohueNe',
        'gtaPm2UoHkc9smB7kNgST8To8mrTGX5T7fes8rtcWZR',
        'GfHViFGvDqhzbaRHYmCgJ9SmBSqQ4gPxDdRfSw1VK1qR',
        '2c5WdJJZtcgtguNqRKaHPi2JqaUXCkVA7w8hwX2yq9Dn',
        'GT9ifbUgGbRoVYi41mSAeNaWtE1tej7TnsGo5V28VeYS',
        '8UjUoFjYCGgHYjFhagec1g6ky7TLgxzBozbS8WExzF6i',
        'FHrkxyAQYDRWAKo6fo93o58fPeYriwCDfipg24225WJU',
        'FDbUZxSkANsfpRvAPNHt3qRTbYi9CexBBuk5eH7crcdg',
        '2P7CZCzXynAq5PYgs3WHZnJ3XgWneQ5mTub2QCH4vQ13',
        'QQ7MY8ZVBGynwsdG4zmEZM1s6zdQ9PnV4PCMat3cw3x',
        'G37AVd8MgtNd7jrX1n8SGiQZehZNdQNUWLS46qu29qq4',
        '3qis3eG4JPqk4Eoxg8R9ogJ7doEETSZmKxqWjCWaWe79'
    ]
    result = process_wallets(wallet_address)

    if result is None or len(result) == 0:
        print("[INFO] No transactions found.")
    else:
        print(f"[INFO] Found {len(result)} transactions.")
        print(result.head())
        result.to_csv("wallet_transactions.csv", index=False)
