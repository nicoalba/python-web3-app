# python-web3-app

Work in progress: Vibe coding a Python web3 app that connects to the Ethereum Sepolia testnet using `web3.py` to query the ETH balance of a user-provided address. 

## Context

This was a learning exercise where I used AI to help guide me through the process as developing a web3 app that queries the blockchain. As someone actively learning Python, this was very helpful for me and I made sure to add comments on every line to document what the code does.

## Feature

- Connects to the Sepolia testnet via a QuickNode endpoint.
- Prompts users to input an Ethereum address and validates it using web3.py's checksum address conversion.
- Queries and displays the ETH balance of the provided address in a user-friendly format.
- - Uses a Coinbase Wallet for testing with Sepolia test ETH, showcasing wallet setup and faucet usage.
Implements error handling for invalid addresses and connection issues.

## Tech stack

- Python 3: Core programming language.
- `web3.py` (`v7.12.0`): Python library for Ethereum blockchain interaction.
- `python-dotenv: Loads environment variables (e.g., QuickNode API URL) from a .env file.
- Coinbase Wallet: Non-custodial wallet for managing Sepolia testnet addresses and test ETH.
- QuickNode: Provides the Sepolia testnet endpoint for blockchain access.

## Prerequisites

- Python 3.6+ installed.
- A Coinbase Wallet set to the Sepolia testnet.
- Test ETH in your Coinbase Wallet’s Sepolia address obtained from a faucet like PoW Faucet).
- A QuickNode account with a Sepolia endpoint URL (free tier available).

## Installation

1. Clone the repo:

    ```bash
    git clone https://github.com/nicoalba/python-web3-app.git
    cd python-web3-app
    ```

2. Set Up a Virtual Environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install web3 python-dotenv
    ```


4. Configure environment variables:

    1. Create a .env file in the project root.
    2. Add your QuickNode Sepolia endpoint URL:WEB3_PROVIDER_URL=https://your-quicknode-sepolia-url

        ```bash
        WEB3_PROVIDER_URL=https://your-quicknode-sepolia-url
        ```
    
    3. Get your URL by signing up at QuickNode and creating a Sepolia endpoint.


5. Set Up Coinbase Wallet:

    1. Install the Coinbase Wallet browser extension from coinbase.com/wallet.
    2. Switch to the Sepolia Test Network in the wallet.
    3. Fund your Sepolia address with test ETH from PoW Faucet or Chainlink Faucet.

## Usage

1. Run the script:

    ```bash
    python test-web3.py
    ```
    
    The script will:

    1. Load the QuickNode endpoint from .env.
    2. Connect to the Sepolia testnet and display the latest block number.
    3. Prompt for an Ethereum address.
    4. Display the ETH balance of the address (e.g., ETH balance of 0xYourAddress: 0.1 ETH).

  2. Enter your Coinbase Wallet’s Sepolia address (or any valid Ethereum address) to check its balance.

## Example output

```plain
Looking for .env file at: /path/to/python-web3-app/.env
web3.py version: 7.12.0
WEB3_PROVIDER_URL: https://omniscient-distinguished-sailboat...
Connected to blockchain!
Latest block number: 8693694
Enter an Ethereum address to check balance: 0xYourAddress
ETH balance of 0xYourAddress: 0.1 ETH
```

## Future enhancements / to do

- Add ERC-20 token balance queries for Sepolia test tokens.
- Create a web interface using FastAPI for user-friendly interaction.

