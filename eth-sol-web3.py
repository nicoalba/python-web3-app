import os # Import built-in os module to handle environment variables
from dotenv import load_dotenv # Import load_dotenv to read .env files
from web3 import Web3, __version__ as web3_version # Import Web3 and its version from web3.py library
from fastapi import FastAPI, HTTPException # Import FastAPI and HTTPException for building web applications

from solana.rpc.api import Client as SolanaClient # Import SolanaClient to interact with Solana blockchain
from solders.pubkey import Pubkey # Import Pubkey from solders to handle Solana public keys

# Load .env file from project root
load_dotenv()
print(f"Looking for .env file at: {os.path.abspath('.env')}")

# Print web3.py version
print(f"web3.py version: {web3_version}")

# Load provider URL from .env (QuickNode endpoint)
provider_url = os.getenv("WEB3_PROVIDER_URL")
SOLANA_PROVIDER_URL = os.getenv("SOLANA_PROVIDER_URL", "https://api.devnet.solana.com")
print(f"WEB3_PROVIDER_URL: {provider_url}")
if not provider_url:
    raise ValueError("WEB3_PROVIDER_URL not set in .env file")

# Create Solana client
solana_client = SolanaClient(SOLANA_PROVIDER_URL) # Initialize Solana client with provider URL from .env

# Connect to blockchain via QuickNode
w3 = Web3(Web3.HTTPProvider(provider_url)) # Initialize Web3 instance with HTTP provider

# Initialize FastAPI app
app = FastAPI(title="Web3 Balance API", description="API for checking Ethereum/Solana blockchain data") # Set API title and description

# Define helper functions
def get_eth_balance(address: str) -> dict: # Function to get Ethereum balance
    checksum_address = w3.to_checksum_address(address) # Convert address to checksum format for validation
    balance = w3.eth.get_balance(checksum_address) # Query the blockchain (via QuickNode) for the address balance in wei
    balance_eth = w3.from_wei(balance, 'ether') # Convert the balance from wei to ether
    return {"address": checksum_address, "balance_eth": float(balance_eth)} # Return balance in JSON format

def get_sol_balance(address: str) -> dict: # Function to get Solana balance
    pubkey = Pubkey.from_string(address) # Convert the address to a Solana PublicKey object for validation
    response = solana_client.get_balance(pubkey) # Query the Solana blockchain for the address balance
    lamports = response.value # Extract the balance in lamports (smallest unit of Solana)
    sol = lamports / 1_000_000_000 # Convert lamports to SOL (1 SOL = 1 billion lamports)
    return {"address": str(pubkey), "balance_sol": sol} # Return balance in JSON format

# Check connection and print status
if w3.is_connected():
    print("Connected to blockchain!")
    print(f"Latest block number: {w3.eth.block_number}")
else:
    print("Connection failed. Check provider URL or network status.")

# Define API endpoints
@app.get("/block-number") # Get the latest Ethereum block number
async def get_block_number(): # Defines an asynchronous function
    try: # Initiate try/except block
        block_number = w3.eth.block_number # Use Web3 (and Eth module) to query Quicknode and get block number -- defined above
        return {"block_number": block_number} # Return block number in JSON
    except Exception as e: # Catch exceptions/errors
        raise HTTPException(status_code=500, detail=f"Error fetching block number: {str(e)}") # Raise HTTP 500 error with message

@app.get( # Define API endpoint to get Ethereum balance
    "/balance/{address}",
    summary="Get Ethereum balance",
    description="Returns the ETH balance for the provided Ethereum wallet address.",
)
async def get_balance(address: str): # Asynchronous function to get balance
    try: # Initiate try/except block
        return get_eth_balance(address) # Call the helper function to get the balance
    except ValueError as e: # Catch ValueError for invalid address format
        raise HTTPException(status_code=400, detail=f"Invalid address: {address} ({str(e)})")
    except Exception as e: # Catch any other exceptions
        raise HTTPException(status_code=500, detail=f"Error fetching balance: {str(e)}")

@app.get(
    "/solana-balance/{address}",
    summary="Get Solana balance",
    description="Returns the SOL balance for the provided Solana wallet address.",
)
async def get_solana_balance(address: str):
    try:
        return get_sol_balance(address) # Call the helper function to get the Solana balance
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid or failed request: {str(e)}")

# CLI functionality to check Eth address balance
if __name__ == "__main__": # Check if the script is run directly (not imported by another module)-- only runs if file is executed directly
    choice = input("Check balance on (1) Ethereum or (2) Solana? Enter 1 or 2: ").strip() # Prompt user to choose between Ethereum or Solana and strip whitespace

    if choice == "1": # If user chooses Ethereum
        address = input("Enter an Ethereum address to check balance: ") # Prompt user for an Ethereum address and stores as string
        try: # Initiate try/except block
            result = get_eth_balance(address) # Call the helper function to get the balance
            print(f"ETH balance of {result['address']}: {result['balance_eth']} ETH") # Print the balance in ETH
        except ValueError as e: # Catch ValueError for invalid address format
            print(f"Invalid address: {address} ({e})") # Print error message for invalid address
    elif choice == "2": # If user chooses Solana
        address = input("Enter a Solana wallet address to check balance: ") # Prompt user for a Solana address and stores as string
        try: # Initiate try/except block
            result = get_sol_balance(address) # Call the helper function to get the balance
            print(f"SOL balance of {result['address']}: {result['balance_sol']} SOL") # Print the balance in SOL
        except Exception as e: # Catch any exceptions
            print(f"Invalid Solana address or request failed: {e}")
    else:
        print("Invalid choice. Please enter 1 or 2.")
