import random


class change():
    def __init__(self):
        self.reset()

    def reset(self):
        file = open("neural_networksFalse.dat", "r")

        self.neural_networks = file.read()[1:-1]
        self.neural_networks = self.neural_networks.split('], [')
        self.neural_networks = [network.replace("[", "") for network in self.neural_networks]
        self.neural_networks = [network.replace("]", "") for network in self.neural_networks]
        self.neural_networks = [network.split(', ') for network in self.neural_networks]

        file.close()

    def change(self, to_change, to_keep):
        self.reset()
        connections = self.neural_networks[to_keep]
        # print(connections)

        elements = len(connections) - 1

        element = random.randint(0, elements)
        strand = connections[element]
        # print(strand)

        strand = list(str(strand))
        index = random.randint(1, 9)
        change_to = random.randint(1, 9)

        if index == 9:
            if len(strand) == 8:
                strand.insert(0, str(change_to))
            else:
                strand[-9] = str(change_to)
            number = str((int("".join(strand[-9:-7])) % 16) + 1)
            strand[-9:-7] = number.split()
        elif index == 8:
            strand[-8] = str(change_to)
            number = str((int("".join(strand[-9:-7])) % 16) + 1)
            strand[-9:-7] = number.split()
        elif index == 7:
            strand[-7] = str(change_to)
            number = str((int("".join(strand[-7:-5])) % 9) + 13)
            strand[-7:-5] = number.split()
        elif index == 6:
            strand[-6] = str(change_to)
            number = str((int("".join(strand[-7:-5])) % 9) + 13)
            strand[-7:-5] = number.split()
        elif index == 5:
            strand[-5] = str(change_to)
            number = str(int(strand[-5]) % 4)
            strand[-5] = number
        elif index == 4:
            strand[-4] = str(change_to)
        elif index == 3:
            strand[-3] = str(change_to)
        elif index == 2:
            strand[-2] = str(change_to)
        elif index == 1:
            strand[-1] = str(change_to)

        strand = "".join(strand)
        # print(strand)

        self.neural_networks[to_change][element] = strand
        # print(self.neural_networks)
        self.neural_networks = [[int(numeral_string) for numeral_string in arr] for arr in self.neural_networks]
        # print(self.neural_networks)

        try:
            file = open("neural_networksFalse.dat", "w")
            file.write(str(self.neural_networks))
            file.close()
        except:
            file = open("neural_networksFalse.dat", "w")
            file.write(str(self.neural_networks))
            file.close()
