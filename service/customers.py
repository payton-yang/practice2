from service.bc_model import BCModel


class Customers(BCModel):
    def post_customers(self, data: list):
        resp = self.post_method('/v3/customers', data)
        if resp is False:
            result = False
        else:
            result = resp

        return result

    def get_customer(self, email):
        resp = self.get_method('/v3/customers', {'email:in': email})
        if resp is False:
            result = False
        else:
            result = resp

        return result
