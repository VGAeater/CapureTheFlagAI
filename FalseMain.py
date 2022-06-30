from FalseChange import change
from FalseSimulateCTF import simulate
import threading, time

sims = [
    simulate(1),
    simulate(2),
    simulate(3),
    simulate(4),
    simulate(5),
    simulate(6),
    simulate(7),
    simulate(8)
]
cha = change()
mutation = 0
winscore = [None] * 8
results = [None] * 8
threads = [None] * 8
greatest_score = [0, 0, 0]
besthistfile = open("besthistoryFalse.txt", 'w')
histfile = open("historyFalse.txt", 'w')

while True:
    try:
        temp_greatest_score = [0, 0, 0]

        mutation += 1
        print(mutation)

        for i in range(8):
            threads[i] = threading.Thread(target=sims[i].simulate, args=[results, i])
            threads[i].start()
        for i in range(8):
            threads[i].join()

        winscore = results

        for score in winscore:
            if score[1] >= 1000 and temp_greatest_score[1] >= 1000:
                if score[1] < temp_greatest_score[1]:
                    temp_greatest_score = list(score)
            elif score[1] > temp_greatest_score[1]:
                temp_greatest_score = list(score)

        if temp_greatest_score[1] >= 1000 and greatest_score[1] >= 1000:
            if temp_greatest_score[1] <= greatest_score[1]:
                greatest_score = list(temp_greatest_score)
        elif temp_greatest_score[1] >= greatest_score[1]:
            greatest_score = list(temp_greatest_score)

        besthistfile.write(str(str(greatest_score)+';'))
        histfile.write(str(str(temp_greatest_score)+';'))

        print(temp_greatest_score)
        print(greatest_score)

        for network in range(16):
            if (((greatest_score[2] * 2) - greatest_score[0]) != network) and (((temp_greatest_score[2] * 2) - temp_greatest_score[0]) != network):
                cha.change(network, ((greatest_score[2] * 2) - greatest_score[0]))
    except KeyboardInterrupt:
        besthistfile.close()
        histfile.close()