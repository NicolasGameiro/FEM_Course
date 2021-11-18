import numpy as np
import math


def add_force(F, node, Fx, Fy):
    phrase = "=== Application d'une nouvelle force au noeud " + str(node) + " ==="
    print(phrase)
    try:
        F[node - 1, 0] = Fx
        F[node - 1, 1] = Fy
        print("nouvelle force : \n", F)
    except:
        print("le noeud choisi n'appartient pas aux noeuds possibles")
    print("=" * len(phrase), '\n')
    return F

def add_DorN(DorN, node, x, y):
    phrase = "=== Application d'une nouvelle condition limite au noeud " + str(node) + " ==="
    print(phrase)
    try:
        DorN[node - 1, 0] = x
        DorN[node - 1, 1] = y
        print("nouvelle force : \n", DorN)
    except:
        print("le noeud choisi n'appartient pas aux noeuds possibles")
    print("=" * len(phrase), '\n')
    return DorN

def Read_Node_List(filename):
    with open(filename, 'r') as f:
        data = f.read()

    print(f'=== Lecture du fichier de maillage : {filename} ===')

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


def assign_BCs(NL, ENL):
    PD = np.size(NL, 1)
    NoN = np.size(NL, 0)
    DOFs = 0
    DOCs = 0
    for i in range(0, NoN):
        for j in range(0, PD):
            if ENL[i, PD + j] == -1:
                DOCs -= 1
                ENL[i, 2 * PD + j] = DOCs
            else:
                DOFs += 1
                ENL[i, 2 * PD + j] = DOFs
    for i in range(0, NoN):
        for j in range(0, PD):
            if ENL[i, PD + j] < 0:
                ENL[i, 3 * PD + j] = abs(ENL[i, 2 * PD + j]) + DOFs
            else:
                ENL[i, 3 * PD + j] = abs(ENL[i, 2 * PD + j])
    DOCs = abs(DOCs)

    return ENL, DOFs, DOCs


def assemble_stiffness(ENL, EL, NL, E, A):
    NoE = np.size(EL, 0)
    NPE = np.size(EL, 1)
    PD = np.size(NL, 1)
    NoN = np.size(NL, 0)

    K = np.zeros([NoN * PD, NoN * PD])
    for i in range(0, NoE):
        nl = EL[i, 0:NPE]
        k = element_stiffness(nl, ENL, E, A)
        for r in range(0, NPE):
            for p in range(0, PD):
                for q in range(0, NPE):
                    for s in range(0, PD):
                        row = ENL[nl[r] - 1, p + 3 * PD]
                        column = ENL[nl[q] - 1, s + 3 * PD]
                        value = k[r * PD + p, q * PD + s]
                        K[int(row) - 1, int(column) - 1] = K[int(row) - 1, int(column) - 1] + value
    return K


def element_stiffness(nl, ENL, E, A):
    X1 = ENL[nl[0] - 1, 0]
    X2 = ENL[nl[0] - 1, 1]
    Y1 = ENL[nl[1] - 1, 0]
    Y2 = ENL[nl[1] - 1, 1]
    L = math.sqrt((X2 - X1) ** 2 + (Y1 - Y2) ** 2)
    C = (X2 - X1) / L
    S = (Y2 - Y1) / L
    k = E * A / L * np.array([[C ** 2, C * S, -C ** 2, -C * C],
                              [C * S, S ** 2, -C * S, -S ** 2],
                              [-C ** 2, -C * S, C ** 2, C * S],
                              [-C * S, -S ** 2, C * S, S ** 2]])
    return k

def element_stiffness_frame(nl, ENL, E, A, I) :
    X1 = ENL[nl[0] - 1, 0]
    X2 = ENL[nl[0] - 1, 1]
    Y1 = ENL[nl[1] - 1, 0]
    Y2 = ENL[nl[1] - 1, 1]
    L = math.sqrt((X2 - X1) ** 2 + (Y1 - Y2) ** 2)
    C = (X2 - X1) / L
    S = (Y2 - Y1) / L
    B = I / L**2
    T = np.array([[C, S, 0, 0, 0, 0],
                  [-S, C, 0, 0, 0, 0],
                  [0, 0, 1, 0, 0, 0],
                  [0, 0, 0, C, S, 0],
                  [0, 0, 0, -S, C, 0],
                  [0, 0, 0, 0, 0, 1]])
    k_elem = E / L * np.array([[A, 0, 0, -A, 0, 0],
                  [0, 12*B, 6*L*B, 0, -12*B, -6*L*B],
                  [0, 6*L*B, 4*L**2*B, 0, 6*L*B, 2*L**2*B],
                  [-A, 0, 0, A, 0, 0],
                  [0, -12*B, -6*L*B, 0, 12*B, -6*L*B],
                  [0, 6*L*B, 2*L**2*B, 0, -6*L*B, 4*L**2*B]])
    k_global = np.transpose(T) * k_elem * T
    return k

def assemble_force(ENL, NL):
    PD = np.size(NL, 1)
    NoN = np.size(NL, 0)
    DOF = 0
    Fp = []

    for i in range(0, NoN):
        for j in range(0, PD):
            if ENL[i, PD + j] == 1:
                DOF += 1
                Fp.append(ENL[i, 5 * PD + j])
    Fp = np.vstack([Fp]).reshape(-1, 1)
    return Fp


def assemble_displacement(ENL, NL):
    PD = np.size(NL, 1)
    NoN = np.size(NL, 0)
    DOC = 0
    Up = []

    for i in range(0, NoN):
        for j in range(0, PD):
            if ENL[i, PD + j] == -1:
                DOC += 1
                Up.append(ENL[i, 4 * PD + j])
    Up = np.vstack([Up]).reshape(-1, 1)
    return Up


def update_nodes(ENL, U_u, NL, Fu):
    PD = np.size(NL, 1)
    NoN = np.size(NL, 0)
    DOFs = 0
    DOCs = 0
    for i in range(0, NoN):
        for j in range(0, PD):
            if ENL[i, PD + j] == 1:
                DOFs += 1
                ENL[i, 4 * PD + j] = U_u[DOFs - 1]
            else:
                DOCs += 1
                ENL[i, 5 * PD + j] = Fu[DOCs - 1]
    return ENL
