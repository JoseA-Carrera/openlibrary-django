from django.shortcuts import render
import requests as rq

def books(request):
    try:
        query_set = request.GET.get('name')
        url = 'http://openlibrary.org/search.json?title=' + query_set
        response =  rq.get(url)
        data = response.json()
        data_dict = dict(data)
        docs = data_dict.get('docs') 

        book = {} # 'book' almacenara de manera anidada todos los datos al template siendo las keys lo titulos

        for key in docs: # 'key' iterara dentro de docs todas las keys que traiga la consulta requests
            values = [] # 'values' sera una lista que almacenara la url de imagen y nombre de author


            cover = key.get('cover_i')
            title = key.get('title')
            author =  key.get('author_name')

            if cover == None: # al la key que no tenga url de imagen 'cover' traera de internet una img 404
                cover = 'https://www.404.agency/static/images/404-share-image.png'
            else:
                cover = f'https://covers.openlibrary.org/b/id/{cover}-M.jpg'

            values.append(cover)
            values.append(author)

            dic = { title: values }
            book |= dic # 'book' concatenara a cada diccionario'dic' del momento


        if response.status_code == 200:
            return render(request, 'index.html', {'books': book})

        else:
            return render(request, 'index.html')

    except:
        return render(request, 'index.html',)

def authors(request):
    try:
        query_set = request.GET.get('name') 
        url = 'https://openlibrary.org/search/authors.json?q=' + query_set
        response =  rq.get(url)
        data = response.json()
        data_dict = dict(data)
        docs = data_dict.get('docs') 
        book = {}

        for key in docs:
            values = []

            photo = key.get('key')
            name = key.get('name')
            top = key.get('top_work')
            birth =  key.get('birth_date')
            death = key.get('death_date')

            photo = f'https://covers.openlibrary.org/a/olid/{photo}-M.jpg'
            
            if death == None:
                death = 'now'

            values.append(photo)
            values.append(top)
            values.append(birth)
            values.append(death)

            dic = { name: values }
            book |= dic

        if response.status_code == 200:
            return render(request, 'author.html', {'authors': book})
        else:
            return render(request, 'author.html')

    except:
        return render(request, 'author.html',)