from service.bc_model import BCModel


class Products(BCModel):

    def get_products(self, param):
        resp = self.get_method(uri='/v3/catalog/products', param=param)
        if resp is False:
            result = {"code": "201", "data": {}}
        else:
            result = {"code": "200", "data": resp}

        return result
