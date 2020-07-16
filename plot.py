import matplotlib.pyplot as plt


def graph_team(team_name, points):

    weeks = [i for i in range(len(points))]
    plt.plot(weeks, points, "o-r")
    plt.ylabel('APD')
    plt.xlabel("Weeks")
    plt.show()
