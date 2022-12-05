from django.shortcuts import render
import requests as rq

def books(request):
    try:
        # se trae todos los datos json y pasarlos a diccionario
        query_set = request.GET.get('name')
        url = 'http://openlibrary.org/search.json?title=' + query_set
        response =  rq.get(url)
        data = response.json()
        data_dict = dict(data)
        docs = data_dict.get('docs') 

        # 'book' tendra toda la informacion para enviarla al template
        book = {} 

        # dentro de 'docs' hay varias keys que corresponde a un objeto de la busqueda
        for key in docs: 
            values = [] 

            cover = key.get('cover_i')
            title = key.get('title')
            author =  key.get('author_name')

            # al no tener portada se accedera a un jpg 404 de internet
            if cover == None: 
                cover = 'https://www.404.agency/static/images/404-share-image.png'
            else:
                cover = f'https://covers.openlibrary.org/b/id/{cover}-M.jpg'

            values.append(cover) 
            values.append(author) 
            dic = { title: values }
            # se concatenara de manera anidada a 'book'
            book |= dic 

        if response.status_code == 200:
            return render(request, 'index.html', {'books': book})

        else:
            return render(request, 'index.html')

    except:
        return render(request, 'index.html',)

#el mismo codigo aplica a la vista authors
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
            
            values.append(photo)
            values.append(top)
            
            if death == None:
                death = 'now'
                
                if birth == None:
                    birth = 'no se sabe'
                    values.append(birth)
                
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
    