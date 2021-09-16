from ....product.models import Product, ProductVariant
import json
from decimal import Decimal


def test_product_by_id(db, client_query):
    product = Product.objects.create(
        name="Test Product",
        descrpiton="Product description",
        price=Decimal("10.00"),
        quantity=10
    )

    response = client_query(
        """
        query myproduct($id: ID!) {
            product(id: $id){
                price
                id
                name
                descrpiton
                quantity
            }
        }
        """,
        variables={'id': 1}
    )
    content = json.loads(response.content)

    product_response = content['data']['product']

    assert product_response['id'] == str(product.id)
    assert product_response['descrpiton'] == product.descrpiton
    assert product_response['quantity'] == product.quantity
    assert product_response['price'] == str(product.price)


def test_products(db, client_query):
    product_1 = Product.objects.create(
        name="Test Product 1",
        descrpiton="Product description",
        price=Decimal("10.00"),
        quantity=10
    )

    product_2 = Product.objects.create(
        name="Test Product 2",
        descrpiton="Product description",
        price=Decimal("20.00"),
        quantity=20
    )

    response = client_query(
        """
        query myproducts {
            products{
                price
                id
                name
                descrpiton
                quantity
            }
        }
        """,
    )
    content = json.loads(response.content)

    product_response = content['data']['products']

    assert product_response[0]['id'] == str(product_1.id)
    assert product_response[0]['descrpiton'] == product_1.descrpiton
    assert product_response[0]['quantity'] == product_1.quantity
    assert product_response[0]['price'] == str(product_1.price)
    assert product_response[1]['id'] == str(product_2.id)
    assert product_response[1]['descrpiton'] == product_2.descrpiton
    assert product_response[1]['quantity'] == product_2.quantity
    assert product_response[1]['price'] == str(product_2.price)


def test_product_variant_by_id(db, client_query):
    product = Product.objects.create(
        name="Test Product",
        descrpiton="Product description",
        price=Decimal("10.00"),
        quantity=10
    )

    product_variant = ProductVariant.objects.create(
        product=product,
        name='Product Variant',
        sku='Test_SKU',
        price=Decimal("15.00")
    )

    response = client_query(
        """
        query myproduct($id: ID!) {
            productVariant(id: $id){
                id
                product{
                    id
                    name
                    descrpiton
                    price
                    quantity
                }
                name
                sku
                price
            }
        }
        """,
        variables={'id': 1}
    )
    content = json.loads(response.content)

    product_variant_response = content['data']['productVariant']

    assert product_variant_response['id'] == str(product_variant.id)
    assert product_variant_response['product']['id'] == str(product.id)
    assert product_variant_response['product']['name'] == product.name
    assert product_variant_response['product']['descrpiton'] == product.descrpiton
    assert product_variant_response['product']['price'] == str(product.price)
    assert product_variant_response['product']['quantity'] == product.quantity
    assert product_variant_response['name'] == product_variant.name
    assert product_variant_response['sku'] == product_variant.sku
    assert product_variant_response['price'] == str(product_variant.price)


def test_product_variants(db, client_query):
    product = Product.objects.create(
        name="Test Product",
        descrpiton="Product description",
        price=Decimal("10.00"),
        quantity=10
    )

    product_variant_1 = ProductVariant.objects.create(
        product=product,
        name='Product Variant 1',
        sku='Test_SKU_1',
        price=Decimal("15.00")
    )

    product_variant_2 = ProductVariant.objects.create(
        product=product,
        name='Product Variant 2',
        sku='Test_SKU_2',
        price=Decimal("25.00")
    )

    response = client_query(
        """
        query myproduct {
            productVariants{
                id
                product{
                    id
                    name
                    descrpiton
                    price
                    quantity
                }
                name
                sku
                price
            }
        }
        """,
    )
    content = json.loads(response.content)

    product_variant_response = content['data']['productVariants']

    assert product_variant_response[0]['id'] == str(product_variant_1.id)
    assert product_variant_response[0]['product']['id'] == str(product.id)
    assert product_variant_response[0]['product']['name'] == product.name
    assert product_variant_response[0]['product']['descrpiton'] == product.descrpiton
    assert product_variant_response[0]['product']['price'] == str(product.price)
    assert product_variant_response[0]['product']['quantity'] == product.quantity
    assert product_variant_response[0]['name'] == product_variant_1.name
    assert product_variant_response[0]['sku'] == product_variant_1.sku
    assert product_variant_response[0]['price'] == str(product_variant_1.price)
    assert product_variant_response[1]['id'] == str(product_variant_2.id)
    assert product_variant_response[1]['product']['id'] == str(product.id)
    assert product_variant_response[1]['product']['name'] == product.name
    assert product_variant_response[1]['product']['descrpiton'] == product.descrpiton
    assert product_variant_response[1]['product']['price'] == str(product.price)
    assert product_variant_response[1]['product']['quantity'] == product.quantity
    assert product_variant_response[1]['name'] == product_variant_2.name
    assert product_variant_response[1]['sku'] == product_variant_2.sku
    assert product_variant_response[1]['price'] == str(product_variant_2.price)
