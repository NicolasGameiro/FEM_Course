import matplotlib.pyplot as plt
import numpy as np
plt.rcParams["figure.figsize"] = (15,6)

def plot_forces(ax, NL,  F) -> None:
    M = F

    """
    min_x = 1.5 * np.min(NL[:, 0])
    min_y = 1.5 * np.min(NL[:, 1])
    max_x = 1.5 * np.max(NL[:, 0])
    max_y = 1.5 * np.max(NL[:, 1])
    print(min_x,min_y,max_x,max_y)
    """

    scale_force = np.max(np.abs(F))//10
    print('==> scale force = ', scale_force*10)
    ax.quiver(NL[:,0], NL[:,1], F[:,0], F[:,1], color='r', angles='xy', scale_units='xy', scale=scale_force*10*2)
    plt.axis('equal')  # <-- set the axes to the same scale
    #plt.xlim([min_x, max_x])  # <-- set the x axis limits
    #plt.ylim([min_y, max_y])  # <-- set the y axis limits
    #plt.grid(b=True, which='major')  # <-- plot grid lines
    return


if __name__ == '__main__':
    NL = np.array([[0, 0],
                   [1, 0],
                   [0.5, 1]])

    Fu = np.array([[0, 0],
                   [0, 0],
                   [0, -20]])

    fig, axs = plt.subplots(2)
    fig.suptitle('Vertically stacked subplots')

    plot_forces(axs[0], NL, Fu)
    plt.show()
