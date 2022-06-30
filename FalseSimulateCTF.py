import math
import random


class simulate:
    def __init__(self, sim):
        self.reset()
        self.sim = sim

    def reset(self):
        file = open("neural_networksFalse.dat", "r")

        self.neural_networks = file.read()[1:-1]
        # print(self.neural_networks)
        self.neural_networks = self.neural_networks.split('], [')
        # print(self.neural_networks)
        self.neural_networks = [network.replace("[", "") for network in self.neural_networks]
        self.neural_networks = [network.replace("]", "") for network in self.neural_networks]
        # print(self.neural_networks)
        self.neural_networks = [network.split(', ') for network in self.neural_networks]
        # print(self.neural_networks)

        self.neural_networks = [[numeral_string.replace("'", "") for numeral_string in arr] for arr in
                                self.neural_networks]

        file.close()

        self.enemyhasflag = False
        self.playerhasflag = False

        self.player = {
            "x": 16,
            "y": 22
        }
        self.playerstart = {
            "x": 16,
            "y": 22
        }
        self.pflag = {
            "x": 16,
            "y": 23
        }

        self.enemy = {
            "x": 16,
            "y": 4
        }
        self.enemystart = {
            "x": 16,
            "y": 4
        }
        self.eflag = {
            "x": 16,
            "y": 3
        }

    def eai(self, tick, sim):
        initial_weight = 0
        second_weight = 0
        enemy_internal_1 = 0
        enemy_internal_2 = 0
        enemy_internal_3 = 0
        enemy_internal_4 = 0

        output_weights = {
            "17": 0,
            "18": 0,
            "19": 0,
            "20": 0,
            "21": 0
        }

        for connection in self.neural_networks[(2 * sim) - 2]:
            if connection[-9:-7] == "10":
                initial_weight = random.random()
            elif connection[-9:-7] == "11":
                if (self.enemyhasflag):
                    initial_weight = 1
                else:
                    initial_weight = 0
            elif connection[-9:-7] == "12":
                if (self.playerhasflag):
                    initial_weight = 1
                else:
                    initial_weight = 0
            elif connection[-9:-7] == "13":
                initial_weight += enemy_internal_1
            elif connection[-9:-7] == "14":
                initial_weight += enemy_internal_2
            elif connection[-9:-7] == "15":
                initial_weight += enemy_internal_3
            elif connection[-9:-7] == "16":
                initial_weight += enemy_internal_4
            elif connection[-8] == "1":
                initial_weight = (self.enemy["x"] - 16) / 16
            elif connection[-8] == "2":
                initial_weight = (self.enemy["y"] - 13) / 13
            elif connection[-8] == "3":
                initial_weight = math.sin(tick)
            elif connection[-8] == "4":
                initial_weight = math.tan(tick)
            elif connection[-8] == "5":
                initial_weight = (self.enemy["x"] - self.player["x"]) / 16
            elif connection[-8] == "6":
                initial_weight = (self.enemy["y"] - self.player["y"]) / 16
            elif connection[-8] == "7":
                initial_weight = -((self.pflag["x"] - self.enemy["x"]) / 16)
            elif connection[-8] == "8":
                initial_weight = -((self.pflag["y"] - self.enemy["y"]) / 16)
            elif connection[-8] == "9":
                if self.player["y"] < 13:
                    initial_weight = 1
                else:
                    initial_weight = 0

            if connection[-5] == "0":
                second_weight = initial_weight + (int(connection[-4:]) / 1000)
            elif connection[-5] == "1":
                second_weight = initial_weight - (int(connection[-4:]) / 1000)
            elif connection[-5] == "2":
                second_weight = initial_weight * (int(connection[-4:]) / 1000)
            elif connection[-5] == "3":
                second_weight = initial_weight / (int(connection[-4:]) / 1000)

            if connection[-7:-5] == "13":
                enemy_internal_1 += second_weight
            elif connection[-7:-5] == "14":
                enemy_internal_2 += second_weight
            elif connection[-7:-5] == "15":
                enemy_internal_3 += second_weight
            elif connection[-7:-5] == "16":
                enemy_internal_4 += second_weight

            try:
                output_weights[connection[-7:-5]] += second_weight
            except:
                pass

        index = 17
        biggest = 17
        while index <= 21:
            if output_weights[str(index)] > output_weights[str(biggest)]:
                biggest = int(index)
            index += 1

        if biggest == 17:
            self.enemy["y"] += 1
        elif biggest == 18:
            self.enemy["y"] -= 1
        elif biggest == 19:
            self.enemy["x"] -= 1
        elif biggest == 20:
            self.enemy["x"] += 1
        elif biggest == 21:
            r = random.randint(0, 3)
            if r == 0:
                self.enemy["y"] += 1
            elif r == 0:
                self.enemy["y"] -= 1
            elif r == 0:
                self.enemy["x"] += 1
            elif r == 0:
                self.enemy["x"] -= 1

    def pai(self, tick, sim):
        initial_weight = 0
        second_weight = 0
        player_internal_1 = 0
        player_internal_2 = 0
        player_internal_3 = 0
        player_internal_4 = 0

        output_weights = {
            "17": 0,
            "18": 0,
            "19": 0,
            "20": 0,
            "21": 0
        }

        for connection in self.neural_networks[(2 * sim) - 1]:
            if connection[-9:-7] == "10":
                initial_weight = random.random()
            elif connection[-9:-7] == "11":
                if (self.playerhasflag):
                    initial_weight = 1
                else:
                    initial_weight = 0
            elif connection[-9:-7] == "12":
                if (self.enemyhasflag):
                    initial_weight = 1
                else:
                    initial_weight = 0
            elif connection[-9:-7] == "13":
                initial_weight += player_internal_1
            elif connection[-9:-7] == "14":
                initial_weight += player_internal_2
            elif connection[-9:-7] == "15":
                initial_weight += player_internal_3
            elif connection[-9:-7] == "16":
                initial_weight += player_internal_4
            elif connection[-8] == "1":
                initial_weight = -((self.player["x"] - 16) / 16)
            elif connection[-8] == "2":
                initial_weight = -((self.player["y"] - 13) / 13)
            elif connection[-8] == "3":
                initial_weight = math.sin(tick)
            elif connection[-8] == "4":
                initial_weight = math.tan(tick)
            elif connection[-8] == "5":
                initial_weight = -((self.player["x"] - self.enemy["x"]) / 16)
            elif connection[-8] == "6":
                initial_weight = -((self.player["y"] - self.enemy["y"]) / 16)
            elif connection[-8] == "7":
                initial_weight = -((self.player["x"] - self.eflag["x"]) / 16)
            elif connection[-8] == "8":
                initial_weight = -((self.player["y"] - self.eflag["y"]) / 16)
            elif connection[-8] == "9":
                if self.player["y"] < 13:
                    initial_weight = 1
                else:
                    initial_weight = 0

            if connection[-5] == "0":
                second_weight = initial_weight + (int(connection[-4:]) / 1000)
            elif connection[-5] == "1":
                second_weight = initial_weight - (int(connection[-4:]) / 1000)
            elif connection[-5] == "2":
                second_weight = initial_weight * (int(connection[-4:]) / 1000)
            elif connection[-5] == "3":
                second_weight = initial_weight / (int(connection[-4:]) / 1000)

            if connection[-7:-5] == "13":
                player_internal_1 += second_weight
            elif connection[-7:-5] == "14":
                player_internal_2 += second_weight
            elif connection[-7:-5] == "15":
                player_internal_3 += second_weight
            elif connection[-7:-5] == "16":
                player_internal_4 += second_weight

            try:
                output_weights[connection[-7:-5]] += second_weight
            except:
                pass

        index = 17
        biggest = 17
        while index <= 21:
            if output_weights[str(index)] > output_weights[str(biggest)]:
                biggest = int(index)
            index += 1

        if biggest == 17:
            self.player["y"] -= 1
        elif biggest == 18:
            self.player["y"] += 1
        elif biggest == 19:
            self.player["x"] += 1
        elif biggest == 20:
            self.player["x"] -= 1
        elif biggest == 21:
            r = random.randint(0, 3)
            if r == 0:
                self.player["y"] += 1
            elif r == 0:
                self.player["y"] -= 1
            elif r == 0:
                self.player["x"] += 1
            elif r == 0:
                self.player["x"] -= 1

    def simulate(self, result, index):
        self.reset()
        tick = 1
        pscore = 0
        escore = 0
        winner = 0

        while True:
            tick += 1
            turn = random.randint(0, 1)

            if turn == 1:
                self.pai(tick, self.sim)
                self.eai(tick, self.sim)
            else:
                self.eai(tick, self.sim)
                self.pai(tick, self.sim)

            if self.enemy["x"] == 0:
                self.enemy["x"] = 1
            elif self.enemy["x"] == 32:
                self.enemy["x"] = 31
            elif self.enemy["y"] == 1:
                self.enemy["y"] = 2
            elif self.enemy["y"] == 25:
                self.enemy["y"] = 24

            if self.player["x"] == 0:
                self.player["x"] = 1
            elif self.player["x"] == 32:
                self.player["x"] = 31
            elif self.player["y"] == 1:
                self.player["y"] = 2
            elif self.player["y"] == 25:
                self.player["y"] = 24

            if self.playerhasflag == True:
                if self.enemyhasflag == True:
                    if self.player["y"] > 13:
                        if self.enemy["y"] < 13:
                            break

            if self.player["y"] == self.eflag["y"]:
                if self.player["x"] == self.eflag["x"]:
                    if self.playerhasflag == False:
                        self.playerhasflag = True
                        pscore += 3
            if self.playerhasflag == True:
                if self.player["y"] > 13:
                    winner = 1
                    break

            if self.enemy["y"] == self.pflag["y"]:
                if self.enemy["x"] == self.pflag["x"]:
                    if self.enemyhasflag == False:
                        self.enemyhasflag = True
                        escore += 3
            if self.enemyhasflag == True:
                if self.enemy["y"] < 13:
                    winner = 2
                    break

            if self.enemy["y"] == self.player["y"]:
                if self.enemy["x"] == self.player["x"]:
                    if self.player["y"] > 13:
                        self.enemy = dict(self.enemystart)
                        self.enemyhasflag = False
                        pscore += 2

            if self.enemy["y"] == self.player["y"]:
                if self.enemy["x"] == self.player["x"]:
                    if self.enemy["y"] < 13:
                        self.player = dict(self.playerstart)
                        self.playerhasflag = False
                        escore += 2

            if winner != 0:
                break
            if tick >= 100:
                break

        if winner == 1:
            pscore += 1000
        elif winner == 2:
            escore += 1000

        if (pscore and escore) >= 1000:
            if pscore < escore:
                winscore = [1, pscore, self.sim]
            elif escore < pscore:
                winscore = [2, escore, self.sim]
        elif pscore > escore:
            winscore = [1, pscore, self.sim]
        elif escore > pscore:
            winscore = [2, escore, self.sim]
        else:
            winscore = [0, 0, 0]

        result[index] = winscore
