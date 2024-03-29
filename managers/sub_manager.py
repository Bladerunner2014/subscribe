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
    def handle_investor(self, user_id, dt: dict):
        res = ResponseHandler()
        transaction_status = self.transaction_checker(dt["transaction_id"])
        if not transaction_status:
            self.logger.error(ErrorMessage.TRANS_ID)
            res.set_status_code(StatusCode.TRANSACTION)
            res.set_response({"message": ErrorMessage.TRANS_ID})
            return res

        request_json = self.req.create_json_from_args(
            secret_key=dt["secret_key"],
            sub_level=dt["sub_level"], expire_date=dt["expire_date"],
            api_key=dt["api_key"],
            exchange=dt["exchange"])
        if transaction_status["contractRet"] != InfoMessage.TRANSACTION_SUCCESS:
            self.logger.error(ErrorMessage.TRANS_ID)
            res.set_status_code(StatusCode.TRANSACTION)
            res.set_response({"message": ErrorMessage.TRANS_ID})
            return res

        try:

            result, status = self.req.send_post_request(base_url=self.config["INVESTOR_BASE_URL"],
                                                        end_point=self.config["INVESTOR_POST_URL"],
                                                        port=self.config["INVESTOR_PORT"]
                                                        , headers={"user_id": user_id},
                                                        body=request_json,
                                                        timeout=self.config["INVESTOR_TIMEOUT"],
                                                        error_log_dict={"message": ErrorMessage.INV_INSERT})


        except Exception as error:
            self.logger.error(ErrorMessage.INV_INSERT)
            self.logger.error(error)

            raise Exception
        res.set_response(result)
        res.set_status_code(status)
        return res

    def subscription_info(self, user_id):
        result, status = self.req.send_get_request(base_url=self.config["INVESTOR_BASE_URL"],
                                                   end_point=self.config["INVESTOR_GET_URL"],
                                                   port=self.config["INVESTOR_PORT"],
                                                   headers={"user_id": user_id},
                                                   timeout=self.config["INVESTOR_TIMEOUT"],
                                                   error_log_dict={"message": ErrorMessage.INV_ERROR})

        if status != StatusCode.SUCCESS:
            return result, status

        result = json.loads(result)
        not_json = {"sub_level": result["sub_level"], "expire_date": result["expire_date"]}
        result = json.dumps(not_json)
        return result, status

    @staticmethod
    def transaction_checker(txid):
        url = "https://apilist.tronscan.org/api/transaction-info?hash=" + str(txid)

        response = requests.get(url).text
        json_object = json.loads(response)
        return json_object
