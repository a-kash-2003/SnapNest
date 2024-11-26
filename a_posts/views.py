from django.shortcuts import render

# Create your views here.
def home_view(requset):
    return render(requset,'a_posts/home.html')