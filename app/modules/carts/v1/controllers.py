from flask import request
from flask_restful import Resource, marshal

from app.utils import merge_attrs
from app.decorators import validate_data
from app.external_services import ProductServices

from app.modules.carts.repositories import CartRepository
from app.modules.products.repositories import ProductRepository

from app.modules.carts.v1.serializers import CartSerializers


class Cart(Resource):
    def get(self, cart_id):
        cart = CartRepository.find_one(id=cart_id)

        if not cart:
            return {"errors": "Cart not found"}, 404

        cart.products = ProductServices.retrieve_products(
            ProductRepository.find(cart=cart_id))

        cart.total = sum(product["price"] * product["amount"] for product in cart.products)

        if cart.discount_coupon:
            cart.discount = cart.discount_coupon.discount
            cart.subtotal = cart.total - (
                cart.discount.value * cart.total / 100 if cart.discount.type == "percentage" else cart.discount.value
            )

        return marshal(cart, CartSerializers.output_data(complete_resource=True)), 200

    @validate_data(CartSerializers.input_data())
    def post(self):
        product = ProductRepository(
            **merge_attrs(request.data, {"cart": CartRepository().save()})).save()

        return marshal({"id": product.cart.id, "products": [product]}, CartSerializers.output_data()), 201

    def delete(self, cart_id):
        cart = CartRepository.find_one(id=cart_id)

        if not cart:
            return {"errors": "Cart not found"}, 404

        cart.delete()

        return None, 204
