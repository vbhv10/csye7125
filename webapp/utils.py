# Rest framework imports
from fastapi.responses import JSONResponse, Response
from fastapi import status as st

from logging.config import dictConfig
import logging
from log import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("cloud")


def response(message: str, status_code: int , data=None, headers=None, log_level="error", no_content=False):
    """
    Customize the response for better information delivery.

    :param status: True if the response if for successful api response else False
    :param message: String message to give details
    :param status_code: states code of the response
    :param data: send data if any
    :param headers: provide headers in the response
    :return: Response class object
    """
    if headers is None:
        headers = {
            "cache-control": "no-cache"
        }

    
    if log_level == 'error':
        logger.error(message + " {}".format(status_code))
    else:
        logger.info(message + " {}".format(status_code))
    message = message if type(message) in [dict, list] else {"message":message}


    if status_code == st.HTTP_204_NO_CONTENT or no_content:
        return Response(status_code=status_code, headers=headers, media_type="application/json")
    return JSONResponse(content=data, status_code=status_code, headers=headers, media_type="application/json")