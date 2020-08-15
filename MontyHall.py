import random

switch = 0
stay = 0
TRIALS = 10000

i = 0
while i < TRIALS:
    doors = [1, 2, 3]
    car = random.randint(1, 3)
    contestant = random.randint(1,3)
    print("The car is behind door number", car)
    print("The contestant chooses door number", contestant)
    doors.remove(car)
    if car != contestant:
        doors.remove(contestant)
    if len(doors) == 1:
        print("Monty shows a herd of goats behind door number", doors[0])
        print("Monty asks the contestant if they want to switch doors...")
        print("The contestant picked a different door than the winning door, so the contestant wins if they switch")
        switch += 1
    else:
        monty = random.randint(0, 1)
        print("Monty shows a herd of goats behind door number", doors[monty])
        print("Monty asks the contestant if they want to switch doors...")
        print("The contestant picked the same door than the winning door, so the contestant loses if they switch")
        stay += 1
    i += 1
    print()

print()
sel = [int(TRIALS == 1), int(switch == 1), int(stay == 1)]
trials = ["Out of the " + str(TRIALS) + " trials", "In our single trial"]
swtimes = [" " + str(switch) + " times", ""]
sttimes = [" times", " time"]
print(trials[sel[0]] + ", the contestant wins" + swtimes[sel[1]] + " if they switch,")
print("and " + str(stay) + sttimes[sel[2]] + " if they stay with their original choice")






