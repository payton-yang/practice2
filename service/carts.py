from service.bc_model import BCModel


class Carts(BCModel):
    def post_cart(self, data: dict):
        resp = self.post_method(uri='/v3/carts', data=data)
        if resp is False:
            result = False
        else:
            result = resp

        return result

    def put_cart_items(self, bc_cart_id, item_id, data: dict):
        resp = self.put_method(uri=f'/v3/carts/{bc_cart_id}/items/{item_id}', data=data)
        if resp is False:
            result = False
        else:
            result = resp

        return result

    def get_cart_items(self, bc_cart_id):
        resp = self.get_method(uri=f'/v3/carts/{bc_cart_id}', param={})
        if resp is False:
            result = False
        else:
            result = resp

        return result

    def delete_cart_items(self, bc_cart_id, item_id):
        resp = self.delete_method(uri=f'/v3/carts/{bc_cart_id}/items/{item_id}')
        if resp is False:
            result = False
        else:
            result = resp

        return result

    def add_cart_items(self, bc_cart_id, data: dict):
        resp = self.post_method(uri=f'/v3/carts/{bc_cart_id}/items', data=data)
        if resp is False:
            result = False
        else:
            result = resp

        return result
