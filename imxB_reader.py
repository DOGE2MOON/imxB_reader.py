import time
import datetime
import json
import os
from web3 import Web3
import sys
import pandas as pd

chains = {
	'Ethereum': ['https://rpc.ankr.com/eth', '0x8C3736e2FE63cc2cD89Ee228D9dBcAb6CE5B767B'],
	'Polygon': ['https://rpc.ankr.com/polygon', '0xBB92270716C8c424849F17cCc12F4F24AD4064D6', '0x7F7AD5b16c97Aa9C2B0447C2676ce7D5CEFEbCd3'],
	'Arbitrum': ['https://arb1.arbitrum.io/rpc', '0x8C3736e2FE63cc2cD89Ee228D9dBcAb6CE5B767B', '0x9708E0B216a88D38d469B255cE78c1369ad898e6'],
	'Avalanche': ['https://api.avax.network/ext/bc/C/rpc', '0x8C3736e2FE63cc2cD89Ee228D9dBcAb6CE5B767B'],
	'Fantom': ['https://rpc.ftm.tools/', '0x60aE5F446AE1575534A5F234D6EC743215624556'],
	'Moonriver': ['https://rpc.moonriver.moonbeam.network', '0x8C3736e2FE63cc2cD89Ee228D9dBcAb6CE5B767B']
	}

imxB_abi = json.loads('[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"interestAccumulated","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"borrowIndex","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"totalBorrows","type":"uint256"}],"name":"AccrueInterest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":true,"internalType":"address","name":"borrower","type":"address"},{"indexed":true,"internalType":"address","name":"receiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"borrowAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"repayAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"accountBorrowsPrior","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"accountBorrows","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"totalBorrows","type":"uint256"}],"name":"Borrow","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"BorrowApproval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"borrowRate","type":"uint256"}],"name":"CalculateBorrowRate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"kinkRate","type":"uint256"}],"name":"CalculateKink","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"kinkBorrowRate","type":"uint256"}],"name":"CalculateKinkBorrowRate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":true,"internalType":"address","name":"borrower","type":"address"},{"indexed":true,"internalType":"address","name":"liquidator","type":"address"},{"indexed":false,"internalType":"uint256","name":"seizeTokens","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"repayAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"accountBorrowsPrior","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"accountBorrows","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"totalBorrows","type":"uint256"}],"name":"Liquidate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":true,"internalType":"address","name":"minter","type":"address"},{"indexed":false,"internalType":"uint256","name":"mintAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"mintTokens","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"newAdjustSpeed","type":"uint256"}],"name":"NewAdjustSpeed","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newBorrowTracker","type":"address"}],"name":"NewBorrowTracker","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"newKinkUtilizationRate","type":"uint256"}],"name":"NewKinkUtilizationRate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"newReserveFactor","type":"uint256"}],"name":"NewReserveFactor","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":true,"internalType":"address","name":"redeemer","type":"address"},{"indexed":false,"internalType":"uint256","name":"redeemAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"redeemTokens","type":"uint256"}],"name":"Redeem","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"totalBalance","type":"uint256"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"ADJUST_SPEED_MAX","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"ADJUST_SPEED_MIN","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"BORROW_FEE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"BORROW_PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"KINK_BORROW_RATE_MAX","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"KINK_BORROW_RATE_MIN","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"KINK_MULTIPLIER","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"KINK_UR_MAX","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"KINK_UR_MIN","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"RESERVE_FACTOR_MAX","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"address","name":"_underlying","type":"address"},{"internalType":"address","name":"_collateral","type":"address"}],"name":"_initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"newAdjustSpeed","type":"uint256"}],"name":"_setAdjustSpeed","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newBorrowTracker","type":"address"}],"name":"_setBorrowTracker","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"_setFactory","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"newKinkUtilizationRate","type":"uint256"}],"name":"_setKinkUtilizationRate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"newReserveFactor","type":"uint256"}],"name":"_setReserveFactor","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"accrualTimestamp","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"accrueInterest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"adjustSpeed","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"borrower","type":"address"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"uint256","name":"borrowAmount","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"borrow","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"borrowAllowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"borrowApprove","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"borrower","type":"address"}],"name":"borrowBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"borrowIndex","outputs":[{"internalType":"uint112","name":"","type":"uint112"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"borrowPermit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"borrowRate","outputs":[{"internalType":"uint48","name":"","type":"uint48"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"borrowTracker","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"collateral","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"exchangeRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"exchangeRateLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getBlockTimestamp","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"kinkBorrowRate","outputs":[{"internalType":"uint48","name":"","type":"uint48"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"kinkUtilizationRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"borrower","type":"address"},{"internalType":"address","name":"liquidator","type":"address"}],"name":"liquidate","outputs":[{"internalType":"uint256","name":"seizeTokens","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"minter","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"mintTokens","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"rateUpdateTimestamp","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"redeemer","type":"address"}],"name":"redeem","outputs":[{"internalType":"uint256","name":"redeemAmount","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"reserveFactor","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalBorrows","outputs":[{"internalType":"uint112","name":"","type":"uint112"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"borrower","type":"address"}],"name":"trackBorrow","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"underlying","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}]')
erc20_abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_upgradedAddress","type":"address"}],"name":"deprecate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"deprecated","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_evilUser","type":"address"}],"name":"addBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"upgradedAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"maximumFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_maker","type":"address"}],"name":"getBlackListStatus","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowed","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newBasisPoints","type":"uint256"},{"name":"newMaxFee","type":"uint256"}],"name":"setParams","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"issue","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"redeem","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"basisPointsRate","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"isBlackListed","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_clearedUser","type":"address"}],"name":"removeBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"MAX_UINT","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_blackListedUser","type":"address"}],"name":"destroyBlackFunds","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_initialSupply","type":"uint256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Issue","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Redeem","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"newAddress","type":"address"}],"name":"Deprecate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"feeBasisPoints","type":"uint256"},{"indexed":false,"name":"maxFee","type":"uint256"}],"name":"Params","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_blackListedUser","type":"address"},{"indexed":false,"name":"_balance","type":"uint256"}],"name":"DestroyedBlackFunds","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"AddedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"RemovedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"}]')
payload = pd.DataFrame()

