import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


def get_request(url, **kwargs):
    print(kwargs)
    print(f"GET from {url}")
    json_data = {}

    try:
        if "apikey" in kwargs:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth("apikey", kwargs['apikey']))
        else:
            response = requests.get(
                url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        print("Network exception occurred")

    status_code = response.status_code
    print(f"status_code: {status_code}")
    # print(f"this is the regular response: {response}")
    # print(f"With status {status_code}")
    # print(f"This is the response.text : {response.text}")
    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    req = get_request(url)
    json_result = req
    print(f"function get_dealers_from_cf {type(json_result)}")

    if json_result:
        dealerships = json_result['dealerships']
        print(f"look for me PLS:{type(dealerships)} ")
        if dealerships:

            dealers = dealerships["rows"]
            print(f"here we go {type(dealers)}")
            for dealer in dealers:
                dealer_doc = dealer['doc']
                dealerObject = CarDealer(address=dealer_doc['address'],
                                         city=dealer_doc['city'],
                                         full_name=dealer_doc['full_name'],
                                         id=dealer_doc['id'],
                                         lat=dealer_doc['lat'],
                                         long=dealer_doc['long'],
                                         short_name=dealer_doc['short_name'],
                                         st=dealer_doc['st'],
                                         state=dealer_doc['state'],
                                         zip=dealer_doc['zip'])
                results.append(dealerObject)
    print(f"look for me #2: {type(results)}")
    return results


def get_dealer_reviews_from_cf(url, dealer_id):
    result = []
    json_result = get_request(url)
    print(f"check it out {type(json_result)}")
    if json_result:
        db = json_result['reviews']
        print(f"check it out {type(db)}")
        if db:
            reviews = db['rows']
            print(f'check it out {type(reviews)}')
            for review in reviews:
                review_doc = review['doc']
                review_object = DealerReview(id=review_doc['id'],
                                             dealership=review_doc['dealership'],
                                             name=review_doc['name'],
                                             purchase=review_doc['purchase'],
                                             review=review_doc['review'])
                if review_doc['purchase'] == True:
                    review_object.set_purchase_details(purchase_date=review_doc['purchase_date'],
                                                       car_make=review_doc['car_make'],
                                                       car_model=review_doc['car_model'],
                                                       car_year=review_doc['car_year'])
                review_object.sentiment = analyze_review_sentiments(
                    review_doc['review'])

                result.append(review_object)
            return result


def post_request(url, payload, **kwargs):
    print(f"Post from {url}")
    print(f"Payload: {payload}")

    print(f"kwargs: {kwargs}")
    try:
        response = requests.post(url, json=payload, params=kwargs)

    except Exception as e:
        print("Error", e)

    status_code = response.status_code
    print(f"With status {status_code}")
    print(f"look for this carlos: {response.text}")
    json_data = json.loads(response.text)

    return json_data


def analyze_review_sentiments(dealerreview, **kwargs):
    API_KEY = "NmNvwoUervE7_eTAdixp3ei8I2WiPFn63n2pjGCVnWj0"
    NLU_URL = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/dc71bd1c-bf9d-4013-a850-091c8c07688c"

    authenticator = IAMAuthenticator(API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version="2021-08-01", authenticator=authenticator)
    natural_language_understanding.set_service_url(NLU_URL)
    response = natural_language_understanding.analyze(text=dealerreview,
                                                      features=Features(sentiment=SentimentOptions())).get_result()
    print(json.dumps(response))
    sentiment_score = str(response["sentiment"]["document"]['score'])
    sentiment_label = response['sentiment']['document']['label']
    print(sentiment_score)
    print(sentiment_label)
    sentimentresult = sentiment_label

    return sentimentresult


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
