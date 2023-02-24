from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.forms import modelform_factory
from offers.models import *
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.images import Image
from django.contrib.auth.decorators import login_required
# Create your views here.
from offers.forms import OfferForm, CreateUserForm, CustomerForm
from .models import *
from .filters import OfferFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def auth(request):
    return render(request, "offers/Non_autorise.html")


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def ahmed(request):
    offer = offers.objects.all()
    offers_count = offer.filter(approve=True).count()
    offers_sell = offer.filter(status="Sell", approve="True").count()
    offers_buy = offer.filter(status="buy", approve="True").count()
    customer = request.user.customer
    myFilter = OfferFilter(request.GET, queryset=offer)
    offer = myFilter.qs

    context = {"offers": offers.objects.all(), "filter": myFilter, "offers": offer, "count": offers_count,
               "buy": offers_buy, "sell": offers_sell, "customer": customer}

    return render(request, "offers/offersPage.html", context)


@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, "offers/register.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        customer.email = request.user.email
        if form.is_valid():
            face_photo = request.POST.get('image_data')
            customer.face_picture.save('image.jpeg', ContentFile(face_photo), save=True)
            form.save()
            return redirect('welcome')

    context = {'form': form}

    return render(request, 'offers/account_settings.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('welcome')
        else:
            messages.info(request, 'Username OR password is incorrect')

    return render(request, "offers/login.html")


@login_required(login_url='login')
def LogoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def detail(request, id):
    offer = get_object_or_404(offers, pk=id)
    return render(request, "offers/detail.html", {"offer": offer})


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def createOrder(request):
    form = OfferForm()
    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            offers = form.save(commit=False)
            offers.customer = request.user.customer
            form.save()
            return redirect('submit')
    else:
        form = OfferForm()
    return render(request, "offers/createOffer.html", {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def updateOrder(request, pk):
    offer = offers.objects.get(id=pk)
    form = OfferForm(instance=offer)
    if request.method == "POST":
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('welcome')
    return render(request, "offers/new.html", {'form': form})


@login_required(login_url='login')
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    offer = customer.offers_set.all()
    myFilter = OfferFilter(request.GET, queryset=offer)
    offer = myFilter.qs
    context = {'customer': customer, 'myFilter': myFilter, 'Offers': offer}
    return render(request, 'offers/customer.html', context)


@login_required(login_url='login')
@admin_only
def welcome(request):
    offer = offers.objects.all()
    myFilter = OfferFilter(request.GET, queryset=offer)
    offer = myFilter.qs

    context = {"offers": offers.objects.all(), "filter": myFilter, "offers": offer}
    return render(request, "offers/home.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def submitted(request):
    return render(request, "offers/offerSubmit.html")


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def offersPage(request):
    offer = offers.objects.all()
    myFilter = OfferFilter(request.GET, queryset=offer)
    offer = myFilter.qs

    context = {"offers": offers.objects.all(), "filter": myFilter, "offers": offer}
    return render(request, "offers/offersPage.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def CustomerInfo(request, pk):
    offer = offers.objects.get(id=pk)
    custome = offer.customer

    context = {'offer': offer, 'customer': custome}
    return render(request, 'offers/CustomerInfo.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def my_offers(request):
    # Get the current user's customer instance
    customer = request.user.customer
    # Filter the offers queryset to only include offers created by the current user
    Offer = offers.objects.filter(customer=customer)
    context = {
        'offers': Offer,
    }

    return render(request, 'offers/my_offers.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def deleteOrder(request, pk):
    offer = offers.objects.get(id=pk)
    if request.method == "POST":
        offer.delete()
        return redirect('/')

    context = {'offer': offer}
    return render(request, 'offers/delete.html', context)
