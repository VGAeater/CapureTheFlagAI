import os
import random

neural_networks = []

input_start = int(input("Input_start: "))
internal_start = int(input("Internal_start: "))
internal_end = int(input("Internal_end: "))
output_end = int(input("Output_end: "))
networks = int(input("Networks: "))
connections = int(input("Connections: "))
link = ""

for network in range(networks):
    neural_networks.append([])
    for connection in range(connections):
        neural_networks[network].append([])

        link = str(random.randint(input_start, internal_end))
        link = link + str(random.randint(internal_start, output_end))

        link = link + str(random.randint(0, 3))
        weight = str(random.randint(0, 9999))

        if int(weight) < 1000:
            weight = "0" + weight
        if int(weight) < 100:
            weight = "0" + weight
        if int(weight) < 10:
            weight = "0" + weight
        link = link + weight
        link = int(link)

        neural_networks[network][connection] = link

os.system('clear')
print(neural_networks)

file = open("neural_networksTrue.dat", "w")
file.write(str(neural_networks))
file.close()
file = open("neural_networksFalse.dat", "w")
file.write(str(neural_networks))
file.close()
