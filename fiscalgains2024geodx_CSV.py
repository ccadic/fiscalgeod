import requests
import csv
from datetime import datetime

wallet_address = "0xc75F7A42D3AA8517f51ebD33b9F5aB4F07A87d85"
token_contract = "0xAC0F66379A6d7801D7726d5a943356A172549Adb"
api_key = "KRNZ17DGEFVPR"

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

def get_transactions():
    url = "https://api.polygonscan.com/api"
    params = {
        "module": "account",
        "action": "tokentx",
        "address": wallet_address,
        "contractaddress": token_contract,
        "page": 1,
        "offset": 10000,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "1":
        print("Erreur Polygonscan:", data.get("message", "inconnue"))
        return []

    return data["result"]

def calculate_total_received_and_export(tx_list):
    total = 0
    rows = []

    for tx in tx_list:
        if tx["to"].lower() == wallet_address.lower():
            timestamp = datetime.fromtimestamp(int(tx["timeStamp"]))
            if start_date <= timestamp <= end_date:
                amount = int(tx["value"]) / (10 ** int(tx["tokenDecimal"]))
                total += amount
                rows.append([
                    timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    f"{amount:.6f}",
                    tx["hash"]
                ])

    # Écriture CSV
    with open("gains_geod_2024.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Montant GEOD", "Transaction Hash"])
        writer.writerows(rows)

    return total

tx_list = get_transactions()
total_received = calculate_total_received_and_export(tx_list)

print(f"\n✅ Total de GEOD reçus sur 2024 : {total_received:.6f} GEOD")
print("📁 Export CSV : gains_geod_2024.csv généré avec succès.")
