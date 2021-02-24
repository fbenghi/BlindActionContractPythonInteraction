"""
https://docs.soliditylang.org/en/v0.5.3/solidity-by-example.html#id2
"""

### no terminal: ganache-cli 
### para lançar a test net

#%%
#conectar com o ganache
from web3 import Web3, utils
# web3.py instance
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))



# %%
from eth_abi import encode_single, encode_abi
# hash = Web3.soliditySha3(['uint256', 'uint256', 'uint256'], [1 ,2, 3]), 16)
# keccak256(abi.encodePacked(value, fake, secret)))
actionBidding =  [10,False, 0]

encoded =  encode_abi(['uint', 'bool', 'bytes32'], utils.randomHex(32))


# %%
