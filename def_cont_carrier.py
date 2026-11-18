import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
from tools.carrier import *
from typing import List

def save_to_checkpoint(
        eps: float,
        sols: List,
        checkpoint_path: str = "checkpoints/checkpoint_1"
        ) -> None:
    """Checkpoint a deflated continuation run. Saves epsilon value and found solutions.

    Parameters
    ----------
    eps: float
        Epsilon value of run.
    sols: list
        List of solutions found on run.
    checkpoint_path: float
        Relative file location to save checkpoint to.
    """
    if not os.path.exists(checkpoint_path):
        os.makedirs(checkpoint_path)

    # save solutions
    for i, sol in enumerate(sols):
        with open(checkpoint_path + f"/sol_{i}.pkl", "wb") as f:
            pickle.dump(sol, f)

    # save epsilon value
    np.save(checkpoint_path + "/eps", eps)
    return


if __name__ == "__main__":
    
    # initialise epsilons to iterate over
    epsilons = np.hstack([np.linspace(1/2, 0.1, 40, endpoint=False), np.linspace(0.1, 0.01, 100)])**(1/2)

    # initialise guesses - we choose zero, and asymmetric guesses
    guesses = [
        lambda x: 0 * x,
        lambda x: 5*x*(1 - x**2),
        lambda x: 5*x*(x**2 - 1)
        ]
    
    for j, eps in enumerate(epsilons):
        print(f"Epsilon =  {eps}\n----------------")
        solver = DeflatedCarrier(256, eps, guesses[0])

        # seek solutions with each of the initial guesses
        for guess in guesses:
            print(f"Guess: {guess}")
            solver.u0 = guess

            solver.deflated_solve(16, tol=1e-8, max_iters=30)
        
        # use solutions as guesses for the next iteration
        guesses = [i for i in solver.deflator] + [
            lambda x: 0 * x,
            lambda x: 5*x*(1 - x**2),
            lambda x: 5*x*(x**2 - 1)
            ]
        
        print(f"{len(solver.deflator.solutions)} solutions found for epsilon = {eps}\n---------------------------------------------------")
        save_to_checkpoint(eps, [i for i in solver.deflator], checkpoint_path=f"checkpoints/run_1/checkpoint_{j}")

    # plot final solutions
    for i, sol in enumerate(solver.deflator):
        vals = np.linspace(-1, 1, 500)
        plt.plot(vals, sol(vals))
        plt.grid()
        plt.xlabel("x")
        plt.ylabel("y")
        plt.savefig(f"figs/sol_{i}")
        plt.cla()
        # plt.show()