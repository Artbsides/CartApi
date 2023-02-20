import unittest
import pytest

from unittest.mock import patch
from bson.objectid import ObjectId

from mongoengine.connection import _get_db

from tests.main import app

from app.modules.carts.repositories import CartRepository
from app.modules.products.repositories import ProductRepository


class TestProducts(unittest.TestCase):
    def tearDown(self):
        _get_db().drop_collection("coupons")
        _get_db().drop_collection("products")
        _get_db().drop_collection("carts")

        _get_db().create_collection("products") \
            .create_index([("product_uuid", 1), ("cart", 1)], unique=True)

    def create_cart(self, data):
        return CartRepository(**data).save()

    def create_product(self, data):
        return ProductRepository(**data).save()

    def test_post(self):
        assert app.test_client().post(f'/v1/cart/{ObjectId()}/products').status_code == 422

        response = app.test_client().post(f'/v1/cart/{ObjectId()}/products',
            json={
                "product_uuid": "c0b3fe2c-9cc9-475a-9c11-4cfaec941909",
                "price": 25,
                "amount": 2
            }
        )

        assert response.status_code == 404

        cart = self.create_cart({})

        response = app.test_client().post(f'/v1/cart/{cart.id}/products',
            json={
                "product_uuid": "c0b3fe2c-9cc9-475a-9c11-4cfaec941909",
                "price": 25,
                "amount": 2
            }
        )

        assert response.status_code == 201

        response = app.test_client().post(f'/v1/cart/{cart.id}/products',
            json={
                "product_uuid": "c0b3fe2c-9cc9-475a-9c11-4cfaec941909",
                "price": 25,
                "amount": 2
            }
        )

        assert response.status_code == 409

        with patch("app.modules.products.repositories.Product", object), pytest.raises(Exception):
            response = app.test_client().post(f'/v1/cart/{cart.id}/products',
                json={
                    "product_uuid": "c0b3fe2c-9cc9-475a-9c11-4cfaec941909",
                    "price": 25,
                    "amount": 2
                }
            )

            assert response.status_code == 500

    def test_patch(self):
        assert app.test_client().patch(f'/v1/cart/{ObjectId()}/products/{ObjectId()}').status_code == 404

        cart = self.create_cart({})

        assert app.test_client().patch(f'/v1/cart/{cart.id}/products/{ObjectId()}').status_code == 404

        product = self.create_product({
            "cart": cart,
            "product_uuid": "c0b3fe2c-9cc9-475a-9c11-4cfaec941909",
            "price": 25,
            "amount": 2
        })

        with pytest.raises(Exception):
            assert app.test_client().patch(f'/v1/cart/{cart.id}/products/{product.id}').status_code == 500

        response = app.test_client().patch(f'/v1/cart/{cart.id}/products/{product.id}',
            json={
                "amount": 2,
                "price": 25.50
            }
        )

        assert response.status_code == 204

    def test_delete(self):
        assert app.test_client().delete(f'/v1/cart/{ObjectId()}/products/{ObjectId()}').status_code == 404

        cart = self.create_cart({})

        assert app.test_client().delete(f'/v1/cart/{cart.id}/products/{ObjectId()}').status_code == 404

        product = self.create_product({
            "cart": cart,
            "product_uuid": "c0b3fe2c-9cc9-475a-9c11-4cfaec941909",
            "price": 25,
            "amount": 2
        })

        assert app.test_client().delete(f'/v1/cart/{cart.id}/products/{product.id}').status_code == 204

        with patch("app.modules.products.repositories.Product", object), pytest.raises(Exception):
            assert app.test_client().delete(f'/v1/cart/{cart.id}/products/{product.id}').status_code == 500
