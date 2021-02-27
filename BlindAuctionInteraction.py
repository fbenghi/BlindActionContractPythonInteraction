"""
Links úteis
	Smart Contract do BlindAuction
		https://docs.soliditylang.org/en/v0.5.3/solidity-by-example.html#id2
	
	Lendo json de arquivo (usado para carregar o ABI)
		https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/

	Conversão de variáveis para ABI
		https://eth-abi.readthedocs.io/en/latest/encoding.html
	
	Funções de Hash
"""

#%%
from web3 import Web3

#%%
# Conectar com o ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

#%%
# Carregar ABI
import json
with open('artifacts/BlindAuction.json') as json_file:
    contractData = json.load(json_file)

# Endereço do contrato
contractAddress = '0xADCaf36ed48c30844938cB789D4D6318A86a44B5'

#%%
# Interagir com um contrato 
contract = w3.eth.contract(address = contractAddress, abi = contractData["abi"])


#%%
# Garantir que consigo calcular o hash do mesmo jeito que o contrato

# Chamar uma função que calula o hash da oferta NO CONTRATO
hashSmartContract = Web3.toHex(contract.functions.testHash(500,False).call())

# Reproduz o mesmo cálculo no contrato
from eth_abi.packed import encode_abi_packed
actionBidding = [500, False]
encoded = encode_abi_packed(['uint256', 'bool'], actionBidding)
hashSmartPython = Web3.toHex(Web3.sha3(encoded))

"""
	As seguintes funções não retornam o mesmo que o contrato porque encode_abi_packed usa
	non-standard packed encoding. Em que não são respeitados os tamanhos (número de bytes) 
	das variáveis:

	Web3.soliditySha3(['uint8', 'bool'], actionBidding)
	Web3.solidityKeccak(['uint8', 'bool'], actionBidding)
"""




# %%
