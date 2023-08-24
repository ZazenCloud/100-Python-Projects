# Problem 1

'''
number = int(input("Which number do you want to check? "))

if number % 2 = 0:
  print("This is an even number.")
else:
  print("This is an odd number.")
'''

'''
  File "main.py", line 3
    if number % 2 = 0:
                  ^
SyntaxError: invalid syntax
'''

# Single equal sign means assignment (value to variable)
# Double equal signs means evaluation (True or False)
# In this case, we want evaluation

number = int(input("Which number do you want to check? "))

if number % 2 == 0:
    print("This is an even number.")
else:
    print("This is an odd number.")


# Problem 2

'''
year = input("Which year do you want to check?  ")

if year % 4 == 0:
  if year % 100 == 0:
    if year % 400 == 0:
      print("Leap year.")
    else:
      print("Not leap year.")
  else:
    print("Leap year.")
else:
  print("Not leap year.")
'''

'''
  File "main.py", line 3, in <module>
    if year % 4 == 0:
TypeError: not all arguments converted during string formatting
'''

# type(year) -> str
# type(4) -> int
# The input function takes an input from the console as a string
# Therefore, it should be converted to int

year = int(input("Which year do you want to check?"))

if year % 4 == 0:
    if year % 100 == 0:
        if year % 400 == 0:
            print("Leap year.")
        else:
            print("Not leap year.")
    else:
        print("Leap year.")
else:
    print("Not leap year.")


# Problem 3

'''
for number in range(1, 101):
  if number % 3 == 0 or number % 5 == 0:
    print("FizzBuzz")
  if number % 3 == 0:
    print("Fizz")
  if number % 5 == 0:
    print("Buzz")
  else:
    print([number])
'''

'''
No errors, but output is not correct
[1]
[2]
FizzBuzz
Fizz
[3]
...
'''

# OR statement in line 2 will print "FizzBuzz" for
# very number divisible by 3 OR 5
# It should be an AND statement

# There are multiple if statements being triggered
# Elif statements should be implemented
# instead of the second and third if statement

# The number variable is enclosed in brackets in the last print statement
# Removing the brackets makes the code cleaner

for number in range(1, 101):
    if number % 3 == 0 and number % 5 == 0:
        print("FizzBuzz")
    elif number % 3 == 0:
        print("Fizz")
    elif number % 5 == 0:
        print("Buzz")
    else:
        print(number)
