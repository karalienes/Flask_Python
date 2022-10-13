from requests import put, get, post


put('http://127.0.0.1:5000/todo8', data={'data': 'enes'}).json()
put('http://127.0.0.1:5000/todo9', data={'data': 'karali'}).json()

get('http://127.0.0.1:5000/todo8').json()
get('http://127.0.0.1:5000/todo9').json()

print(get('http://127.0.0.1:5000/Enes').json())
