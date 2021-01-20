from service.bc_model import BCModel


class Products(BCModel):

    def get_products(self, param):
        resp = self.get_method(uri='/v3/catalog/products', param=param)
        if resp is False:
            result = False
        else:
            result = resp

        return result
