import math
import os
import random
import sys
import termios
import threading
import time
import tty


class simulate:
    def __init__(self):
        self.orig_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)

        self.move = ""

        TrueFalse = bool(input("True or False: "))
        if (TrueFalse == True):
            file = open("neural_networksTrue.dat", "r")
        elif (TrueFalse == False):
            file = open("neural_networksFalse.dat", "r")

        self.neural_networks = file.read()[1:-1]
        self.neural_networks = self.neural_networks.split('], [')
        self.neural_networks = [network.replace("[", "") for network in self.neural_networks]
        self.neural_networks = [network.replace("]", "") for network in self.neural_networks]
        self.neural_networks = [network.split(', ') for network in self.neural_networks]

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

    def raw(string: str, replace: bool = False) -> str:
        r = repr(string)[1:-1]  # Strip the quotes from representation
        if replace:
            r = r.replace('\\\\', '\\')
        return r

    def line(self, y):
        if (y == 1) is not True:
            line = "|"
        else:
            line = "_"
        x = 1
        while x < 32:
            if y == self.player['y']:
                if x == self.player['x']:
                    line = line + "P"
                    x += 1
                    continue

            if y == self.pflag['y']:
                if x == self.pflag['x']:
                    if self.enemyhasflag == False:
                        line = line + "#"
                        x += 1
                        continue

            if y == self.enemy['y']:
                if x == self.enemy['x']:
                    line = line + "E"
                    x += 1
                    continue

            if y == self.eflag['y']:
                if x == self.eflag['x']:
                    if self.playerhasflag == False:
                        line = line + "#"
                        x += 1
                        continue

            if y == 13:
                line = line + "-"
            elif y == 1 or y == 24:
                line = line + "_"
            else:
                line = line + " "

            x += 1
            continue

        if y != 1:
            line = line + "|"
        else:
            line = line + "_"
        return line

    def eai(self, tick, sim, player):
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

        for connection in self.neural_networks[(2 * sim) - player]:
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

    def listenthread(self):
        try:
            while True:
                keyin = sys.stdin.read(1)[0]
                if keyin == "\x1b":
                    keyin = sys.stdin.read(1)[0]
                    if keyin == "[":
                        keyin = sys.stdin.read(1)[0]
                        if keyin == "A":
                            self.move = "A"
                        elif keyin == "B":
                            self.move = "B"
                        elif keyin == "C":
                            self.move = "C"
                        elif keyin == "D":
                            self.move = "D"
        except:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.orig_settings)

    def simulate(self, sim, player):
        y = 1
        tick = 1
        canmove = True

        thread = threading.Thread(target=self.listenthread, args=())

        thread.start()

        while True:
            print(self.line(y))
            y += 1

            if y == 25:
                tick += 1
                turn = random.randint(0, 1)

                if canmove == True:
                    if self.move == "A":
                        self.player["y"] -= 1
                        canmove = False
                        self.move = ""
                    elif self.move == "B":
                        self.player["y"] += 1
                        canmove = False
                        self.move = ""
                    elif self.move == "C":
                        self.player["x"] += 1
                        canmove = False
                        self.move = ""
                    elif self.move == "D":
                        self.player["x"] -= 1
                        canmove = False
                        self.move = ""
                else:
                    canmove = True

                if (turn % 2) == 0:
                    self.eai(tick, sim, player)

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
                                print("tie!")
                                break

                if self.player["y"] == self.eflag["y"]:
                    if self.player["x"] == self.eflag["x"]:
                        if self.playerhasflag == False:
                            self.playerhasflag = True
                if self.playerhasflag == True:
                    if self.player["y"] > 13:
                        print("you win!")
                        break

                if self.enemy["y"] == self.pflag["y"]:
                    if self.enemy["x"] == self.pflag["x"]:
                        if self.enemyhasflag == False:
                            self.enemyhasflag = True
                if self.enemyhasflag == True:
                    if self.enemy["y"] < 13:
                        print("you lose!")
                        break

                if self.enemy["y"] == self.player["y"]:
                    if self.enemy["x"] == self.player["x"]:
                        if self.player["y"] > 13:
                            self.enemy = dict(self.enemystart)
                            self.enemyhasflag = False

                if self.enemy["y"] == self.player["y"]:
                    if self.enemy["x"] == self.player["x"]:
                        if self.enemy["y"] < 13:
                            self.player = dict(self.playerstart)
                            self.playerhasflag = False

                time.sleep(.1)
                os.system('clear')
                y = 1
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.orig_settings)
