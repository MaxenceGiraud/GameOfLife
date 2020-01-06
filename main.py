import sys
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
    # Compute the number of neighbour for each cell

    neighbors = np.zeros(support.shape)
    support_int = support.astype(int)
    neighbors[1:-1,
              1:-1] = (support_int[:-2,
                                   :-2] + support_int[:-2,
                                                      1:-1] + support_int[:-2,
                                                                          2:] + support_int[1:-1,
                                                                                            :-2] + support_int[1:-1,
                                                                                                               2:] + support_int[2:,
                                                                                                                                 :-2] + support_int[2:,
                                                                                                                                                    1:-1] + support_int[2:,
                                                                                                                                                                        2:])

    # Go to next step using the number of neighbors and the value of each cell
    return np.logical_or(
        neighbors == 3, np.logical_and(
            support, neighbors == 2))


def compute_movie(support, nstep):
    '''
    Returns the evolution of a board "support" after nstep generations
    @param : support, np.array(dtype=bool), a board of game of life
    @nstep : int, number of step you want the game of life to played
    @return : history of the game, array of nstep size containing each step
    '''
    history = np.zeros((nstep, support.shape[0], support.shape[1]), dtype=bool)
    for n in range(nstep):
        history[n, :, :] = support
        support = next_step(support)
    return history


def load_grid(filename):
    '''
    Load a grid from a file
    see http://www.conwaylife.com/wiki/RLE
    @param : filename : the file you want to load
    @return : np.array(), board of the loaded file
    '''
    
    # Open file and cast it into a unique string
    f = open(filename, "r")
    s = ''

    while True:
        l = f.readline()
        if l == '':             # Empty indicates end of file. An empty line would be '\n'
            break
        if l[0] == '#':
            continue
        if l[0] == 'x':
            continue
        s = s + l[:-1]   # To remove EOL
    f.close()

    # Create matrix
    SHAPE_MAX = (2500, 2500)
    B = np.zeros(SHAPE_MAX).astype(bool)

    # We parse each character and decide accordingly what to do
    # If the character is a digit, we keep going until we reach 'b' or 'o'
    curX, curY = 0, 0
    qs = ''

    for c in s:
        # End of file
        if c == '':
            break

        # Next Line
        if c == '$':

            q = 1 if qs == '' else int(qs)
            curY += q
            curX = 0
            qs = ''

        # Digit (check ascii code for a digit from 0 to 9)
        if ord(c) > 47 and ord(c) < 58:  #
            qs = qs + c

        # Alive (o) or Dead (b) cell
        if c == 'b' or c == 'o':
            q = 1 if qs == '' else int(qs)
            for i in range(q):
                B[curX, curY] = False if c == 'b' else True
                curX += 1
            qs = ''

    posX, posY = (10, 10)
    BshapeY = max(np.where(sum(B) > 0)[0]) + 1
    BshapeX = max(np.where(sum(B.T) > 0)[0]) + 1

    B = B[0:BshapeX, 0:BshapeY]

    C = np.zeros((3 * B.shape[0], 3 * B.shape[1]))
    C[B.shape[0]:(2 * B.shape[0]), B.shape[1]:(2 * B.shape[1])] = np.copy(B)

    return C.astype(bool)


def plotcells(X, filename=False):
    '''
    Plots a board of Game of Life + optionally saving the figure
    @param X : np.array(dtype=bool), a board of the game
    @param : filename: if not false save the figure to the name you assigned it
    @return : nothing, just plot the board (new window)
    '''
    LW = 0.5

    fig = plt.figure(figsize=(16, 9), dpi=120)
    plt.imshow(X[:, ::-1].T, cmap="gray_r")
    plt.gca().get_xaxis().set_visible(False)
    plt.gca().get_yaxis().set_visible(False)
    fig.tight_layout()

    if (filename):
        plt.savefig(filename)
    else:
        plt.show()


def makeMovie(history, filename):
    '''
    Create the movie from a history of a game of life
    @param : history, history of the game of life you want to save
    @param ; filename, string, name of the file (should be *.mp4)
    '''
    # History is the boolean history (non inverted i.e. True = alive)
    # Inversion is done in the colormap

    FIGSIZE = (16, 9)
    DPI = 240
    LW = 0.5

    # Create the plot and its starting point
    my_cmap = plt.get_cmap('gray_r')
    fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
    ax = fig.add_subplot(111)

    im = ax.imshow(history[0, :, ::-1].T, cmap=my_cmap)

    cnt = ax.text(0.01, 0.99, str(0), color='red', fontsize=30,
                  verticalalignment='top', horizontalalignment='left',
                  transform=ax.transAxes)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    fig.tight_layout()

    # The functionc as it is called at the n-th iteration
    # It directly modifies the data within the image

    def update_img(n):
        # Revert and scale from 0-1 to 0-255
        im.set_data(history[n, :, ::-1].T)
        cnt.set_text(str(n))
        return True

    # Create the animation and save it
    print("Making animation")
    ani = animation.FuncAnimation(fig, update_img, history.shape[0],
                                  interval=30)  # 30ms per frame
    writer = animation.FFMpegWriter(fps=30, bitrate=5000)
    print("Save movie")
    ani.save(filename, writer=writer, dpi=DPI)
    print("Saved")


class Unittest(unittest.TestCase):
    def test_next_step_AllDead(self):
        self.assertTrue(
            np.all(
                next_step(
                    np.zeros(
                        (100, 100), dtype=bool)) == np.zeros(
                    (100, 100), dtype=bool)))

    def test_next_step_AllAlive(self):
        self.assertTrue(
            np.all(
                next_step(
                    np.ones(
                        (100, 100), dtype=bool)) == np.zeros(
                    (100, 100), dtype=bool)))


def main():

    rle_file, nstep,video_file  = sys.argv[1:3]

    grid = load_grid(rle_file)
    movie = compute_movie(grid,nstep)
    makeMovie(movie,video_file)

if __name__ == "__main__":
    main()
