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
async def get_block_number(): # Defines an asynchronous function
    try: # Initiate try/except block
        block_number = w3.eth.block_number # Use Web3 (and Eth module) to query Quicknode and get block number -- defined above
        return {"block_number": block_number} # Return block number in JSON
    except Exception as e: # Catch exceptions/errors
        raise HTTPException(status_code=500, detail=f"Error fetching block number: {str(e)}") # Raise HTTP 500 error with message

@app.get("/balance/{address}") # Get the balance of a specific Ethereum address (address is parameter)
async def get_balance(address: str): # Defines an asynchronous function that takes an address as a string parameter
    try: # Intiate try/except block
        checksum_address = w3.to_checksum_address(address) # Convert the address to checksum format for validation
        balance = w3.eth.get_balance(checksum_address) # Query the blockchain (via Quicknode) for the address in wei
        balance_eth = w3.from_wei(balance, 'ether') # Convert the balance from wei to ether
        return {"address": checksum_address, "balance_eth": float(balance_eth)} # Return JSON-compatible dictionary w/ 2 keys
    except ValueError as e: # Catch ValueError for invalid address format
        raise HTTPException(status_code=400, detail=f"Invalid address: {address} ({str(e)})") # Raise HTTP 400 error with message
    except Exception as e: # Catch any other exceptions
        raise HTTPException(status_code=500, detail=f"Error fetching balance: {str(e)}") # Raise HTTP 500 error with message

@app.get("/") # Root endpoint to provide a welcome message
async def root(): # Defines an asynchronous function for the root endpoint
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
