from time import timezone
from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import date

class Login(models.Model):
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    user_type=models.CharField(max_length=10)
    status=models.BooleanField(default=0)

class user_register(models.Model):
    name=models.CharField(max_length=100)
    gender=models.CharField(max_length=10)
    address=models.CharField(max_length=200)
    contact=models.CharField(max_length=15)
    login=models.ForeignKey(Login,on_delete=models.CASCADE)
class company_register(models.Model):
    company_name = models.CharField(max_length=100)
    company_address = models.CharField(max_length=200)
    contact = models.CharField(max_length=15)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100, verbose_name="Company Registration Number / CIN", blank=True, null=True)
    industry_type = models.CharField(
        max_length=100,
        choices=[
            ('Shipping', 'Shipping'),
            ('Logistics', 'Logistics'),
            ('Exporter', 'Exporter'),
            ('Manufacturer', 'Manufacturer'),
            ('Other', 'Other'),
        ],
        default='Other'
    )

    login=models.ForeignKey(Login,on_delete=models.CASCADE)
class contract_register(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    gender=models.CharField(max_length=10)
    date_of_birth=models.DateField()
    district=models.CharField(max_length=100)
    registration_id=models.CharField(max_length=100)
    contact=models.CharField(max_length=15)
    login=models.ForeignKey(Login,on_delete=models.CASCADE)
class job(models.Model):
    job_category=models.CharField(max_length=100)
    job_name=models.CharField(max_length=100)
    job_description=models.TextField()
    salary=models.CharField(max_length=100)
    date_of_apply=models.DateField() 
class job_apply(models.Model):
    STATUS_CHOICES = [
        (0, 'Pending'),   # Added 'Pending' with value 0
        (1, 'Accepted'),
        (2, 'Rejected'),
    ]
    user = models.ForeignKey(user_register, on_delete=models.CASCADE, null=True, blank=True)
    job_id = models.ForeignKey(job, on_delete=models.CASCADE, null=True, blank=True)
    cv = models.FileField(upload_to='cv/')
    current_date = models.DateField(auto_now_add=True)
    login_id = models.ForeignKey(Login, on_delete=models.CASCADE, null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)  # Default is now 'Pending'
    appointment_status=models.IntegerField(("Appointment Status"), choices=STATUS_CHOICES, default=0)  # Default is now 'Pending'
    appointment_letter=models.FileField(upload_to='appointment_letter/', blank=True, null=True)  # Optional field for appointment letter
class Interview(models.Model):
    job_application = models.ForeignKey('job_apply', on_delete=models.CASCADE, related_name='interview_list')
    current_date = models.DateField(auto_now_add=True)
    interview_date = models.DateField()
    interview_time = models.TimeField()
    description = models.TextField()
    interview_link = models.URLField(max_length=200, blank=True, null=True) 
    interview_status = models.CharField(max_length=20, default='Scheduled', choices=[
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
    ])
    def __str__(self):
        return f"Interview on {self.interview_date} for {self.job_application.job_id.job_name if self.job_application else 'N/A'}"
class News(models.Model):
    content = models.TextField()  # Field to store the news content
    current_date = models.DateField(auto_now_add=True)  # Automatically store the current date

    def __str__(self):
        return f"News on {self.current_date}"
class Ship(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)  # Link to the company login
    ship_name = models.CharField(max_length=100)  # Name of the ship
    source = models.CharField(max_length=100)  # Source location
    destination = models.CharField(max_length=100)
    departure_date = models.DateField(null=True, blank=True)
    ship_description = models.TextField()  # Description of the ship
    ship_details = models.TextField()  # Additional details about the ship
    created_at = models.DateTimeField(auto_now_add=True)
    imo_number = models.CharField(max_length=7, unique=True, null=True, blank=True)
    mmsi_number = models.CharField(max_length=9, unique=True, null=True, blank=True)
    flag_state = models.CharField(max_length=50, default="Unknown")  # Country where the ship is registered
    year_built = models.PositiveIntegerField(default=2000)  # Year the ship was constructed
    SPACE_CHOICES = [
        ('available', 'Available'),
        ('not_available', 'Not Available'),
    ]
    space = models.CharField(max_length=20, choices=SPACE_CHOICES, default='available') 
    location_status = models.CharField(max_length=20, default='Docked')
    SHIP_CATEGORY_CHOICES = [
        ('Container', 'Container'),
        ('Oil Tanker', 'Oil Tanker'),
        ('Bulk Carrier', 'Bulk Carrier'),
        ('Passenger', 'Passenger'),
    ]
    ship_category = models.CharField(
        max_length=100,
        choices=SHIP_CATEGORY_CHOICES,
        default='Container'
    )
    SHIP_TYPE_CHOICES = [
        ('Import', 'Import'),
        ('Export', 'Export'),
        ('Both', 'Both'),
    ]
    ship_type = models.CharField(
        max_length=10,
        choices=SHIP_TYPE_CHOICES,
        default='Import'
    )
    

    def __str__(self):
        return self.ship_name
    
class Import(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    import_date = models.DateField(null=True)  # Field for datepicker input
    added_at = models.DateTimeField(auto_now_add=True)
    RELEASE_STATUS_CHOICES = [
        ('', '---------'),  # Default empty choice
        ('pending', 'Pending'),
        ('request_documents', 'Request Documents'),
        ('documents_submitted', 'Documents Submitted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    release_status = models.CharField(
        max_length=20,
        choices=RELEASE_STATUS_CHOICES,
        default='',
        blank=True
    )
    gate_pass = models.CharField(max_length=100, blank=True, null=True)
  

class Export(models.Model):
    user_login = models.ForeignKey(Login, on_delete=models.CASCADE, default=None)
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, default=None)
    product_category = models.CharField(max_length=100, default="")
    product_name = models.CharField(max_length=100, default="")
    company_name = models.CharField(max_length=100, default="")
    exporting_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tax = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    product_description = models.TextField(default="")
    quantity = models.PositiveIntegerField(default=0)
    recipient_name = models.CharField(max_length=100, default="")
    recipient_address = models.TextField(default="")
    recipient_contact_number = models.CharField(max_length=15, default="")
    source = models.CharField(max_length=100, default="")
    destination = models.CharField(max_length=100, default="")
    cancel_status = models.IntegerField(default=0)
    refund_status = models.IntegerField(default=0)  # 0 = Not Refunded, 1 = Refunded
    PAYMENT_STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'Paid'),
        (2, 'Failed'),
    ]
    payment_status = models.IntegerField(choices=PAYMENT_STATUS_CHOICES, default=0)
    unique_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4, editable=False)
    current_date = models.DateField(auto_now_add=True) 
    month = models.IntegerField(default=date.today().month)
    year = models.IntegerField(default=date.today().year)

    def __str__(self):
        return self.product_name
    
