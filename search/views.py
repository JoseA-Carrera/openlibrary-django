from django.shortcuts import render
import requests as rq

def index(request):
    try:
        query_set = request.GET.get('title')
        url = 'http://openlibrary.org/search.json?title=' + query_set
        response =  rq.get(url)
        data = response.json()
        data_dict = dict(data)
        titles = []
        docs = data_dict.get('docs') 

        for title in docs:
            t = title.get('title')
            titles.append(t)

        print(titles)

        if response.status_code == 200:
            return render(request, 'index.html', {'xd': titles})

        else:
            return render(request, 'index.html')

    except:
        return render(request, 'index.html',)
