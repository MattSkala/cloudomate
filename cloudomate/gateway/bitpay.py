import json
import urllib


def extract_info(url):
    """
    Extracts amount and BitCoin address from a BitPay URL.
    :param url: the BitPay URL like "https://bitpay.com/invoice?id=J3qU6XapEqevfSCW35zXXX"
    :return: a tuple of the amount in BitCoin along with the address
    """
    bitpay_id = url.split("=")[1]
    url = "https://bitpay.com/invoiceData/" + bitpay_id + "?poll=false"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    amount = data['invoice']['buyerTotalBtcAmount']
    address = data['invoice']['bitcoinAddress']
    return amount, address
