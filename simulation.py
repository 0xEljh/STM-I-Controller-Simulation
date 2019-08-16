import matplotlib.pyplot as plt
import math
import queue


#### DAQ/Simulation Input Parameters ####
samples = 50000  # number of samples/time steps to simulate
sampling_rate = 100000 # i.e. samples per sec/size of time step


# Supporting Functions & Classes #
def get_time(sample_no):
    return sample_no/sampling_rate
def get_sample(time):
    return int(sampling_rate * time)

class noise:
    def __init__(self,amplitude,frequency):
        self.amplitude = amplitude  # some float
        self.frequency = frequency #some float

    def amp(self, *amplitude):
        if amplitude:
            self.amplitude = amplitude

    def freq(self, *frequency):
        if frequency:
            self.frequency = frequency

    def val(self, sample_no):
        x = get_time(sample_no) * 2 * math.pi * self.frequency  # 2 n * pi / T
        return self.amplitude*math.sin(x)

def transmission (workfunction, energy, distance):  # workfunction and energy in eV, distance in nanometers
    ev_to_j = 1.6 * (10**-19)
    h = 6.5821 * (10**-16)
    mass = 9.11* (10**-31)
    coefficient = 16 * energy * (workfunction - energy) / (workfunction **2) # no need to convert to j
    exponent_term = math.exp(- 2 * distance * (10**-12) * (math.sqrt(2* mass *(workfunction - energy) * ev_to_j))/(h * ev_to_j))
    return coefficient * exponent_term

#### Controller Input Parameters ####

noise_set = [noise(0.1,50), noise(0.05,630), noise(0.05, 400), noise(0.03,10), noise(0.03, 220)]  # List of noise to generate in the background.
# These (voltage) amplitude - frequency pairs came from FFTs of  the experimental results

time_lag = 0.0003   # time delay of the circuit in seconds

setpoint = 1  # Setpoint voltage of Vtunneling

piezo_ratio = 645 # Ratio of 1V : Deflection in nanometers

initial_distance = 1000  # Initial distance between the tip & sample in nanometers

work_function_ev = 4.08  # Workfunction of sample in eV
energy = 1  # Sample bias/Energy of the electron in eV

## I controller ##
RC_value = (1/1000000) * (100000 + 5000)  # RC value of the Integral RC circuit
frequency = 1/RC_value  # Time constant of the circuit
# Ki = 1/RC = frequency
print("The Ki value is " + str(frequency))


#### #### ## End of user inputs; The rest are calculations ## #### ####


# initialisation:
sample_lag = get_sample(time_lag)

sample_period = int(sampling_rate/frequency)
initial_output = 0

errors, error_timestamps = [], []
outputs, distance, amped_currents, timestamps = [], [], [], []

initial_current = transmission(work_function_ev, energy, initial_distance)

print("initial current is : " + str(initial_current))

recorded_d = []  # Might also want to see the changes in distance!

for n in range(0, sample_lag):
    amped_currents.append(initial_current)  # initialise amped currents part before controller starts
    outputs.append(initial_output)
    distance.append(initial_distance)  # taken as base dist s.t. any increase in dist leads to some finite current
    timestamps.append(get_time(n))

print("time lag in samples is : "+ str(sample_lag))
print("period in samples is : " + str(sample_period))

sum = 0

for i in range(sample_lag, samples):

    timestamps.append(get_time(i)) # update time

    ## I - controller portion ##
    v_tunnel = amped_currents[-1]
    for signal in noise_set:
        v_tunnel += signal.val(i)
    error = setpoint - v_tunnel # diff. between setpoint and current value of amplified tunnelling current
    # this is V-in for the integrator circuit

    error = error /get_sample(RC_value)
    errors.append(error)
    error_timestamps.append(get_time(i))
    sum += error #  Sum all the errors into integral
    # there is a maximum and minimum sum due to Vcc
    if sum <-10:
        sum = -10
    if sum >10:
        sum = 10
    #output of the I controller is 1/RC * integral:
    v_out = sum #/ RC_value
    #again, there is a max and min value:
    if v_out >10:
        v_out=10
    if v_out<-10:
        v_out = -10
    outputs.append(v_out)

    # find change in distance due to change in output: aka vpiezo * piezo deflection/v
    piezo_d = outputs[-1] * piezo_ratio
    # moving upwards leads to negative change in d

    #there is a maximum deflection for the piezo:

    if piezo_d > 10000:
        piezo_d = 10000
    if piezo_d < -10000:
        piezo_d = -10000
    d = initial_distance - piezo_d
    # distance cannot be negative
    if d < 0:
        d = 0
        print("crashed tip into sample at sample no " +str(i))
    distance.append(d)

    # calculate new tunneling current based on new d:
    current = transmission(work_function_ev, energy, d)
    # There is a maximum amplification on the tunnelling current
    if current > 10:
        current = 10
    if current < -10:
        current = -10

    amped_currents.append(current)

#plt.plot(timestamps, outputs, "g--", error_timestamps, errors, "r--", timestamps, amped_currents, "b--", timestamps, distance)
plt.plot(timestamps, outputs, color = "green", linewidth=2, label = "Vpiezo")
plt.plot(error_timestamps, errors, "r--", label="Error")
#plt.plot(timestamps, distance, label="distance")
plt.plot(timestamps, amped_currents, color ="blue", linewidth=2, label="Vtunneling")
plt.title("Voltage Signals against Time")
plt.legend()
plt.show()

