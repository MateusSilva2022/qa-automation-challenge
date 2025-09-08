import random, string
from dataclasses import dataclass

SUBJECTS = ["Maths","Physics","Chemistry","Computer Science","English","Economics","Arts","Biology","Accounting","History"]
HOBBIES = ["Sports","Reading","Music"]
GENDERS = ["Male","Female","Other"]
STATE_CITY = {"NCR":["Delhi","Gurgaon","Noida"],"Uttar Pradesh":["Agra","Lucknow","Merrut"],"Haryana":["Karnal","Panipat"],"Rajasthan":["Jaipur","Jaiselmer"]}

@dataclass
class Person:
    first_name:str; last_name:str; email:str; gender:str; mobile:str
    birth_day:int; birth_month_idx:int; birth_year:int
    subjects:list; hobbies:list; address:str; state:str; city:str

def rand(n=8, letters=True, digits=False):
    ch = (string.ascii_lowercase if letters else "") + (string.digits if digits else "")
    return "".join(random.choice(ch) for _ in range(n))

def random_person():
    first = random.choice(["Mateus","Joao","Ana","Carla","Bruno","Livia","Renan","Paula","Lucas","Beatriz"])
    last  = random.choice(["Silva","Souza","Oliveira","Almeida","Gomes","Lima","Ribeiro","Pereira","Costa","Carvalho"])
    email = f"{first.lower()}.{last.lower()}@example.com"
    gender = random.choice(GENDERS)
    mobile = "".join(random.choice("0123456789") for _ in range(10))
    day, month_idx, year = random.randint(1,28), random.randint(0,11), random.randint(1990,2005)
    subjects = random.sample(SUBJECTS, k=random.randint(1,3))
    hobbies = random.sample(HOBBIES, k=random.randint(1,2))
    address = f"Rua {rand(6).title()} {random.randint(10,999)}, Bairro {rand(5).title()}"
    state = random.choice(list(STATE_CITY.keys()))
    city  = random.choice(STATE_CITY[state])
    return Person(first,last,email,gender,mobile,day,month_idx,year,subjects,hobbies,address,state,city)

