
"""
Spiel "Zahlenraten", in Python programmiert.
"""

import random


guess_count = 0
repeat = 1
1
print('Zahlenraten')
while repeat == 1:
    print('Bereich auswählen')
    minBereich = int(input('Min Wert: '))
    maxBereich = int(input('Max Wert: '))
    while minBereich<0:
        print('Min Wert muss größer 0 sein')
        minBereich = int(input('Min Wert: '))
    while maxBereich<0:
        print('Max Wert muss größer 0 sein')
        maxBereich = int(input('Max Wert: '))
    while minBereich>=maxBereich:
        print('Min größer als Max. Bitte neu eingeben!')
        minBereich = int(input('Min Wert: '))
        maxBereich = int(input('Max Wert: '))
    
            
        # initialisiere des Zufallszahlengenerators
    random.seed()
    # erzeuge neue Zufallszahl zwischen 1 und 100
    correct_answer = random.randint(minBereich,maxBereich)


    player_input = 0



    # solange der Spieler noch nicht die richtige Antwort eingegebe hat...
    while player_input != correct_answer:
        # lese Eingabe vom Spieler ein und parse den eingegebenen String zu einer Ganzzahl (int)
        player_input = int(input('Zahl eingeben: '))
        # vergleiche Eingabe mit der richtigen Antwort
        if player_input > correct_answer:
            print('Zahl zu groß!')
            guess_count+=1
        elif player_input < correct_answer:
            print('Zahl zu klein!')
            guess_count+=1
        else:
            guess_count+=1
            print('Sie haben gewonnen!')
            if guess_count==1:
                print('Sie haben ',guess_count,'Versuch gebraucht')
            else:
                print('Sie haben ',guess_count,'Versuche gebraucht')
    print('Neues Spiel?')
    print(' [1] Ja ')
    print(' [2] Nein')
    repeat= int(input())