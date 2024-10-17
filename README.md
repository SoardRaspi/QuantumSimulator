<h1>QOSF Cohort 10 Screening Tasks' Solutions</h1>
<p>This repository contains the solutions to the QSOF Cohort 10 Screening Tasks. The folders represent the code and other related media items to the individual tasks. In the sections below, the problem statement of the tasks and approach/solution is described in brief. A brief description of how to use the code along with the requirements for that individual code is also mentioned. The folder for each task contains the code file and the related media.</p>

<h2>Task 1</h2>
<h3>Problem Statement:</h3> 
<p>Task 1 asks to write a code to make a state vector simulator from scratch. This is to understand how the gate operates on the states mathematically.</p>

<h3>Solution:</h3>
<p>There are two approaches presented in the code to do these operations and their runtimes are compared for varying number of qubits. The code currently compares the runtimes for only upto 15 qubits, which as can be seen from the comparison graph, grows spontaneously. Given the device limitations, the code compares only upto 15 qubits, but this can be easily changed in the code to any number of qubits.</p>
<img src="Task 1/runtime comparison.png" alt="comaparison graph" width="500">
In this graph, the blue line represents the runtimes by following <b>Method 1</b> and the orange line represents the runtimes by following <b>Method 2</b>.

<h4>Method 1:</h4>
<p>The method one proposes calculating the state vectors after every layer of gate operations. Here a layer of gate operations is defined as the collective operation of the gates across all wires which lie in the sam vertical position. As an example, in the circuit: </p>
<br>
<p>q0 --X--H--</p>
<p>q1 --Y--Z--</p>
<p>q2 --Z--X--</p>
<br>

<p>the layers would be :</p>
<br>
<p>layer 1: X, Y, X</p>
<p>layer 2: H, Z, X</p>
<br>

<p>Following Method 1, the cumulative operator for a layer is first calculated using the tensor (kronecker) product which represents a multi-qubit operator which operates directly on the whole system's state vector. For the given circuit, we can mathematically write, </p>

<br>
<p>layer 1: <img src="https://latex.codecogs.com/svg.latex?\color{White}X%20\otimes%20Y%20\otimes%20X" alt="X tensor Y tensor X" /></p>
<p>layer 2: <img src="https://latex.codecogs.com/svg.latex?\color{White}H%20\otimes%20Z%20\otimes%20X" alt="H tensor Z tensor X" /></p>
<br>

<p>The code follows by first calculating the multi-gate qubit operator for each layer as it traverses through the input circuit by following the kronecker product operation among the gates in that layer. Following the notation, we go from top-to-bottom and left-to-right. The top-to-bottom rule can be seen in the mathematical formulation of the operation. In the code, this is done using numpy's kron function. Calculations for the layer 2's operator are shown below: </p>

```math
H\ \otimes\ Z\ \otimes\ X\ =
\frac{1}{\sqrt{2}}\begin{bmatrix}
1 & 1 \\
1 & -1 
\end{bmatrix} \otimes
\begin{bmatrix}
1 & 0 \\
0 & -1 
\end{bmatrix} \otimes
\begin{bmatrix}
0 & 1 \\
1 & 0 
\end{bmatrix}\ =
\frac{1}{\sqrt{2}}\begin{bmatrix}
1 & 1 \\
1 & -1 
\end{bmatrix} \otimes
\begin{bmatrix}
0 & 1 & 0 & 0 \\
1 & 0 & 0 & 0 \\
0 & 0 & 0 & -1 \\
0 & 0 & -1 & 0 \\
\end{bmatrix}
```

```math
= \frac{1}{\sqrt{2}}\begin{bmatrix}
0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 \\
1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\
0 & 0 & 0 & -1 & 0 & 0 & 0 & -1 \\
0 & 0 & -1 & 0 & 0 & 0 & -1 & 0 \\
0 & 1 & 0 & 0 & 0 & -1 & 0 & 0 \\
1 & 0 & 0 & 0 & -1 & 0 & 0 & 0 \\
0 & 0 & 0 & -1 & 0 & 0 & 0 & 1 \\
0 & 0 & -1 & 0 & 0 & 0 & 1 & 0 
\end{bmatrix}
```

<p>After the cumulative multi-gate operator has been calculated, the operation of this operator on the state vector looks like:</p>

```math
\vert\psi_{2}\rangle = (Layer\ 2\ operator)\cdot\vert\psi_{1}\rangle
```

<p>Here, the statevector on LHS is the one formed after the operator for the layer is applied on the previou statevector (the statevector on the RHS).</p>

<p>In this approach, the code has no need to look for the special case of the CNOT gate or the Toffoli Gate and can easily go on with the kronecker multiplications to form the final operator. However, this is not the case in Method 2.</p>

<h4>Method 2:</h4>
<p>This method follows a similar approach, but instead of separating the circuit into vertical gate layers, the circuit is seen as a collection of block(s) and/or layer(s). The principle difference in Method 2 is that the single qubit gates are not operated upon to form a cumulative multi-gate operator for the whole circuit and thenoperated upon the state vector of the system. Instead of this, for each wire, the single qubit gates are operated upon the corresponding wire sequentially using matrix multiplications until a multi-qubit gate like the CNOT gate or the Toffoli gate. The portion of the circuit before or after or in-between the vertical layer(s) where the multi-qubit gate(s) is used is called here as a block of the circuit.</p>

<p>Following the above definition, for each block, until the block ends, for each wire the single-qubit gates are operated on the corresponding wire sequentially, thus always maintaining the dimension of 2 x 2. After the end of the block, the final matrix for each wire, representing the combined transformation in that block for that wire, is multiplied among themselves using the kronecker product to form the multi-qubit operator for the whole system.</p>

<p>Here, end of the block means that either the whole circuit has ended or a multi-qubit gate has been encountered in the circuit. Once this happens, the multi-qubit operators are matrix-multiplied to form the matrix of combined operation. This particular part of this method is similar to the layer-based calculation(s) taking place in Method 1.</p>

<p>As an example, in the circuit:</p>
<br>
<p>q0 --X--H--.</p>
<p>q1 --Y--Z--x</p>
<p>q2 --Z--X--I</p>
<br>

<p>the blocks would be :</p>
<br>
<p>block 1: [[X, H], [Y, Z], [Z, X]]</p>
<p>block 2: [.x, I]</p>
<br>