class Documents(models.Model):
    import_item = models.ForeignKey('Import', on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='import_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    do_file = models.FileField(upload_to='import_documents/', verbose_name="Delivery Order (DO)", blank=True, null=True)
    customs_duty_file = models.FileField(upload_to='import_documents/', verbose_name="Customs Duty Payment Proof", blank=True, null=True)
    packing_list_file = models.FileField(upload_to='import_documents/', verbose_name="Packing List", blank=True, null=True)
    import_declaration_file = models.FileField(upload_to='import_documents/', verbose_name="Import Declaration Form", blank=True, null=True)
    kyc_file = models.FileField(upload_to='import_documents/', verbose_name="KYC Documents", blank=True, null=True)


class Complaint(models.Model):
    export = models.ForeignKey(Export, on_delete=models.CASCADE)  # Link to export
    user = models.ForeignKey(Login, on_delete=models.CASCADE)     # Link to user
    complaint_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    replay_text = models.TextField(blank=True, null=True)  # Optional field for reply from admin
    
    def __str__(self):
        return f"Complaint by {self.user.email} on {self.created_at.date()}"
class Notification(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE, null=True, blank=True)  
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Tender(models.Model):
    TENDER_TYPE_CHOICES = [
        ('open', 'Open Tender'),
        ('close', 'Close Tender'),
    ]
    category = models.CharField(max_length=100)
    tender_type = models.CharField(max_length=10, choices=TENDER_TYPE_CHOICES)
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    starting_date = models.DateField()
    number_of_days = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} ({self.get_tender_type_display()})"
class TenderApplication(models.Model):
    STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'Approved'),
        (2, 'Rejected'),
    ]
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    contract_login = models.ForeignKey(Login, on_delete=models.CASCADE)
    applied_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # <-- Default value added
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    contract_agreement = models.FileField(upload_to='agreements/', null=True, blank=True)

    def __str__(self):
        return f"{self.contract_login.email} applied for {self.tender.category} ({self.get_status_display()})"
class Payment(models.Model):
    export = models.ForeignKey(Export, on_delete=models.CASCADE, default=None)
    login = models.ForeignKey(Login, on_delete=models.CASCADE)  # Link to the user/company login
    card_holder = models.CharField(max_length=100)
    card_number = models.CharField(max_length=20)
    cvv = models.CharField(max_length=4)
    expiry_date = models.CharField(max_length=5)  # Format: MM/YY
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.login.email} on {self.current_date.date()} for {self.amount}"
    

class ExportProduct(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)  # Company login
    product_category = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=8, decimal_places=2)
    current_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} ({self.product_category})"
class ShipLocation(models.Model):
    location = models.CharField(max_length=255)  # current location
    current_date = models.DateField(auto_now_add=True)
    company_login = models.ForeignKey(Login, on_delete=models.CASCADE)
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.location} ({self.current_date})"

class ProductStatus(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    export = models.ForeignKey(Export, on_delete=models.CASCADE)
    company_login = models.ForeignKey(Login, on_delete=models.CASCADE)
    current_date = models.DateField(auto_now_add=True)
    current_time = models.TimeField(auto_now_add=True)
    booking_confirmed = models.BooleanField(default=False)
    customs_cleared = models.BooleanField(default=False)
    loaded_on_vessel = models.BooleanField(default=False)
    in_transit = models.BooleanField(default=False)
    arrived_at_port = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Status for {self.export} on {self.current_date} {self.current_time}"
class Chat(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(Login, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Login, related_name='received_messages', on_delete=models.CASCADE)
    current_date = models.DateField(auto_now_add=True)
    current_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.email} to {self.receiver.email} on {self.current_date} {self.current_time}"
class WorkStatusReport(models.Model):
    contract = models.ForeignKey(Login, on_delete=models.CASCADE)
    tender_application = models.ForeignKey('TenderApplication', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='work_status/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.contract} on {self.created_at}"
class Alerts(models.Model):
    contract = models.ForeignKey(Login, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    # Optionally, add a type field for categorizing notifications
    type = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.contract} - {self.message}"
    
class CompanyNotification(models.Model):
    company = models.ForeignKey(company_register, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.company.name}: {self.message[:30]}"
