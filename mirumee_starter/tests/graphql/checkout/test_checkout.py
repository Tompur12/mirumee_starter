from ....checkout.models import Checkout, CheckoutLine
from ....product.models import Product, ProductVariant
from ....account.models import User
import json
from decimal import Decimal


def test_checkout_by_id(db, client_query):
    product = Product.objects.create(
        name="Test Product 1",
        descrpiton="Product description",
        price=Decimal("10.00"),
        quantity=10
    )

    product_variant_1 = ProductVariant.objects.create(
        product=product,
        name="Test Product Variant 1",
        sku="Test SKU 1",
        price=Decimal("15.00")
    )

    product_variant_2 = ProductVariant.objects.create(
        product=product,
        name="Test Product Variant 2",
        sku="Test SKU 2",
        price=Decimal("25.00")
    )

    user = User.objects.create(
        email="test@user.pl",
        password="qwerty",
        first_name="test_name",
        last_name="test_lastname",
        is_staff=False,
        is_active=True
    )

    checkout = Checkout.objects.create(
        user=user,
        user_email="test@user.pl"
    )

    checkout_line_1 = CheckoutLine.objects.create(
        variant=product_variant_1,
        quantity=10,
        checkout=checkout
    )

    checkout_line_2 = CheckoutLine.objects.create(
        variant=product_variant_2,
        quantity=10,
        checkout=checkout
    )

    response = client_query(
        """
        query mycheckout($id: ID!){
            checkout(id: $id){
                id
                user{
                    id
                }
                userEmail
                lines{
                    id
                    variant{
                        id
                        price
                    }
                quantity
                }
            }
        }
        """,
        variables={'id': 1}
    )
    content = json.loads(response.content)

    checkout_response = content['data']['checkout']

    assert checkout_response['id'] == str(checkout.id)
    assert checkout_response['user']['id'] == str(checkout.user.id)
    assert checkout_response['userEmail'] == checkout.user_email
    assert checkout_response['lines'][0]['id'] == str(checkout_line_1.id)
    assert checkout_response['lines'][0]['variant']['id'] == str(product_variant_1.id)
    assert checkout_response['lines'][0]['variant']['price'] == str(product_variant_1.price)
    assert checkout_response['lines'][0]['quantity'] == checkout_line_1.quantity
    assert checkout_response['lines'][1]['id'] == str(checkout_line_2.id)
    assert checkout_response['lines'][1]['variant']['id'] == str(product_variant_2.id)
    assert checkout_response['lines'][1]['variant']['price'] == str(product_variant_2.price)
    assert checkout_response['lines'][1]['quantity'] == checkout_line_2.quantity


def test_checkouts(db, staff_query):
    product = Product.objects.create(
        name="Test Product 1",
        descrpiton="Product description",
        price=Decimal("10.00"),
        quantity=10
    )

    product_variant_1 = ProductVariant.objects.create(
        product=product,
        name="Test Product Variant 1",
        sku="Test SKU 1",
        price=Decimal("15.00")
    )

    product_variant_2 = ProductVariant.objects.create(
        product=product,
        name="Test Product Variant 2",
        sku="Test SKU 2",
        price=Decimal("25.00")
    )

    user_1 = User.objects.create(
        email="test1@user.pl",
        password="qwerty",
        first_name="test_name_1",
        last_name="test_lastname_1",
        is_staff=False,
        is_active=True
    )

    user_2 = User.objects.create(
        email="test2@user.pl",
        password="qwerty",
        first_name="test_name_2",
        last_name="test_lastname_2",
        is_staff=False,
        is_active=True
    )

    checkout_1 = Checkout.objects.create(
        user=user_1,
        user_email="test@user.pl"
    )

    checkout_2 = Checkout.objects.create(
        user=user_2,
        user_email="test@user.pl"
    )

    checkout_line_1 = CheckoutLine.objects.create(
        variant=product_variant_1,
        quantity=10,
        checkout=checkout_1
    )

    checkout_line_2 = CheckoutLine.objects.create(
        variant=product_variant_2,
        quantity=10,
        checkout=checkout_1
    )

    checkout_line_3 = CheckoutLine.objects.create(
        variant=product_variant_1,
        quantity=10,
        checkout=checkout_2
    )

    checkout_line_4 = CheckoutLine.objects.create(
        variant=product_variant_2,
        quantity=10,
        checkout=checkout_2
    )

    response = staff_query(
        """
        query mycheckouts{
            checkouts{
                id
                user{
                    id
                }
                userEmail
                lines{
                    id
                    variant{
                        id
                        price
                    }
                quantity
                }
            }
        }
        """,
    )
    content = json.loads(response.content)

    checkout_response = content['data']['checkouts']

    assert checkout_response[0]['id'] == str(checkout_1.id)
    assert checkout_response[0]['user']['id'] == str(checkout_1.user.id)
    assert checkout_response[0]['userEmail'] == checkout_1.user_email
    assert checkout_response[0]['lines'][0]['id'] == str(checkout_line_1.id)
    assert checkout_response[0]['lines'][0]['variant']['id'] == str(product_variant_1.id)
    assert checkout_response[0]['lines'][0]['variant']['price'] == str(product_variant_1.price)
    assert checkout_response[0]['lines'][0]['quantity'] == checkout_line_1.quantity
    assert checkout_response[0]['lines'][1]['id'] == str(checkout_line_2.id)
    assert checkout_response[0]['lines'][1]['variant']['id'] == str(product_variant_2.id)
    assert checkout_response[0]['lines'][1]['variant']['price'] == str(product_variant_2.price)
    assert checkout_response[0]['lines'][1]['quantity'] == checkout_line_2.quantity
    assert checkout_response[1]['id'] == str(checkout_2.id)
    assert checkout_response[1]['user']['id'] == str(checkout_2.user.id)
    assert checkout_response[1]['userEmail'] == checkout_2.user_email
    assert checkout_response[1]['lines'][0]['id'] == str(checkout_line_3.id)
    assert checkout_response[1]['lines'][0]['variant']['id'] == str(product_variant_1.id)
    assert checkout_response[1]['lines'][0]['variant']['price'] == str(product_variant_1.price)
    assert checkout_response[1]['lines'][0]['quantity'] == checkout_line_3.quantity
    assert checkout_response[1]['lines'][1]['id'] == str(checkout_line_4.id)
    assert checkout_response[1]['lines'][1]['variant']['id'] == str(product_variant_2.id)
    assert checkout_response[1]['lines'][1]['variant']['price'] == str(product_variant_2.price)
    assert checkout_response[1]['lines'][1]['quantity'] == checkout_line_4.quantity
