import datetime
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')
django.setup()
import random
import sys
from string import ascii_lowercase

from fileuploads.models import TagImage, CategoryImage, ProductImage

from addresses.models import Address

from orders.models import Order, OrderItem
from products.models import Product

import faker

from categories.models import Category
from comments.models import Comment
from tags.models import Tag
from users.models import AppUser

faker = faker.Faker()


def seed_products():
    products_count = Product.objects.count()
    products_to_seed = 35

    sys.stdout.write('[+] Seeding %d products\n' % (products_to_seed - products_count))

    dir = os.path.join(os.getcwd(), 'static', 'images', 'products')

    if not os.path.exists(dir):
        os.makedirs(dir)

    for i in range(products_count, products_to_seed):
        name = faker.sentence()
        # slug = faker.slug()
        # description = faker.paragraph(nb_sentences=3, variable_nb_sentences=10)
        description = faker.text()
        tags = Tag.objects.get_random_tag()
        categories = Category.objects.gent_random_category()
        price = round(random.uniform(150, 3000), 2)
        start_date = datetime.date(year=2016, month=1, day=1)
        random_date = faker.date_between(start_date=start_date, end_date='+4y')

        publish_on = random_date
        # publish_on = faker.date_time_between('-3y', '+1y')
        product = Product.objects.create(name=name, description=description, price=price,
                                         publish_on=publish_on, stock=faker.random_int(min=0, max=400))
        product.tags.add(tags)
        product.categories.add(categories)

        file_name = "".join(random.choice(ascii_lowercase) for i in range(16))
        file_path = os.path.join(dir, file_name)
        ProductImage.objects.create(file_name=file_name, original_name='adults.png',
                                    file_length=faker.random.randint(400, 10000),
                                    product=product,
                                    file_path=file_path.replace(os.getcwd(), '').replace('\\', '/'))


def seed_admin():
    email = 'admin@djangoshopapi.com'
    admin = AppUser.objects.get_admin()
    if admin is None:
        AppUser.objects.create_superuser('admin', 'admin@blogapi.com', 'password', first_name='adminFN',
                                         last_name='adminLN')
    else:
        admin.email = email
        if not admin.check_password('password'):
            admin.set_password('password')
        admin.save()


def seed_users():
    users_count = AppUser.objects.count()
    users_to_seed = 23
    sys.stdout.write('[+] Seeding %d users\n' % (users_to_seed - users_count))
    for i in range(users_count, users_to_seed):
        profile = faker.profile(fields='username,mail,name')
        username = profile['username']
        first_name = profile['name'].split()[0]
        last_name = profile['name'].split()[1]
        email = profile['mail']
        password = 'password'
        # create_user instead of create, to hash
        AppUser.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                    password=password)


def seed_tags():
    dir = os.path.join(os.getcwd(), 'static', 'images', 'tags')
    if not os.path.exists(dir):
        os.makedirs(dir)

    sys.stdout.write('[+] Seeding tags\n')
    tag, created = Tag.objects.get_or_create(name='jackets', defaults={'description': 'spring mvc tutorials'})
    file_name = "".join(random.choice(ascii_lowercase) for i in range(16))
    file_path = os.path.join(dir, file_name)
    TagImage.objects.create(file_name=file_name, original_name='jackets.png',
                            file_length=faker.random.randint(400, 10000),
                            tag=tag,
                            file_path=file_path.replace(os.getcwd(), '').replace('\\', '/'))

    tag, created = Tag.objects.get_or_create(name='jeans', defaults={'description': 'rails tutorials'})

    file_name = "".join(random.choice(ascii_lowercase) for i in range(16))
    file_path = os.path.join(dir, file_name)
    TagImage.objects.create(file_name=file_name, original_name='jeans.png',
                            file_length=faker.random.randint(400, 10000),
                            tag=tag,
                            file_path=file_path.replace(os.getcwd(), '').replace('\\', '/'))

    tag, created = Tag.objects.get_or_create(name='shoes', defaults={'description': '.net core tutorials'})

    file_name = "".join(random.choice(ascii_lowercase) for i in range(16))
    file_path = os.path.join(dir, file_name)
    TagImage.objects.create(file_name=file_name, original_name='shoes.png',
                            file_length=faker.random.randint(400, 10000),
                            tag=tag,
                            file_path=file_path.replace(os.getcwd(), '').replace('\\', '/'))


