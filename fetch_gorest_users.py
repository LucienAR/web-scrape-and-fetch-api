import requests

# GraphQL and REST API for Testing and Prototyping https://gorest.co.in/
url = 'https://gorest.co.in/public/v2/users'

r = requests.get(url)

if r.status_code == 200:
    data = r.json()
    print("Successful!")
    
    # เลือกข้อมูลที่ต้องการ ในที่นี้จะเป็นชื่อกับเพศ
    for users in data:
        name = users.get('name')
        gender = users.get('gender')
        print(f"Name : {name}\ngender: {gender}\n")
        
else:
    print(f"Error: Unable to fetch data. Status code: {r.status_code}")
    
# นำข้อมูลที่ได้นี้ ไปเก็บในแหล่งที่ต้องการเช่น csv, database
    
