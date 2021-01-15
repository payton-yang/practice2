from service.bc_model import BCModel


class Addresses(BCModel):
    def get_customer_addresses(self, customer_id):
        resp = self.get_method(uri='/v3/customers/addresses', param={'customer_id:in': customer_id})
        if resp is False:
            result = False
        else:
            result = resp

        return result

    def add_address(self, data):
        resp = self.post_method(uri='/v3/customers/addresses', data=data)
        if resp is False:
            result = False
        else:
            result = resp

        return result
