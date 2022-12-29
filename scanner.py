# (c) @AbirHasan2005

import requests
from decimal import Decimal
from configs import Configs
from bs4 import BeautifulSoup


class Etherscan:
    def __init__(self, wallet: str):
        self.wallet = wallet
        self.api_key = Configs.API_KEY

    def set_wallet(self, wallet: str):
        self.wallet = wallet

    def get_wallet_balance(self):
        balance_data_api = "https://api.etherscan.io/api?" \
                           "module=account&" \
                           "action=balance&" \
                           f"address={self.wallet}&" \
                           "tag=latest&" \
                           f"apikey={self.api_key}"
        rate_data_api = "https://api.etherscan.io/api?" \
                        "module=stats&" \
                        "action=ethprice&" \
                        f"apikey={self.api_key}"
        res0 = requests.get(balance_data_api).json()
        balance = Decimal(res0.get("result", "0")) / 1000000000000000000
        res1 = requests.get(rate_data_api).json()
        rate = Decimal(res1.get("result", {}).get("ethusd", "0"))
        ether_balance = f"{balance}"
        ether_value = f"${'{:.2f}'.format(balance*rate)} (@ ${rate.__float__():,}/ETH)"
        return ether_balance, ether_value

    def _get_wallet_balance(self):
        session = requests.Session()
        session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                                        "AppleWebKit/537.36 (KHTML, like Gecko) " \
                                        "Chrome/108.0.0.0 " \
                                        "Safari/537.36"
        res = session.get(f"https://etherscan.io/address/{self.wallet}")
        soup = BeautifulSoup(res.content, "lxml")
        balance_divs = soup.find_all("div", attrs={"class": "row align-items-center"})
        data = [str(balance_div.text).strip() for balance_div in balance_divs]
        ether_balance = str(data[0].split("Balance:\n", 1)[-1].split(" ", 1)[0])
        ether_value = str(data[1].split("EtherValue:\n", 1)[-1]).strip()
        return ether_balance, ether_value
