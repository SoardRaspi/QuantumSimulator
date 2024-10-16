import numpy as np
import time
import pennylane as qml
import matplotlib.pyplot as plt

# State Vector simulation of quantum computers

# Important initializations
ket0 = np.array([1, 0])
ket1 = np.array([0, 1])

X = np.array([[0, 1],
              [1, 0]])
Y = np.array([[0, -1j],
              [1j, 0]])
Z = np.array([[1, 0],
              [0, -1]])
I = np.array([[1, 0],
              [0, 1]])
H = np.array([[1, 1],
              [1, -1]]) / np.sqrt(2)

CNOT = np.array([[1, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 1],
                 [0, 0, 1, 0]])
TOFF = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0, 0],
                 [0, 0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1],
                 [0, 0, 0, 0, 0, 0, 1, 0]])


def RX(t):
    return np.array([[np.cos(t / 2), -np.sin(t / 2) * 1j],
                     [-np.sin(t / 2) * 1j, np.cos(t / 2)]])


def RY(t):
    return np.array([[np.cos(t / 2), -np.sin(t / 2)],
                     [np.sin(t / 2), np.cos(t / 2)]])


def RZ(t):
    return np.array([[np.exp(-(t / 2) * 1j), 0],
                     [0, np.exp((t / 2) * 1j)]])


operators_dict = {"X": X, "Y": Y, "Z": Z,
                  "I": I, "H": H,
                  "c": CNOT, "t": TOFF,
                  "RX": RX, "RY": RY, "RZ": RZ}

def circuit1_function(circuit):
    wires = []
    layers = []

    for wire in circuit:
        layer_temp = wire.split("--")
        wires.append(layer_temp)

    valid = True
    num_columns = len(wires[0])
    num_wires = len(circuit)

    state = ket0
    for i in range(num_wires - 1):
        state = np.kron(state, ket0)

    for layer in range(num_columns):
        layers.append("")

    for wire in wires:
        if valid:
            if len(wire) != num_columns:
                valid = False

    if not valid:
        print("Error with circuit input, incorrect number of column segments... Check if the identity"
              "gates are applied where no opration is to be performed, to form a valid vertical"
              "gate segment")

        return -1
    else:
        for layer in range(num_columns):
            for wire in wires:
                layers[layer] += wire[layer]

        for i in range(len(layers)):
            layer_temp = layers[i]
            layer_temp = layer_temp.replace("..x", "t")
            layer_temp = layer_temp.replace(".x", "c")

            if (('.' in layer_temp) or ('x' in layer_temp)) and \
                    ((".x" not in layer_temp) or ("..x" not in layer_temp)):
                return -1

            layers[i] = layer_temp

        for layer in layers:
            layer_operator = operators_dict[layer[0]]
            for gate in layer[1:]:
                layer_operator = np.kron(layer_operator, operators_dict[gate])

            state = np.dot(layer_operator, state)

        return state


def circuit2_function(circuit):
    wires = []
    layers = []

    for wire in circuit:
        layer_temp = wire.split("--")
        wires.append(layer_temp)

    valid = True
    num_columns = len(wires[0])
    num_wires = len(circuit)

    state = ket0
    for i in range(num_wires - 1):
        state = np.kron(state, ket0)

    for block in range(num_wires):
        layers.append("")

    for wire in wires:
        if valid:
            if len(wire) != num_columns:
                valid = False

    if not valid:
        print("Error with circuit input, incorrect number of column segments... Check if the identity"
              "gates are applied where no opration is to be performed, to form a valid vertical"
              "gate segment")

        return -1
    else:
        for i in range(num_wires):
            temp = ""
            temp_arr = []

            for iii in range(len(wires[i])):
                ii = wires[i][iii]
                if (ii == '.') or (ii == 'x'):
                    temp_arr.append(temp)
                    temp_arr.append(ii)
                    temp = ""

                else:
                    temp += ii

                if iii == len(wires[i]) - 1:
                    if temp != "":
                        temp_arr.append(temp)

            wires[i] = temp_arr

        for block_index in range(len(wires[0])):
            if len(wires[0][block_index]) != 1:
                list_operators = []

                for wire in wires:
                    wire_block = wire[block_index]
                    operator_temp = operators_dict[wire_block[0]]

                    for g in wire_block[1:]:
                        operator_temp = np.dot(operator_temp, operators_dict[g])

                    list_operators.append(operator_temp)

                block_operator_overall = list_operators[0]
                for wire_operator in list_operators[1:]:
                    block_operator_overall = np.kron(block_operator_overall, wire_operator)

                state = np.dot(block_operator_overall, state)

            else:
                layer_temp = ""

                for wire in wires:
                    layer_temp += wire[block_index]

                layer_temp = layer_temp.replace("..x", "t")
                layer_temp = layer_temp.replace(".x", "c")

                if (('.' in layer_temp) or ('x' in layer_temp)) and \
                        ((".x" not in layer_temp) or ("..x" not in layer_temp)):
                    return -1

                layer_operator = operators_dict[layer_temp[0]]
                for gate in layer_temp[1:]:
                    layer_operator = np.kron(layer_operator, operators_dict[gate])

                state = np.dot(layer_operator, state)

        return state


def task1_function(num_qubits=None, string_input=None, circuit_type=1):
    if num_qubits is None:
        num_qubits = int(input("Number of qubits: "))

    circuit_arr = []
    qubit_counter = 0

    for row in range(num_qubits):
        if string_input is None:
            string_temp = input(f"q{qubit_counter}: ")

        else:
            string_temp = string_input

        if string_temp.startswith("--"):
            string_temp = string_temp[2:]
        circuit_arr.append(string_temp)

        qubit_counter += 1

    if circuit_type == 1:
        output = circuit1_function(circuit_arr)

        if type(output) == int:
            return output
        else:
            return 0
    elif circuit_type == 2:
        output = circuit2_function(circuit_arr)

        if type(output) == int:
            return output
        else:
            return 0
    elif circuit_type == 3:
        output1 = circuit1_function(circuit_arr)
        output2 = circuit1_function(circuit_arr)

        if (output1 != -1) and (output2 != -1):
            print("diff:", np.linalg.norm(output1 - output2))
        else:
            return -1

status = task1_function(num_qubits=None, string_input=None, circuit_type=3)

if status == -1:
    print("Some error occurred!!!")
else:
    print("Code run successfully!!!")
