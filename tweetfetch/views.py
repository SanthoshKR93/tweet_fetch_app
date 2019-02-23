from django.views.generic import TemplateView
from tweetfetch.forms import IndexForm
from django.shortcuts import render

import base64
import requests

class IndexView(TemplateView):
   template_name = 'tweetfetch/index.html'
   def get(self,request):
      form = IndexForm()
      return render(request,self.template_name,{'form':form})

   def post(self,request):
      form = IndexForm(request.POST)
      if form.is_valid():
         text = form.cleaned_data['Twitter_Handle']

      client_key = "5aJoczxh94b5mOehbipM9uxNk"
      client_secret = "mptFtY6vrWCcxCeXojSzXHpsV03BFHde5oBaYxNOgKkUu5jZAl"

      key_secret = '{}:{}'.format(client_key,client_secret).encode('ascii')
      base64_encoded_key = base64.b64encode(key_secret)
      base64_encoded_key = base64_encoded_key.decode('ascii')

      base_url = 'https://api.twitter.com/'
      auth_url = '{}oauth2/token'.format(base_url)

      auth_headers = {
      'Authorization': 'Basic {}'.format(base64_encoded_key),
      'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      }

      auth_data = {
      'grant_type': 'client_credentials'
      }

      auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
      access_token = auth_resp.json()['access_token']

      search_headers = {
      'Authorization': 'Bearer {}'.format(access_token)    
      }

      search_params = {
      'screen_name':text,
      'q': text,
      'result_type': 'recent',
      'count': 10
      }

      search_url = '{}1.1/statuses/user_timeline.json'.format(base_url)

      search_resp = requests.get(search_url, headers=search_headers, params=search_params)

      tweet_data = search_resp.json()
      #print(tweet_data)
      tweets = []
      if search_resp.status_code == 200:
         tweets = []
         for x in tweet_data:
            tweets.append(x['text'])
         if tweets == []:
            tweets.append('No Posts To display') 
      elif search_resp.status_code == 404:
         tweets = []
         tweets.append('No results!! Check whether the user handle entered is valid.')
      else:
         tweets.append('No Posts To display')
              


      context = {
      'form':form,'tweets':tweets,
      }
      return render(request,self.template_name,context)

