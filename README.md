# GosperLife
My attempt at [Conway's game of life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) using Python, it's called Gosper because that was the first pattern I ran (a gosper glider gun).

So far, only runs on Linux Ubuntu. In order to run in windows, the `os.system('clear')` command should be changed to `os.system('cls')`, at some point I will fix this.

 ### Game of life Rules:
 1. Any live cell with fewer than two live neighbors dies
 2. Any live cell with two or three live neighbors lives on to the next gen
 3. Any live cell with more than three live neighbors dies
 4. Any dead cell with exactly three live neighbors becomes a live cell
 
 special cases (text files must be in the same directory): 
 * if board is larger than 25x25 and if user specifies 66 seeds, a canada goose is seeded (persistent pattern)
 * if board is larger than 38x38 and if user specifies 99 seeds, a gosper gun is seeded (generates gliders)            
