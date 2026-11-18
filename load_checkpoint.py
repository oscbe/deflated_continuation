import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
from tools.carrier import *
from def_cont_carrier import save_to_checkpoint
from typing import Union, List

def load_from_checkpoint(
        checkpoint_path: str
        ) -> Union[float, List]:
    """Loads the epsilon value and solutions associated with a deflated continuation run.

    Parameters
    ----------
    checkpoint_path: string
        Relative location to load data from.

    Returns
    -------
    eps: float
        Epsilon value in checkpoint.
    solutions: list
        List of solutions in checkpoint.
    """
    solutions = []
    for f in os.listdir(checkpoint_path):

        # load epsilon value
        if f.endswith(".npy"):
            eps = np.load(os.path.join(checkpoint_path, f))

        # load in solutions
        else:
            with open(os.path.join(checkpoint_path, f), "rb") as sol:
                obj = pickle.load(sol)
                solutions.append(obj)
    return eps, solutions

if __name__ == "__main__":
    
    # load checkpoint and initialise epsilons to iterate over
    eps, sols = load_from_checkpoint("checkpoints/run_1/checkpoint_117")
    epsilons = np.linspace(0.1, eps**2, 40, endpoint=False)**(1/2)
    epsilons = epsilons[::-1]

    # initialise guesses - previous solutions, zero, and asymmetric guesses
    guesses = sols + [
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
        save_to_checkpoint(eps, [i for i in solver.deflator], checkpoint_path=f"checkpoints/run_2/checkpoint_{j}")