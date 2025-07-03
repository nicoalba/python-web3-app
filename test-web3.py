from web3 import Web3
import web3  # Import the web3 module explicitly

print(web3.__version__)  # Should print 7.12.0
provider_url = os.getenv("WEB3_PROVIDER_URL")
w3 = Web3(Web3.HTTPProvider(provider_url))
if w3.is_connected():
    print("Connected to blockchain!")
    print(f"Latest block: {w3.eth.block_number}")
else:
    print("Connection failed.")
