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

    def update_pwd(self, data):
        resp = self.put_method('/v3/customers', data)
        if resp is False:
            result = False
        else:
            result = resp

        return result

    def validate_pwd(self, customer_id, data):
        resp = self.post_method(f'/v2/customers/{customer_id}/validate', data)
        if resp is False:
            result = False
        else:
            result = resp
        return resp
