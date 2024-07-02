from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from .models import Link
from django.http import HttpResponseRedirect
from urllib.parse import urlparse
import re

def is_valid_url(url):
    if 'google' in url :
       return False
    
    if '/pdf/' in url :
       return False
    
    if 'https://' not in url :
       return False
    
    return True

def ValidName(name) :
    if '[' in name :
       return False
    
    return True

def parseGoogleScholar(res):
    soup = BeautifulSoup(res.text, 'html.parser')
    allLinks = soup.find_all('a')
    
    validLinks = filter_valid_links(allLinks)
    return validLinks


def filter_valid_links(links):
    valid_links = []
    curLink = []
    for link in links:
        try:
            # print(link)
            url = link.get('href')
            if is_valid_url(url=url) and ValidName(link.text):
               valid_links.append([link.text, url])
        except:
            pass
    return valid_links


# Create your views here.

def scrape(request) :
  baseUrl = "https://scholar.google.com/scholar?q={}"
  if request.method == 'POST' :
    keyword = request.POST.get('site','')
    url = baseUrl.format(keyword)
    res = requests.get(url)
    validLinks = parseGoogleScholar(res)
    # print(val)
    for title, link in validLinks :
      
      Link.objects.create(
        address = link,
        name = title
      )
    return HttpResponseRedirect('/')
  
  else :

    data = Link.objects.all()

  return render(request, "myapp/result.html", {
    'data' : data,
  })

def clear(request) :
  Link.objects.all().delete()
  return render(request=request,template_name='myapp/result.html')


