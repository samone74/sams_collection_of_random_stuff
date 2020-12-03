import random

num =  random.randint(1, 900)
print('raad een getal tussen de 1 en de 900')
while True:

    raad = input()
    i = int(raad)
    if i == num:
        print('Je hebt het goed geraden')
        break
    if i < num:
        print('Probeer een hoger getal')
    if i > num:
        print('Probeer een lager getal')
    print('Probeer opnieuw')