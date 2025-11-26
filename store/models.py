from django.db import models

# Create your models here.

class Promotion(models.Model):
    description = models.TextField()
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

class Product(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion)
    title = models.CharField(max_length=255)  # varchar(255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2) # e.g 9999.99
    inventory = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    # In 'ManyToMany' relationship  : Django does not add a promotion column to  Product, 
    # and it does not add a product column to Promotion. Instead, django automatically creates a third table
    # With 'ManyToMany relationship, the relationship is not stored n Product. It's stored in the join table 
    # So if a Promotion is deleted, Django deletes on ly the rows in the join table. It doesn't delete the Product
    # Join table ( id| product_id | promotion_id) , so 'on_delete' attribute is not required.
    # So Django creates a third join table with the name '<app_name><model_name><field_name>' 
    # and also creates a 'ForeginKey' relationship for each model('Product' and 'Promotion')
    # Reverse relation default name: <product(model in lowercase)>_set
        # Join table: 
            # class StoreProductPromotions(models.Model):
            #     product = models.ForeginKey(Product, on_delete=models.CASCADE)
            #     promotions = models.ForeignKey(Promotion, on_delete=models.CASCADE)

            # product = Product.Objects.get(id=1)
            # prom = product.promotions.all()

class Customer(models.Model):
    # Django new features 
    # class Member(models.TextChoices):
    #     bronze = 'B', 'Bronze'
    #     silver = 'S', 'Silver'
    #     gold = 'G', 'Gold'
    
    # class MemberUsingNumber(models.IntegerChoices):
    #     bronze = '0', 'Bronze'
    #     silver = '1', 'Silver'
    #     gold = '2', 'Gold'

        # membership = models.CharField(choices=MemberUsingNumber.choices, default=MemberUsingNumber.bronze)
        # 
    BRONZE_MEMBERSHIP = 'B'
    SILVER_MEMBERSHIP = 'S'
    GOLD_MEMBERSHIP = 'G'
    MEMBERSHIP_CHOICES = [
        (BRONZE_MEMBERSHIP, 'Bronze'),
        (SILVER_MEMBERSHIP, 'Silver'),
        (GOLD_MEMBERSHIP, 'Gold')
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=50)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES, default=BRONZE_MEMBERSHIP)

    #customer.membership = 
    # get_membership_display() : to display the value visible to the admin

    class Meta:
        db_table = "store_customers"
        indexes = [models.Index(
            fields=['last_name', 'first_name']
        )
        ]

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantiy = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name = 'cart')
    created_at = models.DateTimeField(auto_now_add=True)
    # Think of 'Carts' as the container for all the products a user wants to buy
    # They usually contains the metadata about the cart(user, data created, total price, status)
    # 'Cart' itself doesn't know the details of each product - that's what 'cartitem' is for.
    # one customer can have one active 'cart' at a time .


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField()
    # Think of CartItem as the inddi idual products inside the carts
    # Each CarItem represents one rpoduct in the cart and ncludes qunatity , price, tetc.
    # A 'Cart' can have multiple 'CartItems'
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    # A single product can appear in many users' carts.
    # e.g Produt: 'iPhone 15' 
            # can be in amaunel's cart
            # can be in Sara's cart 
            # can be in Dawit's cart


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.PositiveIntegerField()
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True, related_name='my_address')
    # this model has a 'customer_id' primary key since we use 'primary_key = True' 
    # so Django doesn't create an id for this model automatically

    # And the 'related_name = 'my_address' used in 'Reverse relationship'
    # e.g customer = Customer.Objects.get(id=1)
    #     address = customer.my_address       : returns the Address model
    # But without the 'related_name' attribute, Django automatically uses the lower case of that related model
    # e.g  customer = Customer.Objects.get(id=1)
    #       address1 = customer.address (lower case of 'Customer')

