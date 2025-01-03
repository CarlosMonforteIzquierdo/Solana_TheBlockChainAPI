#    Obtiene detalles de una transacción en la blockchain de Solana para identificar los tokens vendidos y comprados.
import requests
import json
from decouple import config

API_KEY = config("HELIUS_API_KEY")  #Colocar API key de RPC 
def get_transaction_details(signature):
    
    base_url = f"https://api.helius.xyz/v0/transactions/{signature}?api-key={API_KEY}"
    
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        transaction_data = response.json()
        
        # Extraer balances antes y después de la transacción
        pre_balances = transaction_data.get("preTokenBalances", [])
        post_balances = transaction_data.get("postTokenBalances", [])
        
        token_changes = []
        
        #To compare only swaps and exclude send/receive transactions wallet address must be the same
        for pre, post in zip(pre_balances, post_balances):
            if pre["owner"] == post["owner"]:  
                mint_address = pre["mint"]
                pre_amount = int(pre["uiTokenAmount"]["amount"])
                post_amount = int(post["uiTokenAmount"]["amount"])
                
                if pre_amount != post_amount:
                    change = post_amount - pre_amount
                    token_changes.append({
                        "mint": mint_address,
                        "amount_change": change,
                        "direction": "bought" if change > 0 else "sold",
                        "decimals": pre["uiTokenAmount"]["decimals"],
                        "ui_amount": abs(change) / (10 ** pre["uiTokenAmount"]["decimals"])
                    })
        # Estructurar el JSON final
        result = {
            "transaction_signature": signature,
            "token_changes": token_changes
        }
        return result
    
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return {"error": "Error al obtener datos de la transacción"}

if __name__ == "__main__":
    # Ejemplo de uso
    transaction_signature = "3XhxLMMf3nwhQpwVUKjNtQUfizYDJ3WzQwp2vsXsLCcLX2NfFiHQTJRQz4f8ncCiTBFYRTV9GYvqRnYP7QqroW9b"
    result = get_transaction_details(transaction_signature)
    print(json.dumps(result, indent=4))
