from django import forms
from . import models

class BrandForm(forms.ModelForm):
    class Meta:
        model = models.Brands
        fields = '__all__'

class BrandDeleteForm(forms.ModelForm):
    brand_to_delete = forms.ModelChoiceField(queryset=models.Brands.objects.all(), label='Brand to delete', empty_label='Select a brand')  
    class Meta:
        model = models.Brands
        fields = ['brand_to_delete']