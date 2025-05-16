import pandas as pd

# data = pd.read_csv(r'C:\Users\ayemi\OneDrive\Documents\The_Haritz\data\wallet_transactions.csv')
# print(data)

def clean_transactions(data: pd.DataFrame) -> pd.DataFrame:
    print("[INFO] Cleaning transaction data...")
    essential_columns = [
        "wallet", "signature", "timestamp", "from", "to", "amount"
    ]
    before_rows = len(data)
    clean_data = data.dropna(subset=essential_columns)
    clean_data.reset_index(drop=True, inplace=True)
    after_rows = len(clean_data)
    print(f"[INFO] Dropped {before_rows - after_rows} rows with missing essential columns.")
    
    # Convert timestamp and amount to datetime and numeric types
    clean_data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s', errors='coerce')
    clean_data['amount'] = pd.to_numeric(data['amount'], errors='coerce')

    clean_data['token_mint'] = clean_data['token_mint'].fillna('N/A')
    clean_data['transfer_type'] = clean_data['transfer_type'].fillna('N/A')
    clean_data['direction'] = clean_data['direction'].fillna('N/A')
    clean_data['fee'] = clean_data['fee'].fillna(0)

    print(f"[INFO] Cleaned data: {len(clean_data)} rows remaining.")
    return clean_data


if __name__ == "__main__":
    # clean_transactions(pd.read_csv(r'C:\Users\ayemi\OneDrive\Documents\The_Haritz\data\wallet_transactions.csv'))
    
    data = pd.read_csv(r'C:\Users\ayemi\OneDrive\Documents\The_Haritz\data\wallet_transactions.csv')
    cleaned_data = clean_transactions(data)
    
    print(cleaned_data)
    cleaned_data.to_csv(r'C:\Users\ayemi\OneDrive\Documents\The_Haritz\data\cleaned_wallet_transactions.csv', index=False)
    print("[INFO] Cleaned data saved to cleaned_wallet_transactions.csv")