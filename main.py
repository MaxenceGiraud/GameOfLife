import numpy as np
import matplotlib.pyplot as plt

def compute_cell(support,x,y):
    return support[x,y] == True


def main():
    support = np.ones((2, 2), dtype=bool)
    print(compute_cell(support,1,1))

if __name__ == "__main__":
    main()
