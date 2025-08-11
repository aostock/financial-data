from typing import Any, Optional, TypeVar, Generic
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
import math

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    code: int = Field(default=0, description="Status code, 0 for success, 1 for error")
    data: Optional[T] = Field(default=None, description="Data field, None for no data")
    msg: Optional[str] = Field(default="", description="Message field")


def handle_nan_values(data):
    """Recursively handle NaN values in data structures"""
    if isinstance(data, dict):
        return {key: handle_nan_values(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [handle_nan_values(item) for item in data]
    elif isinstance(data, float) and math.isnan(data):
        return None
    elif hasattr(data, 'model_dump'):  # Pydantic model
        model_data = data.model_dump()
        return handle_nan_values(model_data)
    else:
        return data


def success(data)->BaseResponse:
    """
    :param data:
    :return:
    """
    # Handle NaN values before returning the response
    clean_data = handle_nan_values(data)
    return BaseResponse(code=0, data=clean_data)

def error(msg, code=1)->JSONResponse:
    """
    :param msg:
    :param code:
    :return:
    """
    if isinstance(msg, Exception):
        msg = str(msg)
    return BaseResponse(code=code, msg=msg)


async def exception_handler(request: Request, e: Exception) -> JSONResponse:
    """
    异常处理函数
    :param request: 请求对象
    :param e: 异常对象
    :return: JSONResponse 对象
    """
    return error(msg=str(e))