def seed_categories():
    sys.stdout.write('[+] Seeding categories\n')
    dir = os.path.join(os.getcwd(), 'static', 'images', 'categories')
    if not os.path.exists(dir):
        os.makedirs(dir)

    category, created = Category.objects.get_or_create(name='adults', defaults={'description': 'adults clothes'})
    file_name = "".join(random.choice(ascii_lowercase) for i in range(16))
    file_path = os.path.join(dir, file_name)
    CategoryImage.objects.create(file_name=file_name, original_name='adults.png',
                                 file_length=faker.random.randint(400, 10000),
                                 category=category,
                                 file_path=file_path.replace(os.getcwd(), '').replace('\\', '/'))
    category, created = Category.objects.get_or_create(name='kids', defaults={'description': 'kids clothes'})
    file_name = "".join(random.choice(ascii_lowercase) for i in range(16))
    file_path = os.path.join(dir, file_name)
    CategoryImage.objects.create(file_name=file_name, original_name='kids.png',
                                 file_length=faker.random.randint(400, 10000),
                                 category=category,
                                 file_path=file_path.replace(os.getcwd(), '').replace('\\', '/'))

    category, created = Category.objects.get_or_create(name='teenagers', defaults={'description': 'teenagers clothes'})
    file_name = "".join(random.choice(ascii_lowercase) for i in range(16))
    file_path = os.path.join(dir, file_name)
    CategoryImage.objects.create(file_name=file_name, original_name='teenagers.png',
                                 file_length=faker.random.randint(400, 10000),
                                 category=category,
                                 file_path=file_path.replace(os.getcwd(), '').replace('\\', '/'))


def seed_comments():
    comments_count = Comment.objects.count()
    comments_to_seed = 31
    sys.stdout.write('[+] Seeding %d comments\n' % (comments_to_seed - comments_count))

    if bool(random.getrandbits(1)):
        rating = faker.random_int(min=1, max=5)
    else:
        rating = None

    for i in range(comments_count, comments_to_seed):
        Comment.objects.create(content=faker.sentence(), user_id=AppUser.objects.order_by('?').only('id').first().id,
                               rating=rating,
                               product=Product.objects.order_by('?').only('id').first())


def seed_addresses():
    addresses_to_seed = 25
    address_count = Address.objects.all().count()
    sys.stdout.write('[+] Seeding %d addresses\n' % (addresses_to_seed - address_count))

    for i in range(address_count, addresses_to_seed):

        if bool(random.getrandbits(1)):
            user = AppUser.objects.order_by('?').only('id', 'first_name', 'last_name').first()
        else:
            user = None

        address = Address(
            country=faker.country(),
            city=faker.city(),
            zip_code=faker.zipcode(),  # or faker.postcode()
            address=faker.street_address(),  # address=faker.address()
            user=user)

        if user is not None:
            address.first_name = user.first_name
            address.last_name = user.last_name
        else:
            profile = faker.profile(fields='name')
            first_name = profile['name'].split()[0]
            last_name = profile['name'].split()[1]
            address.first_name = first_name
            address.last_name = last_name

        address.save()
        address.save()


def seed_orders():
    orders_to_seed = 25
    orders_count = Order.objects.all().count()
    sys.stdout.write('[+] Seeding %d orders\n' % (orders_to_seed - orders_count))

    for i in range(orders_count, orders_to_seed):
        address_id = Address.objects.order_by('?').only('id').first().id
        user_id = AppUser.objects.order_by('?').values('id').first()['id']
        Order.objects.create(address_id=address_id, user_id=user_id)

    order_items_to_seed = 35
    order_items_count = OrderItem.objects.count()
    sys.stdout.write('[+] Seeding %d order items\n' % (order_items_to_seed - order_items_count))

    for i in range(order_items_count, order_items_to_seed):
        product = Product.objects.order_by('?').only('id').first()
        order = Order.objects.get_order_not_containing_product(product)
        if order is None:  # all orders have this product already
            continue
        OrderItem.objects.create(
            name=product.name,
            slug=product.slug,
            user_id=order.user_id,
            order_id=order.id,
            product=product,
            quantity=faker.random_int(min=1, max=7),
            price=min(5, product.price + (round(random.uniform(-20.0, 20.0), 2))),
            # random price near the usual product price
            # user=AppUser.objects.order_by('?').first())
        )


if __name__ == '__main__':
    seed_categories()
    seed_tags()
    seed_admin()
    seed_users()
    seed_products()
    seed_comments()

    seed_addresses()
    seed_orders()

    print("done")
article = faker.text(max_nb_chars=20)
