import re
import os
import requests
import traceback
import pandas as pd
import tqdm

etherscan_base_url = "https://api.etherscan.io/api"

csv_dir = "scraping/eth2"


def is_valid_ethereum_address(address):
    return re.match('^0x[a-fA-F0-9]{40}$', address) is not None


def crawl_etherscan_code(address_list, api_key, output_dir="contracts/"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    # ver_info = pd.DataFrame(columns=["address", "version"])
    for address in tqdm.tqdm(address_list):
        try:
            payload = {
                "module": "contract",
                "action": "getsourcecode",
                "address": address,
                "apikey": api_key
            }

            if is_valid_ethereum_address(address):
                address_dir = os.path.join(output_dir, address)
                if not os.path.exists(address_dir):
                    os.makedirs(address_dir, exist_ok=True)
                else:
                    continue
                files = os.listdir(address_dir)
                if len(files) > 0:
                    print(f"Already crawled {address}, skip...")
                    continue
                else:
                    response = requests.get(etherscan_base_url, params=payload)
                    response_json = response.json()

                    if response_json["status"] == "1":
                        contract_info = response_json["result"][0]
                        contract_name = contract_info["ContractName"]
                        source_code = contract_info["SourceCode"]
                        version = contract_info["CompilerVersion"]
                        # ver_info = pd.concat([ver_info, pd.DataFrame({"address": [address], "version": [version]})], axis=0)
                        # Save the source code to a file
                        file_name = f"{contract_name}.sol"
                        file_path = os.path.join(address_dir, file_name)
                        with open(file_path, "w", encoding='utf-8') as f:
                            f.write(source_code)
                    else:    
                        print(f"Error for address {address}: {response_json['message']}")
            else:
                print(f"Invalid address {address}, skip...")
        except Exception as e:
            traceback.print_exc()
    # ver_info.to_csv(os.path.join(csv_dir, "version_info.csv"), index=False)

if __name__ == "__main__":
    df = pd.read_csv('top5000_address.csv')
    address_list = [row['address'] for index, row in df.iterrows() if row['chain'] == 'eth']
    crawl_etherscan_code(address_list)