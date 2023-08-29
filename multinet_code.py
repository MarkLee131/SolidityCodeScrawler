import os
import subprocess
import pandas as pd
import tqdm
from multiprocessing import Pool

## pip install getsourcecode
## pip install retrying

def get_bnbcode(address:str):
    code_path = '/home/kaixuan/SC-SAST/BNB_Scan/' + address
    os.makedirs(code_path, exist_ok=True)
    try:    
        res = subprocess.run(['getCode', '-n', 'bsc', '-a', address, '-o', code_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell = False)
        print(res.stdout.decode('utf-8'))
    except Exception as e:
        print(e, 'for address:', address)


def multi_get_bnbcode(address:list, poolnum:int=10):
    addr_len = len(address)
    with Pool(poolnum) as p:
        ret = list(
            tqdm.tqdm(p.imap(get_bnbcode, address), total=addr_len, desc='down bnbcode'))
        p.close()
        p.join()
    return ret
    


if __name__ == '__main__':
    # print("-"*59)
    # print("test for 0x0012365F0a1E5F30a5046c680DCB21D07b15FcF7:")
    # get_bnbcode('0x0012365F0a1E5F30a5046c680DCB21D07b15FcF7')
    
    df = pd.read_csv('/home/kaixuan/SC-SAST/BNB_Scan/BNB-OFFICIAL.csv')
    address = df.address.unique()
    multi_get_bnbcode(address, 10)