def read_imxB(chain, imxB_address):
	chain = str(chain)
	web3 = Web3(Web3.HTTPProvider(chains['Arbitrum'][0]))
	imxB_address = Web3.toChecksumAddress(imxB_address)
	contract = web3.eth.contract(address=imxB_address, abi=imxB_abi)

	ADJUST_SPEED_MAX = contract.functions.ADJUST_SPEED_MAX().call()
	payload.at['Value','ADJUST_SPEED_MAX'] = ADJUST_SPEED_MAX
	ADJUST_SPEED_MIN = contract.functions.ADJUST_SPEED_MIN().call()
	payload['ADJUST_SPEED_MIN'] = ADJUST_SPEED_MIN
	BORROW_FEE = contract.functions.BORROW_FEE().call()
	payload['BORROW_FEE'] = BORROW_FEE
	BORROW_PERMIT_TYPEHASH = contract.functions.BORROW_PERMIT_TYPEHASH().call()
	payload['BORROW_PERMIT_TYPEHASH'] = BORROW_PERMIT_TYPEHASH
	DOMAIN_SEPARATOR = contract.functions.DOMAIN_SEPARATOR().call()
	payload['DOMAIN_SEPARATOR'] = DOMAIN_SEPARATOR
	KINK_BORROW_RATE_MAX = contract.functions.KINK_BORROW_RATE_MAX().call()
	payload['KINK_BORROW_RATE_MAX'] = KINK_BORROW_RATE_MAX
	KINK_BORROW_RATE_MIN = contract.functions.KINK_BORROW_RATE_MIN().call()
	payload['KINK_BORROW_RATE_MIN'] = KINK_BORROW_RATE_MIN
	KINK_MULTIPLIER = contract.functions.KINK_MULTIPLIER().call()
	payload['KINK_MULTIPLIER'] = KINK_MULTIPLIER
	KINK_UR_MAX = contract.functions.KINK_UR_MAX().call()
	payload['KINK_UR_MAX'] = KINK_UR_MAX
	KINK_UR_MIN = contract.functions.KINK_UR_MIN().call()
	payload['KINK_UR_MIN'] = KINK_UR_MIN
	MINIMUM_LIQUIDITY = contract.functions.MINIMUM_LIQUIDITY().call()
	payload['MINIMUM_LIQUIDITY'] = MINIMUM_LIQUIDITY
	PERMIT_TYPEHASH = contract.functions.PERMIT_TYPEHASH().call()
	payload['PERMIT_TYPEHASH'] = PERMIT_TYPEHASH
	RESERVE_FACTOR_MAX = contract.functions.RESERVE_FACTOR_MAX().call()
	payload['RESERVE_FACTOR_MAX'] = RESERVE_FACTOR_MAX
	accrualTimestamp = contract.functions.accrualTimestamp().call()
	payload['accrualTimestamp'] = accrualTimestamp
	adjustSpeed = contract.functions.adjustSpeed().call()
	payload['adjustSpeed'] = adjustSpeed
	borrowIndex = contract.functions.borrowIndex().call()
	payload['borrowIndex'] = borrowIndex
	borrowRate = contract.functions.borrowRate().call()
	payload['borrowRate'] = borrowRate
	borrowTracker = contract.functions.borrowTracker().call()
	payload['borrowTracker'] = borrowTracker
	collateral = contract.functions.collateral().call()
	payload['collateral'] = collateral
	decimals = contract.functions.decimals().call()
	payload['decimals'] = decimals
	exchangeRateLast = contract.functions.exchangeRateLast().call()
	payload['exchangeRateLast'] = exchangeRateLast
	factory = contract.functions.factory().call()
	payload['factory'] = factory
	getBlockTimestamp = contract.functions.getBlockTimestamp().call()
	payload['getBlockTimestamp'] = getBlockTimestamp
	kinkBorrowRate = contract.functions.kinkBorrowRate().call()
	payload['kinkBorrowRate'] = kinkBorrowRate
	kinkUtilizationRate = contract.functions.kinkUtilizationRate().call()
	payload['kinkUtilizationRate'] = kinkUtilizationRate
	name = contract.functions.name().call()
	payload['name'] = name
	rateUpdateTimestamp = contract.functions.rateUpdateTimestamp().call()
	payload['rateUpdateTimestamp'] = rateUpdateTimestamp
	reserveFactor = contract.functions.reserveFactor().call()
	payload['reserveFactor'] = reserveFactor
	#symbol = contract.functions.symbol().call() -> left out so that true symbol can be fetched
	#payload['symbol'] = symbol
	totalBalance = contract.functions.totalBalance().call()
	payload['totalBalance'] = totalBalance
	totalBorrows = contract.functions.totalBorrows().call()
	payload['totalBorrows'] = totalBorrows
	totalSupply = contract.functions.totalSupply().call()
	payload['totalSupply'] = totalSupply
	underlying = contract.functions.underlying().call()
	payload['underlying'] = underlying
	underlying_contract = web3.eth.contract(address=Web3.toChecksumAddress(underlying), abi=erc20_abi)
	symbol = underlying_contract.functions.symbol().call()
	payload['symbol'] = symbol

	final = payload.T
	final.to_csv(chain + " " + str(symbol) + " imxB" + ".csv", encoding='utf-8')
