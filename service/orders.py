# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :practice2
# @File     :orders
# @Date     :2021/1/17 23:05
# @Author   :杨宏伟
# @Email    :yhw17@qq.com
# @Software :PyCharm
-------------------------------------------------
"""
from service.bc_model import BCModel


class Orders(BCModel):
    def post_order(self, data: dict):
        resp = self.post_method('/v2/orders', data)
        if resp is False:
            result = False
        else:
            result = resp

        return result
