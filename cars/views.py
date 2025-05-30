from django.shortcuts import render, redirect
from . import forms
from . import models

from django.views.generic import DetailView
from django.contrib import messages
# Create your views here.


def add_cars(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = forms.CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('home')
    else:
        form = forms.CarForm()

    return render(request, 'form.html', {'form': form, 'title': 'Add Car', 'button_text': 'Add Car', 'button_class': 'btn-success'})


def car_detail(request, car_id):
    car = models.Car.objects.get(id=car_id)

    if request.method == 'POST':
        if 'buy_now' in request.POST:
            if car.quantity > 0:
                car.buyers.add(request.user)
                car.quantity -= 1
                car.save()
                messages.success(request, 'Car purchased successfully!')
            else:
                messages.error(request, 'Car is out of stock!')
        elif 'comment' in request.POST:
            comment_form = forms.CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.car = car
                new_comment.save()

    # if request.method == 'POST':
    #     comment_form = forms.CommentForm(request.POST)
    #     if comment_form.is_valid():
    #         new_comment = comment_form.save(commit=False)
    #         new_comment.car = car
    #         new_comment.save()

    # if request.method == 'POST':
    #     # Check if the form is for adding a comment
    #     if 'comment' in request.POST:
    #         comment_form = forms.CommentForm(request.POST)
    #         if comment_form.is_valid():
    #             new_comment = comment_form.save(commit=False)
    #             new_comment.car = car
    #             new_comment.save()
    #     # Check if the form is for buying the car
    #     elif 'buy_now' in request.POST:
    #         if car.quantity > 0:
    #             car.buyers.add(request.user)
    #             car.quantity -= 1
    #             car.save()
    #             messages.success(request, 'Car purchased successfully!')
    #         else:
    #             messages.error(request, 'Car is out of stock!')

    # comments = car.comments.all()
    comments = models.Comment.objects.filter(car=car)

    comment_form = forms.CommentForm()

    return render(request, 'car_detail.html', {'car': car, 'comments': comments, 'comment_form': comment_form})


def delete_car(request, car_id):
    #car = get_object_or_404(Car, id=car_id)
    if not request.user.is_authenticated:
        return redirect('login')
    
    car = models.Car.objects.get(id=car_id)
    # Проверка дали потребителят има право да изтрие колата
    if request.user.is_superuser or car.owner == request.user:
        car.delete()
        messages.success(request, 'Car was successfully deleted.')
    else:
        messages.error(request, 'You do not have permission to delete this car.')
    
    return redirect('home') 
