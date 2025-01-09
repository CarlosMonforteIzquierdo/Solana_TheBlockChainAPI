import json

def view_swap_info(file_path):
    """
    Extrae la información de swaps de tokens desde un archivo JSON.
    Un swap ocurre cuando un usuario envía un token y recibe otro dentro de la misma transacción.
    """
    try:
        # Cargar datos del archivo JSON
        with open(file_path, "r") as file:
            data = json.load(file)
        
        swaps = []
        processed_pairs = set() #Conjunto para evitar duplicados

        for transaction in data:
            # Validar si existen transferencias de tokens
            token_transfers = transaction.get("tokenTransfers", [])
            
            #Comparar transferencias para detectar swaps
            for i, transfer_out in enumerate(token_transfers):
                for transfer_in in token_transfers:
                    if(
                        transfer_out["fromUserAccount"] == transfer_in["toUserAccount"] and transfer_out["toUserAccount"] == transfer_in["fromUserAccount"]
                    ):
                        pair_key = tuple(sorted([transfer_out["mint"], transfer_in["mint"]]))
                        if pair_key not in processed_pairs:
                            swaps.append({
                                "sent_mint": transfer_out.get("mint"),
                                "sent_amount": transfer_out.get("tokenAmount"),
                                "received_mint": transfer_in.get("mint"),
                                "received_amount": transfer_in.get("tokenAmount")
                            })
                            processed_pairs.add(pair_key) #Marcar par como procesado
            

        return swaps

    except FileNotFoundError:
        print(f"El archivo {file_path} no existe.")
        return []
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON. Asegúrate de que el archivo tenga el formato correcto.")
        return []

if __name__ == "__main__":
    file_path = "transaction_details.json"  # Nombre del archivo JSON
    swaps = view_swap_info(file_path)

    # Imprimir los resultados
    if swaps:
        print("Swaps encontrados:")
        for idx, swap in enumerate(swaps, start=1):
            print(f"Swap {idx}:")
            print(f"  Sent: {swap['sent_amount']} {swap['sent_mint']}")
            print(f"  Received: {swap['received_amount']} {swap['received_mint']}")
    else:
        print("No se encontraron swaps en los datos proporcionados.")