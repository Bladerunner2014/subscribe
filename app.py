import logging
from flask import Flask, request
from dotenv import dotenv_values
from constants.status_code import StatusCode
from constants.info_message import InfoMessage
from blueprint import v1_blueprint
from constants.error_message import ErrorMessage
from managers.sub_manager import SubscribeManager
from swagger import swagger
from log import log

app = Flask("subscribe")
config = dotenv_values(".env")
logger = logging.getLogger(__name__)


# To send information of an investor and store it to the database
@v1_blueprint.route('/subscribe', methods=['POST'])
def subscriber_info():
    request_data = request.get_json()
    user_id = request.headers.get('user_id')

    if not user_id:
        return logger.error(ErrorMessage.BAD_REQUEST), StatusCode.BAD_REQUEST

    sub_manager = SubscribeManager()
    res = sub_manager.handle_investor(user_id, dt=request_data)
    if res:
        logger.info(InfoMessage.INV_SUCCESS)
    return res.generate_response()


swagger.run_swagger(app)
log.setup_logger()

app.register_blueprint(v1_blueprint)
app.run(host=config["HOST"], port=config["PORT"], debug=config["DEBUG"])
