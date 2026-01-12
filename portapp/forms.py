from django import forms
from.models import Documents, Login, user_register, company_register, contract_register,job,Interview,Tender, TenderApplication,WorkStatusReport, Import

class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['email', 'password']
        widgets ={
            'password': forms.PasswordInput(attrs={'placeholder':'Enter your password'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = user_register
        fields =['name','gender','address','contact']
class CompanyForm(forms.ModelForm):
    class Meta:
        model = company_register
        fields = [
            'company_name',
            'company_address',
            'contact',
            'state',
            'district',
            'city',
            'registration_number',           # <-- This
            'industry_type',                 # <-- This
        ]
class ContractForm(forms.ModelForm):
    class Meta:
        model  = contract_register
        fields =['name','address','gender','date_of_birth','district','registration_id','contact'] 
class Loginformcheck(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = user_register
        fields = ['name', 'gender', 'address', 'contact'] 
class JobForm(forms.ModelForm):
    class Meta:
        model = job
        fields = ['job_category', 'job_name', 'job_description', 'salary', 'date_of_apply']
        widgets = {
            'date_of_apply': forms.DateInput(attrs={'type': 'date'}),  # Use a date picker
        }
class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['interview_date', 'interview_time', 'description']
class TenderForm(forms.ModelForm):
    class Meta:
        model = Tender
        fields = ['category', 'tender_type', 'description', 'amount', 'starting_date', 'number_of_days']
        widgets = {
            'starting_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
class AgreementUploadForm(forms.ModelForm):
    class Meta:
        model = TenderApplication
        fields = ['contract_agreement']  # Only allow uploading the agreement
        widgets = {
            'contract_agreement': forms.ClearableFileInput(attrs={'accept': '.pdf'}),
        }
class WorkStatusReportForm(forms.ModelForm):
    class Meta:
        model = WorkStatusReport
        fields = ['description', 'file']

class ImportForm(forms.ModelForm):
    class Meta:
        model = Import
        fields = ['item_name', 'quantity', 'import_date']
        widgets = {
            'import_date': forms.DateInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Select date'}),
        }

class DocumentsForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = [
            'do_file',
            'customs_duty_file',
            'packing_list_file',
            'import_declaration_file',
            'kyc_file'
        ]
        widgets = {
            'do_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'customs_duty_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'packing_list_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'import_declaration_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'kyc_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }