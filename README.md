# SolidityCodeScrawler
Python scripts for scrawling and extracting source code from Solidity smart contracts.

## multinet_code.py

This script is used to extract source code from smart contracts in multiple networks, including Ethereum, Binance Smart Chain, Polygon, etc.

> This tool is designed to quickly download the code of open source contracts on the blockchain explorer. 
The downloaded code maintains the file directory structure at the time of verification.


The core logic is to use the [GetCode](https://pypi.org/project/getSourceCode/) to get the source code of a smart contract. 

- :warning: Ensure that you read the [GetCode](https://pypi.org/project/getSourceCode/) documentation before using this script, since the output usually seems to be a little bit different from that was expected. :angry:

### Environment Setup

```shell
pip install getsourcecode
pip install retrying
```

## License

The code is licensed under GPL-3.0 License. See [LICENSE](./LICENSE) for details.