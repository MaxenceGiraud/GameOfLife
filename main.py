import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

    ## Go to next step using the number of neighbors and the value of each cell
    next = np.logical_or(neighbors==3,np.logical_and(support,neighbors==2))

    return next

def load_grid(file):
    '''
    Load a grid from a file
    '''
    coordonates =[]
    with open(file, 'r') as f:
        content = f.readlines()
        for lign in content[1:] :
            coordonates.append([int(lign[0]),int(lign[2])])

    grid = np.zeros((max(np.array(coordonates)[:,0])*10, max(np.array(coordonates)[:,0])*10),dtype=bool)
    for [x,y] in coordonates :
        grid[x][y] = True 

    return grid

def game_movie():
    '''
    create a movie from a certain grid 
    '''
    return

def step_plot(support):
    '''
    plot one step of the game
    '''
    plt.imshow(support,cmap="gray")
    plt.show()  

def main():

    #support2 = np.ones((20, 20),dtype=bool)
    #print(support2,"\n\n\n")
    #print(next_step(support2))
    #step_plot(next_step(support2))

    print(load_grid("./grid1.txt")) 
    #grid = np.loadtxt("./grid1.txt",dtype=bool)
    #print(grid)
if __name__ == "__main__":
    main()
