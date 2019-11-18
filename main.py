import numpy as np
import matplotlib.pyplot as plt

def next_step(support):
    '''
    Any live cell with two or three neighbors survives.
    Any dead cell with three live neighbors becomes a live cell.
    All other live cells die in the next generation. Similarly, all other dead cells stay dead.
    '''

    ## Compute the number of neighbour for each cell

    neighbors = np.zeros(support.shape)
    support_int = support.astype(int)
    neighbors[1:-1,1:-1] = (support_int[:-2,:-2] + support_int[:-2,1:-1] + support_int[:-2,2:] + support_int[1:-1,:-2] + support_int[1:-1,2:]  + support_int[2:,:-2]   + support_int[2:,1:-1]  + support_int[2:,2:]) 
    print (neighbors,"\n\n")

    ## Go to next step using the number of neighbors and the value of each cell
    next = np.logical_or(neighbors==3,np.logical_and(support,neighbors==2))

    return next

def step_plot(support):

    plt.imshow(support,cmap="gray")
    plt.show()


def main():
    support = np.zeros((20, 20), dtype=bool)
    support[1,1] = "True"
    support[1,2] = "True"
    support[2,1] = "True"
    support[2,2] = "True"
    support[0,0] = "True"
    support[0,1] = "True"

    step_plot(support)
    step_plot(next_step(support))

if __name__ == "__main__":
    main()
