import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

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

def compute_movie(support,nstep):
    ''' Returns the evolution of a board "support" after nstep generations '''
    history = np.zeros((T,support.shape[0], support.shape[1]),dtype=bool)
    for n in range(nstep):
        history[n,:,:] = support
        support = next_step(support)   
    return history  

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
    n = 5
    movie=[]
    grid = load_grid("./grid1.txt")
    movie.append(plt.imshow(grid,animated=True))
    
    fig = plt.figure()

    for i in np.arange(n):
        
        grid = next_step(grid)
        movie.append([plt.imshow(grid,animated=True)])

    
    animation.ArtistAnimation(fig, movie, interval=50, blit=True,repeat_delay=1000)   
    plt.show()

    return 

def step_plot(support):
    '''
    plot one step of the game
    '''
    plt.imshow(support,cmap="gray")
    plt.show()  

def main():

    game_movie()
    
if __name__ == "__main__":
    main()
