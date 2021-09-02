from datetime import timedelta, datetime

x = datetime.now()
sum = 0 
for i in range(10000):
    sum += 1
y = datetime(2021, 7, 6)

print(y-x > timedelta(days = 1))