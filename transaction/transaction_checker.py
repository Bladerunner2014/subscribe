import requests
import json
import time


class TransactionChecker:
    def trans_info(self, txid):
        url = "https://apilist.tronscan.org/api/transaction-info?hash=" + str(txid)
        response = requests.get(url).text
        json_object = json.loads(response)

        return json_object["contractRet"]


# if __name__ == "__main__":
#     trans_info = TransactionChecker()
#     trans_info.trans_info(
#         "de5cd79c571f18648c20ab7ec0959064b719e8516ec9734f861b3a9a48101e42")
#     print(type(status))
#     print("Dst: " + address)
#     print(date)
#     print(name)
#     print(amount)
#     print("--- %s seconds ---" % (time.time() - start_time))
