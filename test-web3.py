import os # Import built-in os module to handle environment variables
from dotenv import load_dotenv # Import load_dotenv to read .env files
from web3 import Web3 # Import Web3 from web3.py library to interact with Ethereum blockchain
import web3 # Import web3 module to access its version

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

# Check connection
if w3.is_connected():
    print("Connected to blockchain!")
    print(f"Latest block number: {w3.eth.block_number}")

    # Get address from user input
    address = input("Enter an Ethereum address to check balance: ") # Input stored in variable 'address'
    try:
        checksum_address = w3.to_checksum_address(address) # Convert input to checksum address
        balance = w3.eth.get_balance(checksum_address) # Get balance in wei
        balance_eth = w3.from_wei(balance, 'ether') # Convert balance to ether
        print(f"ETH balance of {checksum_address}: {balance_eth} ETH") # Print balance in ether
    except ValueError as e: # Handle invalid address error
        print(f"Invalid address: {address} ({e})") # Print error message
else:
    print("Connection failed. Check provider URL or network status.")
