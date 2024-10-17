<h1>QOSF Cohort 10 Screening Tasks' Solutions</h1>
<p>This repository contains the solutions to the QSOF Cohort 10 Screening Tasks. The folders represent the code and other related media items to the individual tasks. In the sections below, the problem statement of the tasks and approach/solution is described in brief. A brief description of how to use the code along with the requirements for that individual code is also mentioned. The folder for each task contains the code file and the related media.</p>

<h2>Task 1</h2>
<h3>Problem statement:</h3> 
<p>Task 1 asks to write a code to make a state vector simulator from scratch. This is to understand how the gate operates on the states mathematically. There are two approaches presented in the code to do these operations and their runtimes are compared for varying number of qubits. The code currently compares the runtimes for only upto 15 qubits, which as can be seen from the comparison graph, grows spontaneously. Given the device limitations, the code compares only upto 15 qubits, but this can be easily changed in the code to any number of qubits.</p>
<img src="Task 1/runtime comparison.png" alt="comaparison graph" width="500">
In this graph, the blue line represents the runtimes by following <b>Method 1</b> and the orange line represents the runtimes by following <b>Method 2</b>.
