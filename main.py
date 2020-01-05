import unittest
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def next_step(support):
    '''
    Compute next step of the Game with the 3 following rules
    Any live cell with two or three neighbors survives.
    Any dead cell with three live neighbors becomes a live cell.
    All other live cells die in the next generation. Similarly, all other dead cells stay dead.
    @param : support, np.array(dtype=bool), a board of game of life
    @return : np.array(dtype=bool) of same size as support, next step of the game of life
    '''
    ## Compute the number of neighbour for each cell

    neighbors = np.zeros(support.shape)
    support_int = support.astype(int)
    neighbors[1:-1,1:-1] = (support_int[:-2,:-2] + support_int[:-2,1:-1] + support_int[:-2,2:] + support_int[1:-1,:-2] + support_int[1:-1,2:]  + support_int[2:,:-2]   + support_int[2:,1:-1]  + support_int[2:,2:]) 

    ## Go to next step using the number of neighbors and the value of each cell
    return np.logical_or(neighbors==3,np.logical_and(support,neighbors==2))


def compute_movie(support,nstep):
    ''' 
    Returns the evolution of a board "support" after nstep generations 
    @param : support, np.array(dtype=bool), a board of game of life
    @nstep : int, number of step you want the game of life to played
    @return : history of the game, array of nstep size containing each step
    '''
    history = np.zeros((nstep,support.shape[0], support.shape[1]),dtype=bool)
    for n in range(nstep):
        history[n,:,:] = support
        support = next_step(support)   
    return history  

def load_grid(file):
    '''
    Load a grid from a file
    '''
    ## TODO/ TO correct
    coordonates =[]
    with open(file, 'r') as f:
        content = f.readlines()
        for lign in content[1:] :
            coordonates.append([int(lign[0]),int(lign[2])])

    grid = np.zeros((max(np.array(coordonates)[:,0])*10, max(np.array(coordonates)[:,0])*10),dtype=bool)
    for [x,y] in coordonates :
        grid[x][y] = True 

    return grid

def plotcells(X, filename=False):
    ''' 
    Plots a board of Game of Life + optionally saving the figure
    @param X : np.array(dtype=bool), a board of the game
    @param : filename: if not false save the figure to the name you assigned it
    @return : nothing, just plot the board (new window)
    '''
    LW = 0.5
    if(X.shape[0]>200): 
        USE_IMSHOW = True
    else:
        USE_IMSHOW = False
        
    fig = plt.figure(figsize=(16,9),dpi=120)    
    if USE_IMSHOW == False:    
        # Light blue lines as cells boundaries
        plt.pcolor(X.T, cmap="gray_r",
                   edgecolors='cadetblue', linewidths=LW)
    else:
        plt.imshow(X[:,::-1].T, cmap="gray_r")        
    plt.gca().get_xaxis().set_visible(False)
    plt.gca().get_yaxis().set_visible(False)
    fig.tight_layout()
    
    if (filename != False): 
        plt.savefig(filename,dpi=90)
    else:
        plt.show()

def makeMovie(history,filename):
    ''' 
    Create the movie from a history of a game of life
    @param : history, history of the game of life you want to save
    @param ; filename, string, name of the file (should be *.mp4)
    '''
    # History is the boolean history (non inverted i.e. True = alive)
    # Inversion is done in the colormap
    
    FIGSIZE = (16,9)
    DPI = 240
    LW = 0.5
    
    
    if(history.shape[1]>200): 
        USE_IMSHOW = True
    else:
        USE_IMSHOW = False
    
    # Create the plot and its starting point
    print("Create initial plot")
    my_cmap = plt.get_cmap('gray_r')
    fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
    ax = fig.add_subplot(111)
    
    if USE_IMSHOW == False:
    # First option : use pcolor
        pc = ax.pcolor(history[0,:,:].T, cmap=my_cmap,
                       edgecolors='cadetblue', linewidths=LW)
    else:        
    # Second option : use imshow
        im  = ax.imshow(history[0,:,::-1].T, cmap=my_cmap)
    
    cnt = ax.text(0.01, 0.99, str(0),color='red', fontsize=30,
            verticalalignment='top', horizontalalignment='left',
            transform=ax.transAxes)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    fig.tight_layout()
    
    
    # The function as it is called at the n-th iteration
    # It directly modifies the data within the image
    def update_img(n):
        # Revert and scale from 0-1 to 0-255
        print('Frame '+str(n))
        if USE_IMSHOW == False:
            new_color = my_cmap(255*history[n,:,:].T.ravel()) 
            pc.update({'facecolors':new_color})
        else:
            im.set_data(history[n,:,::-1].T)

        cnt.set_text(str(n))
    
        return True
    
    # Create the animation and save it
    print("Make animation")
    ani = animation.FuncAnimation(fig, update_img, history.shape[0], 
                                  interval=30) # 30ms per frame
    writer = animation.FFMpegWriter(fps=30, bitrate=5000)
    print("Save movie")
    ani.save(filename, writer = writer, dpi=DPI) 
    print("Saved") 

class Unittest(unittest.TestCase):
    def test_next_step_AllDead(self):
        self.assertTrue(np.all(next_step(np.zeros((100,100),dtype=bool)) == np.zeros((100,100),dtype=bool)))

    def test_next_step_AllAlive(self):
        self.assertTrue(np.all(next_step(np.ones((100,100),dtype=bool)) == np.zeros((100,100),dtype=bool)))



def main():

    #game_movie()
    test = np.zeros((100,100),dtype=bool)
    test[10,10]=True
    test[10,11]=True
    test[10,12]=True
    test[10,13]=True
    test[11,13]=True
    test[11,13]=True

    m = compute_movie(test,100)
    makeMovie(m,"test.mp4")

if __name__ == "__main__":
    main()
