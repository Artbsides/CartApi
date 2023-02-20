import unittest
import pytest

from unittest.mock import patch
from bson.objectid import ObjectId
from datetime import datetime, timedelta

from mongoengine.connection import _get_db

from tests.main import app
from app.constants import DISCOUNT_TYPES

from app.modules.carts.repositories import CartRepository
from app.modules.coupons.repositories import CouponRepository


class TestCoupons(unittest.TestCase):
    def tearDown(self):
        _get_db().drop_collection("coupons")
        _get_db().drop_collection("products")
        _get_db().drop_collection("carts")

        _get_db().create_collection("products") \
            .create_index([("product_uuid", 1), ("cart", 1)], unique=True)

    def create_cart(self, data):
        return CartRepository(**data).save()

    def create_coupon(self, data):
        return CouponRepository(**data).save()

    def test_put(self):
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

        with pytest.raises(Exception):
            response = app.test_client().put("/v1/cart/123/coupon",
                json={
                    "code": coupon.code
                }
            )

            assert response.status_code == 500

        response = app.test_client().put(f'/v1/cart/{ObjectId()}/coupon',
            json={
                "code": coupon.code
            }
        )

        assert response.status_code == 404

        response = app.test_client().put(f'/v1/cart/{cart.id}/coupon',
            json={
                "code": "abc"
            }
        )

        assert response.status_code == 404

        response = app.test_client().put(f'/v1/cart/{cart.id}/coupon',
            json={
                "code": coupon.code
            }
        )

        assert response.status_code == 201

    def test_delete(self):
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

        assert app.test_client().delete(f'/v1/cart/{ObjectId()}/coupon').status_code == 404
        assert app.test_client().delete(f'/v1/cart/{cart.id}/coupon').status_code == 204

        with patch("app.modules.carts.repositories.Cart", object), pytest.raises(Exception):
            assert app.test_client().delete(f'/v1/cart/{cart.id}/coupon').status_code == 500
