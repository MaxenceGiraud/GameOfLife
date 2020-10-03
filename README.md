# GameOfLife
GameOfLife Project

## Build Status
[![CircleCI](https://circleci.com/gh/MaxenceGiraud/GameOfLife.svg?style=svg&circle-token=bea5bcd7b017faabf8bbf2f7bb9dcbfb4dfc2736)](https://circleci.com/gh/MaxenceGiraud/GameOfLife)

## Contributors

Project done By Maxence Giraud

## How to use 

### From the command line
```bash
python3 GameOfLife/gameoflife.py -i inputfile -o outputfile -s numberofsteps

### Simple example
python3 GameOfLife/gameoflife.py -i breeder.rle -o breader.mp4 -s 300
```

### Using python
```python
import GameOfLife as gof

nsteps = 300
grid = gof.load_grid("breader.rle")
movie = gof.compute_movie(grid, 300)
gof.makeMovie(movie, "breader.mp4")
```

### unittest
To launch unittest : 
```python 
python3 -m unittest tests/gof_test.py
```

### Input files 
This program supports RLE files, to look at the formalism :
<https://www.conwaylife.com/wiki/Run_Length_Encoded>

## License
[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
