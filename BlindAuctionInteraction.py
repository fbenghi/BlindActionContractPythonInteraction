"""
Links úteis
	Smart Contract do BlindAuction
		https://docs.soliditylang.org/en/v0.5.3/solidity-by-example.html#id2
	
	Lendo json de arquivo (usado para carregar o ABI)
		https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/

	Conversão de variáveis para ABI
		https://eth-abi.readthedocs.io/en/latest/encoding.html
	
	Funções de Hash
		https://web3py.readthedocs.io/en/stable/web3.main.html?highlight=soliditySha3#cryptographic-hashing

	Interagindo com funções de contrato
		https://hackernoon.com/ethereum-smart-contracts-in-python-a-comprehensive-ish-guide-771b03990988
"""

#%%
from web3 import Web3

#%%
# Conectar com o ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

#%%
# Carregar ABI
import json
with open('/home/felipe/Documents/Ethereum/Scripts/Remix-Ide/Contracts/artifacts/BlindAuction.json') as json_file:
    contractData = json.load(json_file)

# Endereço do contrato
contractAddress = '0xf28250691Cb78e2744EE181bd508F6d03aF4b9E4'

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
print("calculado pelo smart contract:", hashSmartContract)
print("calculado pelo python:", hashSmartPython)



# %%
#faz oferta 1 - Gera dicionário de parâmetros, assina e envia
from eth_abi.packed import encode_abi_packed

#dados da conta
fromAccount = w3.eth.accounts[3]
private_key = Web3.toBytes(hexstr='0x8415e94b6ad63bdd82d6acf616e418785bd0fde344363fba1dd1b6e30dd72dcf')
nonce = w3.eth.getTransactionCount(fromAccount)

#Dados da oferta
actionBidding = [1, False, b'0x8CF9']
encoded = encode_abi_packed(['uint256', 'bool', 'bytes32'], actionBidding)
hashBid = Web3.toHex(Web3.sha3(encoded))

#cria parametros da transacao
result = contract.functions.bid(hashBid).buildTransaction({
        'nonce': nonce,
		'value': w3.toWei(3, 'ether'),
    })

#assina
signed_txn = w3.eth.account.sign_transaction(result, private_key=private_key)	
#envia
txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

#%%
#faz oferta 2 - envia a transação numa etapa somente
from eth_abi.packed import encode_abi_packed

#Dados da oferta
actionBidding = [w3.toWei(20, 'ether'), True, b'0x8CF9']
encoded = encode_abi_packed(['uint256', 'bool', 'bytes32'], actionBidding)
hashBid = Web3.toHex(Web3.sha3(encoded))

#envia transação
resultTransact = contract.functions.bid(hashBid).transact({
		'value': w3.toWei(20, 'ether'),
		'from': w3.eth.accounts[5],
    })

#%%
tx_receipt = w3.eth.getTransactionReceipt(resultTransact)
contract.events.AddedBidding().processReceipt(tx_receipt)


#%%
_values = [10,10,10,10,10,w3.toWei(15, 'ether'),w3.toWei(20, 'ether')]
_fake   = [False,False, False,True,True,True,True]
_hash   = [b'0x8CF9',b'0x8CF9',b'0x8CF9',b'0x8CF9',b'0x8CF9',b'0x8CF9',b'0x8CF9']
resultTransact = contract.functions.reveal(_values,_fake,_hash).transact({
		'from': w3.eth.accounts[5],
    })

#%%
tx_receipt = w3.eth.getTransactionReceipt(resultTransact)
contract.events.RevealBidding().processReceipt(tx_receipt)



# %%
#revela a oferta

# nonce = w3.eth.getTransactionCount(fromAccount)

# revealDict = contract.functions.reveal([1],[False],[b'0x8CF9']).call()

# revealSigned = w3.eth.account.sign_transaction(revealDict, private_key=private_key)	

# %%
newTransfers = transfer_filter.get_new_entries()
newTransfers