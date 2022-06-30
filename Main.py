from SimulateCTF import simulate

sim = simulate()

try:
    sim.simulate(int(input("sim\n")), int(input("player, enemy = 1, player = 2")))
except Exception as err:
    print(err)
