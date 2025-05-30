from django.shortcuts import render, redirect
from . import forms
from . import models
# Create your views here.

def add_brands(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = forms.BrandForm(request.POST)
            if form.is_valid():
                # confusion
                # form.instance.user = request.user
                form.instance.author = request.user
                form.save()
                return redirect('home')
        else:
            form = forms.BrandForm()
        return render(request, 'form.html', {'form': form, 'title': 'Add Brand', 'button_text': 'Add Brand', 'button_class': 'btn-success'})
    else:
        return redirect('login')
    
def delete_brand(request):
    if request.user.is_authenticated:
       # brand = get_object_or_404(Brands, id=brand_id)
    

        if request.method == 'POST':
            form = forms.BrandDeleteForm(request.POST)
            if form.is_valid():
                brand_obj = form.cleaned_data['brand_to_delete']
                brand_obj.delete()
                return redirect('home') 
        else:
            form = forms.BrandDeleteForm()
        return render(request, 'form.html', {'form': form, 'title': 'Delete Brand', 'button_text': 'Delete Brand', 'button_class': 'btn-danger'})
    else:
        return redirect('login')
