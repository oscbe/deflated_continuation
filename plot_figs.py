import os
import numpy as np
import matplotlib.pyplot as plt
import pickle

dir = "checkpoints/run_1/checkpoint_139"

solutions = []
nums = []
for fname in os.listdir(dir):
    f = os.path.join(dir, fname)
    if fname.endswith('.npy'):
        eps = np.load(f)
    else:
        with open(f, 'rb') as file:
            obj = pickle.load(file)
            solutions.append(obj)
            nums.append(int(fname.split("_")[1].split(".")[0]))

numbered = list(zip(solutions, nums))
numbered.sort(key=lambda x: x[1])
solutions = list(zip(*numbered))[0]

vals = np.linspace(-1, 1, 1000)
for i, sol in enumerate(solutions):
    plt.plot(vals, sol(vals))
    plt.gca().set(
        xlabel='x',
        ylabel='y',
    )
    # plt.title(f"Solution {i + 1}", fontweight='bold')
    plt.grid()
    plt.savefig(f"figs/sol_{i+1}")
    plt.cla()