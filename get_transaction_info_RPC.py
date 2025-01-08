import requests
import json
from decouple import config

API_KEY = config("HELIUS_API_KEY")

def get_transaction_details(signature):
    base_url = f"https://api.helius.xyz/v0/transactions/{signature}?api-key={API_KEY}"
    
    try:
        response = requests.get(base_url)
        if response.status_code != 200:
            return {
                "error": "Error al obtener datos de la transacción",
                "status_code": response.status_code,
                "details": response.text
            }
        
        transaction_data = response.json()
        pre_balances = transaction_data.get("preTokenBalances", [])
        post_balances = transaction_data.get("postTokenBalances", [])
        
        token_changes = []
        for pre, post in zip(pre_balances, post_balances):
            if pre.get("owner") == post.get("owner"):
                mint_address = pre.get("mint", "unknown")
                pre_amount = int(pre.get("uiTokenAmount", {}).get("amount", 0))
                post_amount = int(post.get("uiTokenAmount", {}).get("amount", 0))
                decimals = pre.get("uiTokenAmount", {}).get("decimals", 0)
                
                change = post_amount - pre_amount
                if change != 0:
                    token_changes.append({
                        "mint": mint_address,
                        "amount_change": change,
                        "direction": "bought" if change > 0 else "sold",
                        "decimals": decimals,
                        "ui_amount": abs(change) / (10 ** decimals)
                    })
        
        return {
            "transaction_signature": signature,
            "token_changes": token_changes
        }
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Error al conectar con la API: {e}"}

if __name__ == "__main__":
    transaction_signature = "3XhxLMMf3nwhQpwVUKjNtQUfizYDJ3WzQwp2vsXsLCcLX2NfFiHQTJRQz4f8ncCiTBFYRTV9GYvqRnYP7QqroW9b"
    result = get_transaction_details(transaction_signature)
    
    # Guardar en un archivo JSON
    with open("transaction_details.json", "w") as json_file:
        json.dump(result, json_file, indent=4)
    
    print("Información guardada en 'transaction_details.json'")
