from web3 import Web3
import json

TOKENS = {
    'SOKU': '0x0e4B5Ea0259eB3D66E6FCB7Cc8785817F8490a53',
    'CADINU': '0x748eD23b57726617069823Dc1E6267C8302d4E76',
    'TKO': '0x9f589e3eabe42ebC94A44727b3f3531C0c877809',
    'QANX': '0xAAA7A10a8ee237ea61E8AC46C50A8Db8bCC1baaa',
}
URL = 'https://bsc-dataseed1.binance.org'
pancakeSwapRouterContract = "0x10ED43C718714eb63d5aA57B78B54704E256024E"
BNBTokenAddress = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"
USDTokenAddress  = "0x55d398326f99059fF775485246999027B3197955"
with open('token_abi.json', 'r') as f:
    tokenABI = json.load(f)
with open('pancake_abi.json', 'r') as f:
    pancakeSwapABI = json.load(f)


def getBNBPrice(provider: Web3) -> float:
    bnbToSell = provider.toWei("1", "ether")
    router = provider.eth.contract(address=pancakeSwapRouterContract, abi=pancakeSwapABI)
    amountOut = router.functions.getAmountsOut(bnbToSell, [BNBTokenAddress, USDTokenAddress]).call()
    amountOut = provider.fromWei(amountOut[1], 'ether')
    return amountOut


def getTokenPrice(provider: Web3, tokenAddress: str, tokensToSell: int) -> float:
    tokenRouter = provider.eth.contract(address=tokenAddress, abi=tokenABI)
    tokenDecimals = tokenRouter.functions.decimals().call()
    tokensToSell = int(str(tokensToSell).ljust(tokenDecimals + len(str(tokensToSell)), '0'))

    router = provider.eth.contract(address=pancakeSwapRouterContract, abi=pancakeSwapABI)
    amountOut = router.functions.getAmountsOut(tokensToSell, [tokenAddress, BNBTokenAddress]).call()
    amountOut = provider.fromWei(amountOut[1], 'ether')
    return amountOut


if __name__ == '__main__':
    w3 = Web3(Web3.HTTPProvider(URL))
    if w3.isConnected():
        bnbPrice = getBNBPrice(provider=w3)
        print(f'CURRENT BNB PRICE: {bnbPrice}')
        for name, address in TOKENS.items():
            tokensToSell = 1
            priceInBNB = getTokenPrice(provider=w3, tokenAddress=address, tokensToSell=tokensToSell) / tokensToSell
            priceInUSDT = priceInBNB * bnbPrice
            print(f'{name} VALUE IN BNB: {priceInBNB} | IN USDT: {priceInUSDT}')


