import pandas as pd
train =pd.read_csv('E:/ملفات مهمة/train/train.csv')



	
import keyword
print(keyword.kwlist)

d=[1,2]
for c in d:
	print(c)


def greet(name):
    print("Hello, " + name) # i love it

greet("Sam")

def greet(name):
    print(f"Hello, {name}")

greet("Sam")



if (n := 10) > 5: # i love it
    print(n)

x = 5
print(x)

n=10
if n>5:
	print(n)


name = "Mohamed"
age = 25

if age >= 18:
    print(f"{name} is an adult")

numbers = [10, 20, 30, 40, 50]

for number in numbers:
    print(number)

def calculate_average(numbers):
    total = sum[numbers]  # i love it 
    count = len(numbers)
    return total / count
#print(calculate_average([10, 20, 30, 40]))

user = {
    "name": "Mohamed",
    "age": 25,
    "country": "Algeria",
    "job": "ML Engineer"
}

print(user)

for i in range(5):
    if i == 2:
        print("Two")
    else:
        print("Something else")


def greet(name, country, age=25):
    print(name, age, country)

greet("Mohamed", country="Algeria")



# task 7
'''
numbers = [1, 2, 3, 4, 5]

result = ( for number in numbers:
    if number > 2:
      
    print(result)
)

try:
    number = int(input("Enter a number: "))
    result = 100 / number
    print(result)
except ValueError:
    print("Invalid number")
except ZeroDivisionError:
    print("Cannot divide by zero")'''


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"My name is {self.name}\ and I am {self.age} years old.")
              
person = Person("Mohamed", 25)
person.introduce()

data = {
    "sales": [100, 200, 300],
    "stores": ["A", "B", "C"],
}

for key, values in data.items():
    print(f"{key}: {values}")

if len(data["sales"]) == len(data["stores"]):
    print("Data is consistent")
else:
    print("Data is inconsistent")

def process_data(data):
    if not data:  # i love it 
        return None

    processed = []
    for item in data:
        if isinstance(item, int):
            processed.append(item * 2)
        elif isinstance(item, str):
            processed.append(item.upper())
        else:
            processed.append(item)

    return processed

print(process_data([1, "hello", 3, None]))


numbers = [1, 2, 3, 4, 5]

for number in numbers:
    if number % 2 == 0:
        result = number ** 2
    elif number % 3 == 0:
        result = number ** 3
    else:
        result = number

    print(f"{number} -> {result}")

print("Finished")


numbers = [1, 2, 3, 4, 5]
# i have to understand list comprehension

for number in numbers:
    if number > 2:
        result =  number * 2
        print(result)
''' to become good at debugging syntax errors, you need to deeply understand and internalize the       
 grammar and structural patterns of the language....
 The more code you read,write ,and debug , the more that grammar becomes automatic'''

numbers = [1, 2, 3, 4, 5]
squares=[number**2 for number in numbers]
print(squares)

even_numbers=[number for number in numbers if number%2==0]
print(even_numbers)

result=[number*10 for number in numbers if number>3]
print(result)

names = ["mohamed", "ali", "sara", "ahmed"]
upper_names=[name.upper() for name in names]
print(upper_names)

tricky=[number**2 for number in numbers if number%2==0 if number>2]
print(tricky)
'''
def divide(a, b):
        try:
            c=a+b
            return c
        finally:
            print(c)
        

divide(2,4) 


average = lambda numbers: total = sum(numbers) / len(numbers)
print(average([1, 2, 3]))


count = 0

def increment():
    nonlocal count
    count += 1
    return count

print(increment())


a, *b, *c = [1, 2, 3, 4, 5]
print(a, b, c)



async def fetch():
    data = await get_data()
    return data

result = await fetch()
print(result)


def divide(a, b):
    try:
        return a / b
    finally:
        continue


average = lambda numbers: total = sum(numbers) / len(numbers)
print(average([1, 2, 3]))

'''



from math import sqrt
print(sqrt(16))

import math
print(math.sqrt(25))

from math import *
print(sqrt(49))

def greet(prefix,name="Guest"):
    return prefix + " " + name

print(greet("Mr.", "Ali"))


numbers = [10, 0, 20, 0, 30]

for n in numbers:
    try:
        result = 100 / n
        print(result)
    except ZeroDivisionError:
        print("Skipping zero")
        #continue   # ← valid: jumps to next iteration



for n in numbers:
    try:
        result = 100 / n
    except ZeroDivisionError:
        print("Skipping zero")
        continue        # ← needed! Without it, we'd try to print undefined 'result'
    
    print(f"Success: {result}")
    




