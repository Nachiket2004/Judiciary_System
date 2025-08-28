from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Lawyer(models.Model):
    """
    Lawyer profile model with verification status
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lawyer_profile')
    bar_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    bio = models.TextField(blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    office_address = models.TextField(blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Verification badge info
    verification_badge_url = models.URLField(blank=True)
    verification_qr_code = models.ImageField(upload_to='verification_qr/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lawyers_lawyer'
        verbose_name = 'Lawyer'
        verbose_name_plural = 'Lawyers'
    
    def __str__(self):
        return f"{self.user.full_name} - {self.specialization}"
    
    @property
    def total_cases(self):
        return self.cases.count()
    
    @property
    def won_cases(self):
        return self.cases.filter(outcome='won').count()
    
    @property
    def win_rate(self):
        total = self.total_cases
        if total == 0:
            return 0
        return round((self.won_cases / total) * 100, 2)


class LawyerVerification(models.Model):
    """
    Lawyer verification log with multiple methods support
    """
    VERIFICATION_METHODS = [
        ('ocr', 'OCR Document Processing'),
        ('mock_digilocker', 'Mock DigiLocker (Demo)'),
        ('manual', 'Manual Verification'),
        ('email_phone', 'Email + Phone Verification'),
        ('blockchain', 'Blockchain Verification'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, related_name='verifications')
    method = models.CharField(max_length=20, choices=VERIFICATION_METHODS)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Extracted/submitted data
    extracted_data = models.JSONField(null=True, blank=True)
    raw_ocr_text = models.TextField(blank=True)  # For OCR method
    uploaded_document = models.FileField(upload_to='verification_docs/', null=True, blank=True)
    
    # Admin review
    admin_comments = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_verifications')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Confidence and metadata
    confidence_score = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lawyers_verificationlog'
        verbose_name = 'Verification Log'
        verbose_name_plural = 'Verification Logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.lawyer.user.full_name} - {self.get_method_display()} ({self.status})"
    
    def approve(self, admin_user, comments=""):
        """Approve verification and update lawyer status"""
        self.status = 'approved'
        self.reviewed_by = admin_user
        self.reviewed_at = timezone.now()
        self.admin_comments = comments
        self.save()
        
        # Update lawyer verification status
        self.lawyer.is_verified = True
        self.lawyer.verification_date = timezone.now()
        if self.extracted_data and 'bar_id' in self.extracted_data:
            self.lawyer.bar_id = self.extracted_data['bar_id']
        self.lawyer.save()
    
    def reject(self, admin_user, comments=""):
        """Reject verification"""
        self.status = 'rejected'
        self.reviewed_by = admin_user
        self.reviewed_at = timezone.now()
        self.admin_comments = comments
        self.save()


class Case(models.Model):
    """
    Case model for lawyer case history
    """
    CASE_TYPES = [
        ('criminal', 'Criminal Law'),
        ('civil', 'Civil Law'),
        ('corporate', 'Corporate Law'),
        ('family', 'Family Law'),
        ('property', 'Property Law'),
        ('labor', 'Labor Law'),
        ('tax', 'Tax Law'),
        ('constitutional', 'Constitutional Law'),
        ('other', 'Other'),
    ]
    
    OUTCOMES = [
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('settled', 'Settled'),
        ('ongoing', 'Ongoing'),
        ('dismissed', 'Dismissed'),
    ]
    
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, related_name='cases')
    title = models.CharField(max_length=200)
    description = models.TextField()
    case_type = models.CharField(max_length=20, choices=CASE_TYPES)
    outcome = models.CharField(max_length=10, choices=OUTCOMES, default='ongoing')
    
    date_filed = models.DateField()
    date_resolved = models.DateField(null=True, blank=True)
    court_name = models.CharField(max_length=100)
    case_number = models.CharField(max_length=50, blank=True)
    
    client_name = models.CharField(max_length=100, blank=True)  # Optional, can be anonymized
    opposing_party = models.CharField(max_length=100, blank=True)
    
    # Case value and fees
    case_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    legal_fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lawyers_case'
        verbose_name = 'Case'
        verbose_name_plural = 'Cases'
        ordering = ['-date_filed']
    
    def __str__(self):
        return f"{self.title} - {self.lawyer.user.full_name}"
    
    @property
    def duration_days(self):
        """Calculate case duration in days"""
        end_date = self.date_resolved or timezone.now().date()
        return (end_date - self.date_filed).days