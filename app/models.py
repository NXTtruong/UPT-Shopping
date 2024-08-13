from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator

STATE_CHOICES = (
    ('An Giang', 'An Giang'),
    ('Bà Rịa - Vũng Tàu', 'Bà Rịa - Vũng Tàu'),
    ('Bạc Liêu', 'Bạc Liêu'),
    ('Bắc Giang', 'Bắc Giang'),
    ('Bắc Kạn', 'Bắc Kạn'),
    ('Bắc Ninh', 'Bắc Ninh'),
    ('Bến Tre', 'Bến Tre'),
    ('Bình Định', 'Bình Định'),
    ('Bình Dương', 'Bình Dương'),
    ('Bình Phước', 'Bình Phước'),
    ('Bình Thuận', 'Bình Thuận'),
    ('Cà Mau', 'Cà Mau'),
    ('Cao Bằng', 'Cao Bằng'),
    ('Cần Thơ', 'Cần Thơ'),
    ('Đà Nẵng', 'Đà Nẵng'),
    ('Đắk Lắk', 'Đắk Lắk'),
    ('Đắk Nông', 'Đắk Nông'),
    ('Điện Biên', 'Điện Biên'),
    ('Đồng Nai', 'Đồng Nai'),
    ('Đồng Tháp', 'Đồng Tháp'),
    ('Gia Lai', 'Gia Lai'),
    ('Hà Giang', 'Hà Giang'),
    ('Hà Nam', 'Hà Nam'),
    ('Hà Nội', 'Hà Nội'),
    ('Hà Tĩnh', 'Hà Tĩnh'),
    ('Hải Dương', 'Hải Dương'),
    ('Hải Phòng', 'Hải Phòng'),
    ('Hậu Giang', 'Hậu Giang'),
    ('Hòa Bình', 'Hòa Bình'),
    ('Hưng Yên', 'Hưng Yên'),
    ('Khánh Hòa', 'Khánh Hòa'),
    ('Kiên Giang', 'Kiên Giang'),
    ('Kon Tum', 'Kon Tum'),
    ('Lai Châu', 'Lai Châu'),
    ('Lâm Đồng', 'Lâm Đồng'),
    ('Lạng Sơn', 'Lạng Sơn'),
    ('Lào Cai', 'Lào Cai'),
    ('Long An', 'Long An'),
    ('Nam Định', 'Nam Định'),
    ('Nghệ An', 'Nghệ An'),
    ('Ninh Bình', 'Ninh Bình'),
    ('Ninh Thuận', 'Ninh Thuận'),
    ('Phú Thọ', 'Phú Thọ'),
    ('Phú Yên', 'Phú Yên'),
    ('Quảng Bình', 'Quảng Bình'),
    ('Quảng Nam', 'Quảng Nam'),
    ('Quảng Ngãi', 'Quảng Ngãi'),
    ('Quảng Ninh', 'Quảng Ninh'),
    ('Quảng Trị', 'Quảng Trị'),
    ('Sóc Trăng', 'Sóc Trăng'),
    ('Sơn La', 'Sơn La'),
    ('Tây Ninh', 'Tây Ninh'),
    ('Thái Bình', 'Thái Bình'),
    ('Thái Nguyên', 'Thái Nguyên'),
    ('Thanh Hóa', 'Thanh Hóa'),
    ('Thừa Thiên Huế', 'Thừa Thiên Huế'),
    ('Tiền Giang', 'Tiền Giang'),
    ('TP Hồ Chí Minh', 'TP Hồ Chí Minh'),
    ('Trà Vinh', 'Trà Vinh'),
    ('Tuyên Quang', 'Tuyên Quang'),
    ('Vĩnh Long', 'Vĩnh Long'),
    ('Vĩnh Phúc', 'Vĩnh Phúc'),
    ('Yên Bái', 'Yên Bái'),
)

class Customer(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
)

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)

class OrderPlaced(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_placed')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders_received')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.query}'