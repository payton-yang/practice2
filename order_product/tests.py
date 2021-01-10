from django.test import TestCase

# Create your tests here.
from order_product.models import OrderProduct


class OPTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_op(self):
        product_objects_all = OrderProduct.objects.all()
        for op in product_objects_all:
            print(
                {
                    'order_id': op.order_id,
                    'product_id': op.product_id,
                    'quantity': op.quantity
                }
            )
