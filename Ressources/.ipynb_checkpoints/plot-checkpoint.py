import matplotlib.pyplot as plt
import numpy as np


def circle(x_center, y_center, z_center, radius, ax, color='red'):
    for theta in range(0, 360, 3):
        x = x_center
    y = y_center + radius * np.cos(theta)
    z = z_center + radius * np.sin(theta)
    ax.scatter3D(x, y, z, s=0.1, c=color)


def plot_nodes(NL, ax):
    # Get node coordinates
    xdata = NL[:, 0]
    ydata = NL[:, 1]
    zdata = NL[:, 2]
    # Visualize 3D Nodes
    ax.scatter3D(xdata, ydata, zdata)


def Read_Node_List(filename):
    f = open(filename, 'r')
    data = f.read()
    f.close

    lines = data.splitlines()
    lines.remove(lines[0])
    NoN = len(lines)
    PD = len(lines[0].strip().split()) - 1
    print('dim = ', PD, 'Nbr of Nodes = ', NoN)

    NL = np.zeros([NoN, PD])
    for idx, line in enumerate(lines):
        print(line.strip().split())
        NL[idx, 0] = line.strip().split()[1]  # x
        NL[idx, 1] = line.strip().split()[2]  # y
        NL[idx, 2] = line.strip().split()[3]  # z
        print('x = ', line.strip().split()[1])  # x
        print('y = ', line.strip().split()[2])  # x
        print('z = ', line.strip().split()[3])  # x
        print(NL)
    return NL


# Node List :
NL = np.array([[0, 0, 0],
               [1, 0, 0],
               [3, 0, 0],
               [4, 0, 0]])

# Element List :
EL = np.array([[0, 1],
               [1, 2],
               [2, 3]])

PD = np.size(NL, 1)
NoN = np.size(NL, 0)
NoE = np.size(EL, 0)
print('===== Pb caracteritics =======')
print('dim = ', PD, 'Nbr of Nodes = ', NoN)
fig = plt.figure(figsize=plt.figaspect(1) * 2)
ax = fig.add_subplot(projection='3d')
plot_nodes(NL, ax)
# Get element coordinates
for i in range(NoE):
    node1 = EL[i, 0]
    node2 = EL[i, 1]
    print('element ', i, ' : from node ', node1, ' to node ', node2)
    xline = np.linspace(NL[node1, 0], NL[node2, 0], 100)
    yline = np.linspace(NL[node1, 1], NL[node2, 1], 100)
    zline = np.linspace(NL[node1, 2], NL[node2, 2], 100)
    # Visualize 3D elements
    ax.plot3D(xline, yline, zline, c='black')

x_center, y_center, z_center, radius = 0, 0, 0, 0.5
circle(x_center, y_center, z_center, radius, ax)

# Give labels
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
# Save figure
plt.savefig('3d_scatter.png', dpi=300, bbox_inches='tight', pad_inches=0.1);
# plt.show()
fig = plt.figure(figsize=plt.figaspect(1) * 2)
ax = fig.add_subplot(projection='3d')
filename = 'Mesh.txt'
Read_Node_List(filename)
NL = Read_Node_List(filename)
plot_nodes(NL, ax)
plt.show()
