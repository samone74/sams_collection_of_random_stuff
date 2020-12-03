import random
class woordje:
    def __init__(self, word1, word2):
        self.lang = []
        self.lang.append(word1)
        self.lang.append(word2)
        self.count = 0

#Woord laten zien als fout getypt
#Laatste gevraagrd woord niet meteen wee vragen
#woorden die nog niet gewees zijn hogere kans geven om langs te komen
#Bijhouden hoever iemand is
#Scherm leegmaken bij elk nieuw woord


def main():
    list_woorden = []
    list_woorden.append(woordje('Amerika','America'))
    list_woorden.append(woordje('België','Belgium'))
    list_woorden.append(woordje('land','country'))
    list_woorden.append(woordje('e-mail','email'))
    list_woorden.append(woordje('Engeland','England'))
    list_woorden.append(woordje('vriend','friend'))
    list_woorden.append(woordje('honderd','hundred'))
    list_woorden.append(woordje('Italië','Italy'))
    list_woorden.append(woordje('brief','letter'))
    list_woorden.append(woordje('nummer','number'))
    list_woorden.append(woordje('mensen','people'))
    list_woorden.append(woordje('wonen','to live'))
    list_woorden.append(woordje('vrouw','woman'))
    list_woorden.append(woordje('wereld','world'))
    list_woorden.append(woordje('jaar','year'))

    index = 0;
    index2 = 1;
    while(len(list_woorden) != 0):
        ind = random.randint(0, len(list_woorden) - 1)

        if(list_woorden[ind].count == 0):
            print(list_woorden[ind].lang[index] +" is vertaald " + list_woorden[ind].lang[index2])
            print("Type na " + list_woorden[ind].lang[index2])
        else:
            print("Vertaal " + list_woorden[ind].lang[index])
        test = input()

        if(test == list_woorden[ind].lang[index2]):
            print("Goed gedaan")
            list_woorden[ind].count += 1
            if(list_woorden[ind].count > 2):
                print(list_woorden[ind].lang[index] + " ken je nu goed genoeg")
                del list_woorden[ind]
        else:
            print("Jammer dat is fout")
    print("Je kent alles je bent klaar goed gedaan")
if __name__ == '__main__':
    main()