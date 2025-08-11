
import os
from typing import Type, TypeVar, Dict, Any
from pydantic import BaseModel
import math

T = TypeVar('T', bound=BaseModel)

def convert_camel_to_snake(d):
    """
    将字典中属性名称，从驼峰命名改成下划线命名，首位大写字母前添加下划线， 连续大写字母前添加下划线， 全部字母改成小写
    如果出现空格，空格替换为下划线
    :param d:
    :return:
    """
    # clone keys of d
    keys = list(d.keys())
    for key in keys:
        new_key = key[0].lower()
        for i in range(1, len(key)):
            if key[i] == ' ':
                new_key += '_'
                continue
            pre_is_upper = key[i - 1].isupper()
            if key[i].isupper():
                if not pre_is_upper:
                    new_key += '_'
            new_key += key[i].lower()
        d[new_key] = d.pop(key)
                
def convert_list_dict_camel_to_snake(d):
    """
    将列表中字典的属性名称，从驼峰命名改成下划线命名，首位大写字母前添加下划线， 连续大写字母前添加下划线， 全部字母改成小写
    如果出现空格，空格替换为下划线
    :param d:
    :return:
    """
    for item in d:
        convert_camel_to_snake(item)


def to_model(data: Dict[str, Any], model: Type[T]) -> T:
    """
    将字典转换为 Pydantic 模型
    :param data: 字典数据
    :param model: Pydantic 模型类
    :return: Pydantic 模型实例
    """
    # 处理 nan 值，设置为 None
    for key, value in data.items():
        try:
            if isinstance(value, float) and math.isnan(value):
                data[key] = None
        except (TypeError, ValueError):
            # 如果值不是数值类型，跳过 NaN 检查
            pass
    return model(**data)