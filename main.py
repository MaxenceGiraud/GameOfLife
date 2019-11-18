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
    neighbors[1:-1,1:-1] = (support[:-2,:-2] + support[:-2,1:-1] + support[:-2,2:] + 
                        support[1:-1,:-2] +                support[1:-1,2:]  + 
                        support[2:,:-2]   + support[2:,1:-1]  + support[2:,2:]) 

    return neighbors

def main():
    support = np.zeros((4, 4), dtype=bool)
    support[1,1] = "True"
    support[1,2] = "True"
    support[2,1] = "True"

    print(support,"\n",next_step(support))

if __name__ == "__main__":
    main()
