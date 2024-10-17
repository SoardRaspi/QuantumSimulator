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
<p>layer 1: </p>
<br>

<h4>Method 2:</h4>
<p></p>
