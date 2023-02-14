from constants.status_code import StatusCode
from http_handler.response_handler import ResponseHandler
from http_handler.request_handler import RequestHandler
from constants.error_message import ErrorMessage
import logging
from constants.info_message import InfoMessage
from dotenv import dotenv_values
import requests
import json


# to handle the routes
class SubscribeManager:
    def __init__(self):
        self.config = dotenv_values(".env")
        self.logger = logging.getLogger(__name__)
        self.req = RequestHandler()

    # insert new investor to the database
    def handle_investor(self, user_id: str, dt: dict):
        try:
            transaction_status = self.transaction_checker(dt["transaction_id"])
        except Exception as error:
            self.logger.error(ErrorMessage.TRANS_ID)
            self.logger.error(error)
            raise Exception

        res = ResponseHandler()
        try:
            request_json = self.req.create_json_from_args(user_id=user_id,
                                                          secret_key=dt["secret_key"],
                                                          sub_level=dt["sub_level"], expire_date=dt["expire_date"],
                                                          api_key=dt["api_key"])
        except Exception as error:
            self.logger.error(ErrorMessage.INV_INSERT)
            self.logger.error(error)
            raise Exception

        if transaction_status:
            self.req.send_post_request(base_url=self.config["INVESTOR_BASE_URL"],
                                       end_point=self.config["INVESTOR_POST_URL"],
                                       port=self.config["INVESTOR_PORT"]
                                       ,
                                       body=request_json,
                                       timeout=self.config["INVESTOR_TIMEOUT"], error_log_dict={"message": ErrorMessage.INV_INSERT})
            res.set_status_code(StatusCode.SUCCESS)
            res.set_response({"message": InfoMessage.INV_SUCCESS})

        else:
            res.set_status_code(StatusCode.BAD_REQUEST)
            res.set_response({"message": ErrorMessage.BAD_REQUEST})
        # try:
        #     self.dao.insert_new_investor(investor)
        # except Exception as error:
        #     self.logger.error(ErrorMessage.INV_INSERT)
        #     self.logger.error(error)
        #     raise Exception
        return res

    @staticmethod
    def transaction_checker(txid):
        url = "https://apilist.tronscan.org/api/transaction-info?hash=" + str(txid)
        response = requests.get(url).text
        json_object = json.loads(response)

        return json_object["contractRet"]