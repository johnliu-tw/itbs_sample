number = 35
answer = 0

if number <= 10:
    answer = number * 8
elif number > 10 and number <= 20:
    answer = 10 * 8 + ( number - 10 )*2
else:
    answer = 100

print(answer)