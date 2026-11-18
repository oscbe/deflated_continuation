import numpy as np
import os
import matplotlib.pyplot as plt

checkpoints_dir = "checkpoints/run_1"

nums = []
num_sols = []
epsilons = []

checkpoint_names = os.listdir(checkpoints_dir)
checkpoint_names.sort(key = lambda x: int(x.split("_")[1]))


for checkpoint in checkpoint_names[60:]:
    dir = os.path.join(checkpoints_dir, checkpoint)
    nums.append(int(checkpoint.split("_")[1]))
    num_sol = len(os.listdir(dir)) - 1
    num_sols.append(num_sol)


    epsilons.append(np.load(os.path.join(dir, "eps.npy")))
    print(num_sol)

plt.plot(epsilons, num_sols)
plt.grid()
plt.gca().set(
    xlabel='$\\varepsilon$',
    ylabel = 'Number of solutions'
)
# plt.title("Number of Solutions as $\\varepsilon$ is Varied", fontweight='bold')
plt.savefig("figs/num_sols")
plt.show()