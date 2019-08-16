# STM-I-Controller-Simulation
## Purpose
A simple python simulation of the stability of a scanning tunneling microscope with only 1 degree of freedom (vertical/z-axis) that was built for the module ESP2110. The vertical stability & convergence on a setpoint tunneling signal is maintained by a simple I-controller that uses a piezoelectric plate as its actuator. 

The goal is to attain high stability despite the presence of electrical noise that inevitably occurs due to the power supply & low current/high amplification setup. This simulation is a tool to identify areas of the setup/controller that can be optimised to improve stability despite the high electrical noise that feeds into the I-controller.
This simulation also highlights that that the electrical noise forms a positive feedback loop: background noise leads to fluctuations in the output of the I-controller, which leads to fluctuations in the actuator, which leads to fluctuations in tunnelling distance, which leads to fluctuations in the electrical signal to the I-controller which leads to more fluctuations in the actuator... etc.
## How to use:
Simply edit the following variables:

>samples = 50000  # number of samples/time steps to simulate

>sampling_rate = 100000 # i.e. samples per sec/size of time step

>noise_set = [noise(0.1,50), noise(0.05,630), noise(0.05, 400), noise(0.03,10), noise(0.03, 220)]  # List of noise to generate in the background.

>\# These (voltage) amplitude - frequency pairs came from FFTs of  the experimental results

>time_lag = 0.0003   # time delay of the circuit in seconds

>setpoint = 1  # Setpoint voltage of Vtunneling

>piezo_ratio = 645 # Ratio of 1V : Deflection of the piezo actuator in nanometers

>initial_distance = 1000  # Initial distance between the tip & sample in nanometers

>work_function_ev = 4.08  # Workfunction of sample in eV

>energy = 1  # Sample bias/Energy of the electron in eV

>RC_value = (1/1000000) * (100000 + 5000)  # RC value of the Integral RC circuit

>frequency = 1/RC_value  # Time constant of the circuit

Then run!
