import matplotlib
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np


raw = [l.strip() for l in open("output.txt", "r").readlines()]
total_wins = {}
total_games = {}

position_int = {"TOP": 0, "JG": 1, "MID": 2, "ADC": 3, "SUPP": 4}

def str_to_tuple(s):
    al = s.replace("(", "").replace(")", "").replace(" ", "").split(",")
    return (al[0].replace("\'", ""), int(al[1]))


for gm in range(len(raw)//11):

    mean_score = 0
    for p in range(11*gm, 11*gm+10):
        pc = str_to_tuple(raw[p])
        mean_score += pc[1]
    mean_score /= 10

    for p in range(11*gm, 11*gm+10):
        pc = str_to_tuple(raw[p])
        cdiff = round(pc[1] - mean_score, 1)

        if((pc[0], cdiff) not in total_games):
            total_games[(pc[0], cdiff)] = 0
        total_games[(pc[0], cdiff)] += 1


    if(raw[11*gm+10] == "True"):
        for p in range(11*gm, 11*gm+5):
            pc = str_to_tuple(raw[p])
            cdiff = round(pc[1] - mean_score, 1)
            if((pc[0], cdiff) not in total_wins):
                total_wins[(pc[0], cdiff)] = 0
            total_wins[(pc[0], cdiff)] += 1
    else:
        for p in range(11*gm+5, 11*gm+10):
            pc = str_to_tuple(raw[p])
            cdiff = round(pc[1] - mean_score, 1)
            if((pc[0], cdiff) not in total_wins):
                total_wins[(pc[0], cdiff)] = 0
            total_wins[(pc[0], cdiff)] += 1



organized_wins = [[], [], [], [], []]

for e in total_wins:
    if(total_games[e] > 5):
        organized_wins[position_int[e[0]]].append((e[1], total_wins[e]/total_games[e]))

for i in range(5):
    analysis_position = i # position int

    x = [a[0] for a in organized_wins[analysis_position]]
    y = [a[1] for a in organized_wins[analysis_position]]

    x = np.array(x).reshape((-1, 1))
    y = np.array(y).reshape((-1, 1))

    reg = LinearRegression().fit(x, y)
    print("Position: " + str(i) + "\t\tcoeff: " + str(reg.coef_) + "\t\t r^2: " + str(reg.score(x, y)))

    plt.plot(*zip(*sorted(organized_wins[analysis_position])))
    plt.show()








