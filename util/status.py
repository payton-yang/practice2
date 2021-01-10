# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :practice
# @File     :status
# @Date     :2021/1/9 16:32
# @Author   :杨宏伟
# @Email    :yhw17@qq.com
# @Software :PyCharm
-------------------------------------------------
"""


def update_dict(data: dict):
    SUCCESS = {
        'code': 200,
        'message': 'success',
        'data': {}
    }
    SUCCESS.update(data=data)
    return SUCCESS


FAILURE_BAD = {
    'code': 400,
    'message': 'bad request'
}
FAILURE_NOT_EXIST = {
    'code': 404,
    'message': 'request resource does not exist'
}
