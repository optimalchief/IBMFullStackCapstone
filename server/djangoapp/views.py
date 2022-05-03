from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from random import randrange

from .forms import UserRegisterForm

# Get an instance of a logger
logger = logging.getLogger(__name__)
unique_id = randrange(1000)


def About(request):
    return render(request, 'djangoapp/pages/about.html')


def Contact(request):
    return render(request, 'djangoapp/pages/contact.html')


def signUp(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/djangoapp')

    else:
        form = UserRegisterForm()
    return render(request, 'djangoapp/pages/registration.html', {'form': form})


def get_dealerships(request):
    print("my function get_dealerships")
    context = {}
    if request.method == "GET":

        url = "https://4e11d44e.us-south.apigw.appdomain.cloud/api/dealerships"

        dealerships = get_dealers_from_cf(url)
        print(f"dealerships: {dealerships}")
        context['dealerships'] = dealerships

        return render(request, 'djangoapp/pages/home.html', context)


def get_dealer_details(request, dealer_id):
    print(type(dealer_id))
    print(dealer_id)
    context = {}
    if request.method == "GET":
        url = "https://4e11d44e.us-south.apigw.appdomain.cloud/api/reviews"
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        print(f"look for dealer details here {dealer_reviews}")
        inventory = CarModel.objects.filter(dealer_id=dealer_id)
        context = {
            "dealer_id": dealer_id,
            "reviews": dealer_reviews,
            "inventory": inventory,
        }
        return render(request, 'djangoapp/pages/dealer_details.html', context)


def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://4e11d44e.us-south.apigw.appdomain.cloud/api/dealerships"
        context = {
            "dealer_id": dealer_id,
            "dealer_name": get_dealers_from_cf(url)[dealer_id-1].full_name,
            "cars": CarModel.objects.all(),
        }
        return render(request, 'djangoapp/pages/add_review.html', context)
    elif request.method == "POST":
        if (request.user.is_authenticated):
            username = request.user.username
            payload = dict()
            payload["id"] = unique_id  # placeholder
            payload["name"] = request.POST["name"]
            payload["dealership"] = dealer_id
            payload["review"] = request.POST["content"]
            if ("purchasecheck" in request.POST):
                payload["purchase"] = True
            else:
                payload["purchase"] = False
            print(request.POST["car"])
            if payload["purchase"] == True:
                print(request.POST['car'])
                car_parts = request.POST["car"].split("|")
                payload["purchase_date"] = request.POST["purchase_date"]
                payload["car_make"] = car_parts[0]
                payload["car_model"] = car_parts[1]
                payload["car_year"] = car_parts[2]

            else:
                payload["purchase_date"] = None
                payload["car_make"] = None
                payload["car_model"] = None
                payload["car_year"] = None
            new_payload = {}
            new_payload['docs'] = payload
            print(new_payload)
            json_result = post_request(
                "https://4e11d44e.us-south.apigw.appdomain.cloud/api/post_review", new_payload, dealerId=dealer_id)
            print(json_result)
            # return JsonResponse(json_result)

        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...


# Create a `contact` view to return a static contact page
# def contact(request):

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
