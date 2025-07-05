import os # Import built-in os module to handle environment variables
from dotenv import load_dotenv # Import load_dotenv to read .env files
from web3 import Web3 # Import Web3 from web3.py library to interact with Ethereum blockchain
import web3 # Import web3 module to access its version
from fastapi import FastAPI, HTTPException # Import FastAPI and HTTPException for building web applications

# Load .env file from project root
load_dotenv()
print(f"Looking for .env file at: {os.path.abspath('.env')}")

# Print web3.py version
print(f"web3.py version: {web3.__version__}")

# Load provider URL from .env (QuickNode endpoint)
provider_url = os.getenv("WEB3_PROVIDER_URL")
print(f"WEB3_PROVIDER_URL: {provider_url}")
if not provider_url:
    raise ValueError("WEB3_PROVIDER_URL not set in .env file")

# Connect to blockchain via QuickNode
w3 = Web3(Web3.HTTPProvider(provider_url))

# Initialize FastAPI app
app = FastAPI(title="Web3 Balance API", description="API for checking Ethereum blockchain data") # Set API title and description

# Check connection and print status
if w3.is_connected():
    print("Connected to blockchain!")
    print(f"Latest block number: {w3.eth.block_number}")
else:
    print("Connection failed. Check provider URL or network status.")

# Define API endpoints
@app.get("/block-number") # Get the latest Ethereum block number
async def get_block_number():
    try:
        block_number = w3.eth.block_number
        return {"block_number": block_number}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching block number: {str(e)}")

@app.get("/balance/{address}") # Get the balance of a specific Ethereum address
async def get_balance(address: str):
    try:
        checksum_address = w3.to_checksum_address(address)
        balance = w3.eth.get_balance(checksum_address)
        balance_eth = w3.from_wei(balance, 'ether')
        return {"address": checksum_address, "balance_eth": float(balance_eth)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid address: {address} ({str(e)})")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching balance: {str(e)}")

@app.get("/") # Root endpoint to provide a welcome message
async def root():
    return {"message": "Welcome to the Web3 Balance API! Visit /docs for API documentation."}

# Keep the original CLI functionality
if __name__ == "__main__":
    address = input("Enter an Ethereum address to check balance: ")
    try:
        checksum_address = w3.to_checksum_address(address)
        balance = w3.eth.get_balance(checksum_address)
        balance_eth = w3.from_wei(balance, 'ether')
        print(f"ETH balance of {checksum_address}: {balance_eth} ETH")
    except ValueError as e:
        print(f"Invalid address: {address} ({e})")
