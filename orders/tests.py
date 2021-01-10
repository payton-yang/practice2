import uuid
from datetime import datetime

from django.test import TestCase

# Create your tests here.
from cart_product.models import CartProduct
from carts.models import Carts
from order_product.models import OrderProduct
from orders.models import Orders
from products.models import Products
from users.models import Users


class OrderTest(TestCase):
    def setUp(self):
        user_param = {
            'name': '111',
            'email': '11@qq.com',
            'password': '123'
        }
        user = Users.objects.create(**user_param)
        param = {
            'uuid': uuid.uuid1(),
            'create_time': datetime.now(),
            'user_id': user,
            'status': '1'
        }
        param2 = {
            'uuid': uuid.uuid1(),
            'create_time': datetime.now(),
            'user_id': user,
            'status': '2'
        }
        o1 = Orders.objects.create(**param)
        o2 = Orders.objects.create(**param2)

        product_param = {
            'name': 'cup',
            'type': '22',
            'quantity': 22,
            'color': 'red'
        }
        product_param2 = {
            'name': 'cup2',
            'type': '22',
            'quantity': 223,
            'color': 'red'
        }
        product_param3 = {
            'name': 'cup3',
            'type': '22',
            'quantity': 232,
            'color': 'red'
        }
        product_param4 = {
            'name': 'cup4',
            'type': '22',
            'quantity': 2,
            'color': 'red'
        }
        product_param5 = {
            'name': 'cup5',
            'type': '22',
            'quantity': 2332,
            'color': 'red'
        }
        p1 = Products.objects.create(**product_param)
        p2 = Products.objects.create(**product_param2)
        p3 = Products.objects.create(**product_param3)
        p4 = Products.objects.create(**product_param4)
        p5 = Products.objects.create(**product_param5)

        o_p_param1 = {
            'order_id': o1,
            'product_id': p1,
            'quantity': 15
        }
        o_p_param2 = {
            'order_id': o1,
            'product_id': p2,
            'quantity': 15

        }
        o_p_param3 = {
            'order_id': o2,
            'product_id': p3,
            'quantity': 15

        }
        o_p_param4 = {
            'order_id': o2,
            'product_id': p4,
            'quantity': 15

        }
        o_p_param5 = {
            'order_id': o2,
            'product_id': p5,
            'quantity': 15

        }
        OrderProduct.objects.create(**o_p_param1)
        OrderProduct.objects.create(**o_p_param2)
        OrderProduct.objects.create(**o_p_param3)
        OrderProduct.objects.create(**o_p_param4)
        OrderProduct.objects.create(**o_p_param5)

        c1 = Carts.objects.create(**param)

        c_p_param1 = {
            'cart_id': c1,
            'product_id': p1,
            'quantity': 15
        }
        c_p_param2 = {
            'cart_id': c1,
            'product_id': p2,
            'quantity': 16

        }
        c_p_param3 = {
            'cart_id': c1,
            'product_id': p3,
            'quantity': 17

        }
        cp1 = CartProduct.objects.create(**c_p_param1)
        cp2 = CartProduct.objects.create(**c_p_param2)
        cp3 = CartProduct.objects.create(**c_p_param3)

    def test_order(self):
        user = Users.objects.get(id=1)
        orders = Orders.objects.filter(user_id=1)
        for order in orders:
            products = OrderProduct.objects.filter(order_id=order.id)
            for product in products:
                pro = product.__str__()
                print(pro.__str__())

    def test_op(self):
        product_objects_all = OrderProduct.objects.all()
        for op in product_objects_all:
            print(
                {
                    'order_id': op.order_id_id,
                    'product_id': op.product_id_id,
                    'quantity': op.quantity
                }
            )

    def test_cp(self):
        cart = Carts.objects.get(user_id=1)
        print(cart.__str__())
        # cart_product = CartProduct.objects.filter(cart_id=1, product_id=2)
        # # print(cart_product.quantity)
        # for item in cart_product:
        #     print(item.quantity)
