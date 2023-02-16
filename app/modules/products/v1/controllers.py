from flask import request
from flask_restful import Resource, marshal

from mongoengine import NotUniqueError

from app.utils import merge_attrs
from app.decorators import validate_data

from app.modules.carts.repositories import CartRepository
from app.modules.products.repositories import ProductRepository

from app.modules.products.v1.serializers import ProductsSerializers, ProductSerializers


class Products(Resource):
    @validate_data(ProductsSerializers.input_data())
    def post(self, cart_id):
        try:
            cart = CartRepository.find_one(id=cart_id)

            if not cart:
                return {"errors": "Cart not found"}, 404

            ProductRepository(**merge_attrs(request.data, {
                "cart": cart})).save()

            products = ProductRepository.find(cart=cart.id)

        except Exception as e:
            if isinstance(e, NotUniqueError):
                return {"errors": "Product already added"}, 409

        return marshal({"id": cart.id, "products": products}, ProductsSerializers.output_data()), 201

class Product(Resource):
    @validate_data(ProductSerializers.input_data())
    def patch(self, cart_id, product_id):
        product = ProductRepository.find_one(cart=cart_id, id=product_id)

        if not product:
            return {"errors": "Product not found"}, 404

        product.update(**request.data)

        return None, 204

    def delete(self, cart_id, product_id):
        product = ProductRepository.find_one(cart=cart_id, id=product_id)

        if not product:
            return {"errors": "Product not found"}, 404

        product.delete()

        return None, 204
