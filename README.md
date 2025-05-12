# The Haritz Project - Wallet Risk Analysis Scoring API

## Overview
The Haritz Project is a ML-powered API that assesses the **risk score** and **risk level** of a Solana wallet address using different transaction behaviours. The project is powered with **FastAPI**, the API takes only the wallet address as input and the trained model (**XGBoost**) returns the calculated risk score and risk level, the risk level is a percentage of how heavey the risk of that wallet is, the risk score will diplay either 0 or 1, where 0 implies **not risky** and 0 implies **risky**, but the risk level returns how heavy that risk might be. This repository contains all the necessary files and documentation to help you understand, contribute to, and use the project effectively.

## Features
- Accepts a single wallet address as input
- Feature engineering: Automatically fetches and engineers behaviourial features
- Predicts a wallet risk score and risk level using an ML model
- Returns a JSON response with:
    -'wallet_address'
    -'risk_score'
    -'risk_level'
- Interactive Swagger UI for testing


## Tech Stack
- Python 3.11+
- FastAPI
- XGBoost
- Pandas
- SQLite for storage
- uv for dependency management

## Installation
To get started with the project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/DarkKnight845/WalletWatch_HAR_ITZ
    ```
2. Navigate to the project directory:
    ```bash
    cd The_Haritz
    ```

3. Install dependencies:
    ```bash
    pip install uv 
    uv pip install -r requirements.txt
    ```

## Run the API
```bash
uvicorn src.predictor:app --reload
```

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add feature-name"
    ```
4. Push to the branch:
    ```bash
    git push origin feature-name
    ```
5. Open a pull request.


## Contact
For questions or feedback, please contact TheDarkKnight or Haritz at *ayemiade2006@gmail.com*.
