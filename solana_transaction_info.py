#Not working correctly: extracts too much data
from theblockchainapi import SolanaAPIResource, SolanaNetwork
from decouple import config
import json

API_KEY = config("BLOCKCHAIN_API_KEY")
SECRET_KEY = config("BLOCKCHAIN_API_SECRET")
def main():
    BLOCKCHAIN_API_RESOURCE = SolanaAPIResource(
        api_key_id=API_KEY,
        api_secret_key=SECRET_KEY
    )
    tx_signature = "3XhxLMMf3nwhQpwVUKjNtQUfizYDJ3WzQwp2vsXsLCcLX2NfFiHQTJRQz4f8ncCiTBFYRTV9GYvqRnYP7QqroW9b"
    transaction_info = BLOCKCHAIN_API_RESOURCE.get_solana_transaction(
            tx_signature=tx_signature,
            network=SolanaNetwork.MAINNET_BETA
        )
    print(json.dumps(transaction_info, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()