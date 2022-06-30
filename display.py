# importing the required module
from matplotlib import pyplot as plt

besthist = open("besthistoryTrue.txt", 'r').read()
hist = open("historyTrue.txt", 'r').read()

besthist = [arr.replace('[', '').replace(']', '').split(', ') for arr in besthist.split(';')]
hist = [arr.replace('[', '').replace(']', '').split(', ') for arr in hist.split(';')]
besthist = [[int(num) for num in besthist[i]] for i in range(len(besthist)-1)]
hist = [[int(num) for num in hist[i]] for i in range(len(hist)-1)]

x = [i for i in range(len(hist))]
y = [arr[1] for arr in hist]
bx = [i for i in range(len(besthist))]
by = [arr[1] for arr in besthist]

plt.plot(x, y)
plt.plot(bx, by)

plt.xlabel('Generation')
plt.ylabel('Points')

plt.title('AI')

plt.show()
