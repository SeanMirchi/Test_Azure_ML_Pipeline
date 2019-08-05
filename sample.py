from azureml.core.run import Run
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# This will get the current Run
run = Run.get_context()

print("This is an experiment")

run.log("x", 100)
run.log("y", 200)
run.log("z", 300)

# Lets plot some data
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)
fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
ax.grid()
run.log_image(f"sample_Plot", plot=plt)

Fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
run.log_list("Fibonacci", Fibonacci)
