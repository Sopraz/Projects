''' Black Jack '''
import time
import random
import sys

"""
mise
tirage
attribution des points
si la mise
"""
print('Bienvenue au jeu du BLACK JACK !')
capital = int(input('Quel est votre capital : '))

numero = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Valle','Dame','Roi','As']
couleurs = ['Coeur','Carreau','Pique','Trefle']
jeuentier = []
for i in couleurs:
    for g in numero:
        jeuentier.append(str(g)+ ' de '+ i)
def main():
    global capital

    partie()
    if capital >0:
        continuer = input('Voulez vous rejouer ? (y/n)')
        if continuer == ('y' or 'yes' or 'oui' or 'o'):
            main()
        else:
            print("D'accord, vous repartez avec un montant de ", capital,'euros')
            sys.exit()
    else:
        print('No money left sorry...')




def melange(jeu):
    random.shuffle(jeu)
    return jeu


def partie():
    global jeuentier
    global capital
    if capital >0:
        mise = int(input('Quel est votre mise ?'))
        deck = jeuentier[:]
        melange(deck)
        jeujoueur = []
        jeucroupier = []
        for loop in range(2):
            carte = tirage(deck)
            jeujoueur.append(carte)
        for loop in range(2):
            carte = tirage(deck)
            jeucroupier.append(carte)

        valeur1 = 0
        valeur2 =0

        print('Le croupier pioche un :')
        # for i in jeucroupier:
        #     print(i)
        #     valeur2+= valeurs(i)
        print(jeucroupier[0])
        valeur2 += valeurs(jeucroupier[0])
        print()
        time.sleep(3)
        print('Votre jeu :')
        for i in jeujoueur:
            print(i)
            valeur1+= valeurs(i)
        print()



        v = True
        while v:
            if valeur1 >21:
                print('Vous avez perdu ... ')
                print("Votre capital s'eleve a : ", capital-mise,'euros')
                capital -= mise
                return
            elif valeur1 == 21:
                print('Black Jack ! ')
                print('Vous avez gagne !')
                mise*=2
                capital += mise
                print("Votre capital s'eleve a : ", capital,'euros')
                return
            else:
                voluntee = input('Voulez vous pochier une autre carte ? (y/n) ')
                if voluntee == ('y' or 'yes' or 'ye' or 'oui'):
                    cartess =  tirage(deck)
                    jeujoueur.append(cartess)
                    print(cartess)
                    valeur1+= valeurs(cartess)
                else:
                    v = False
        print('La deuxieme carte du croupier etait :', jeucroupier[1])
        valeur2 += valeurs(jeucroupier[1])
        print('valeur carte croupier',valeur2)
        while valeur2 <valeur1:

            jeucroupier.append(tirage(deck))
            print('le croupier a pioche :', jeucroupier[-1])
            valeur2+= valeurs(jeucroupier[-1])
            print('valeur carte croupier',valeur2)
            if valeur2 == 21:
                print('Black jack pour le croupier ! Vous avez perdu la partie ...')
                print("Votre capital s'eleve a : ", capital-mise,'euros')
                capital -= mise
                return
            elif valeur2 >21:
                print('Vous avez gagne !')
                mise*=2
                capital+= mise
                print("Votre capital s'eleve a : ", capital,'euros')
                print()
                return

        if valeur1>valeur2:
            print('Vous avez gagne !')
            mise *=2
            capital+= mise
            print("Votre capital s'eleve a : ", capital,'euros')
            return
        else:
            print('Vous avez perdu la partie.')
            capital -= mise
            print("Votre capital s'eleve a : ", capital,'euros')
            return

    else:
        print('No money left sorry ...')
        sys.exit()



def tirage(jeu):
    v = random.randint(0,len(jeu)-1)
    car= jeu[v]
    del jeu[v]
    return car

def valeurs(i):
    if i.split()[0] in ['Valle','Roi','Dame'] :
        k= 10
    elif 'As' in i:
        volonte = input('Voulez vous que le As soit un 1 ou un 11 ? (press 1 or 2) ')
        if volonte == '1':
            k=1
        else:
            k =11
    else:
        k= int(i.split()[0])
    return k


main()












