import os
import unittest
import requests_mock
import pytest

from unittest.mock import patch
from bson.objectid import ObjectId
from datetime import datetime, timedelta

from mongoengine.connection import _get_db

from tests.main import app
from app.constants import DISCOUNT_TYPES

from app.modules.carts.repositories import CartRepository
from app.modules.products.repositories import ProductRepository
from app.modules.coupons.repositories import CouponRepository


class TestCart(unittest.TestCase):
    def tearDown(self):
        _get_db().drop_collection("coupons")
        _get_db().drop_collection("products")
        _get_db().drop_collection("carts")

        _get_db().create_collection("products") \
            .create_index([("product_uuid", 1), ("cart", 1)], unique=True)

    def create_coupon(self, data):
        return CouponRepository(**data).save()

    def create_cart(self, data):
        return CartRepository(**data).save()

    def create_product(self, data):
        return ProductRepository(**data).save()

    def test_post(self):
        response = app.test_client().post("/v1/cart",
            json={}
        )

        assert response.status_code == 422

        response = app.test_client().post("/v1/cart",
            json={
                "product_uuid": "c0b3fe2c-9cc9-475a-9c11-4cfaec941909",
                "price": 25,
                "amount": 2
            }
        )

        assert response.status_code == 201

        with patch("app.modules.carts.repositories.Cart", object), pytest.raises(Exception):
            response = app.test_client().post("/v1/cart",
                json={
                    "product_uuid": "c0b3fe2c-9cc9-475a-9c11-4cfaec941909",
                    "price": 25,
                    "amount": 2
                }
            )

            assert response.status_code == 500

    def test_delete(self):
        with pytest.raises(Exception):
            assert app.test_client().delete("/v1/cart/123").status_code == 500

        assert app.test_client().delete(f'/v1/cart/{ObjectId()}').status_code == 404

        cart = self.create_cart({
            "discount_coupon": DISCOUNT_TYPES[0]
        })

        assert app.test_client().delete(f'/v1/cart/{cart.id}').status_code == 204

    @requests_mock.mock()
    def test_get(self, mock_request):
        with pytest.raises(Exception):
            assert app.test_client().get("/v1/cart/123").status_code == 500

        assert app.test_client().get(f'/v1/cart/{ObjectId()}').status_code == 404

        coupon = self.create_coupon({
            "code": "BcOY6A4d",
            "discount": {
                "type": DISCOUNT_TYPES[0],
                "value": 2.5
            },
            "expires_at": datetime.utcnow() + timedelta(days=3)
        })

        cart = self.create_cart({
            "discount_coupon": coupon
        })

        product = self.create_product({
            "cart": cart,
            "product_uuid": "c0b3fe2c-9cc9-475a-9c11-4cfaec941909",
            "price": 25,
            "amount": 2
        })

        mock_request.get(f'{os.getenv("X_API")}/v1/products?uuids[]={product.product_uuid}',
            json={
                "products": [
                    {
                        "id": "c0b3fe2c-9cc9-475a-9c11-4cfaec941909",
                        "title": "Product 1",
                        "description": "Lorem ipsum dolor sit amet.",
                        "price": 12.5,
                        "image": "1631050815.png"
                    }
                ]
            }
        )

        assert app.test_client().get(f'/v1/cart/{cart.id}').status_code == 200

        with patch("app.external_services.requests", object), pytest.raises(Exception):
            assert app.test_client().get(f'/v1/cart/{cart.id}').status_code == 500
