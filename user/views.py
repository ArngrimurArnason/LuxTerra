from http.client import HTTPResponse

from django.shortcuts import render
# Create your views here.
def index(request):
    return HTTPResponse(f"Response from {request.path}")

def get_user_by_id(request):
    return HTTPResponse(f"Response from {request.path}")