import json

def extract_swap_info(file_path):
    try:
        # Cargar los datos desde el archivo JSON
        with open(file_path, "r") as file:
            data = json.load(file)

        # Lista para almacenar los swaps
        swaps = []

        # Recorrer las transacciones y filtrar los swaps
        for transaction in data:
            if "tokenTransfers" in transaction:
                token_transfers = transaction["tokenTransfers"]
                for transfer in token_transfers:
                    if transfer["fromUserAccount"] == transfer["toUserAccount"]:
                        swaps.append({
                            "tokenAmount": transfer["tokenAmount"],
                            "mint": transfer["mint"]
                        })

        # Retornar los swaps encontrados
        return swaps

    except FileNotFoundError:
        print(f"El archivo {file_path} no existe.")
        return []
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON. Asegúrate de que el archivo tenga el formato correcto.")
        return []

if __name__ == "__main__":
    file_path = "transaction_details.json"  # Nombre del archivo JSON
    swaps = extract_swap_info(file_path)

    # Imprimir los resultados
    if swaps:
        print("Swaps encontrados:")
        for idx, swap in enumerate(swaps, start=1):
            print(f"Swap {idx}: Token Amount: {swap['tokenAmount']}, Mint: {swap['mint']}")
    else:
        print("No se encontraron swaps en los datos proporcionados.")
