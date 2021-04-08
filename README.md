# Machine, Date & Learning


<br>

## Value-Iteration


<br>
<b>Team 25 | Tribrid</b>

* Nitin Chandak (2019101024)
* Ayush Sharma (2019101004)

<br>



# Task - 1


**NOTE:** The trace of the state, the chosen action at that state and the value of state
for all iterations of the `VI` algorithm from 0 till convergence has been logged in `outputs/part_2_trace.txt` in following format.
```
iteration=0
(W,0,0,D,0):RIGHT=[12.231]
(W,0,0,D,25):RIGHT=[6.000]
.
.
.
(C,2,3,R,100):SHOOT=[1.232]
iteration=1
(W,0,0,D,0):STAY=[8.999]
.
.
.
.(so on until the end of iterations)
```


## Interpretation, Analysis & Comments



## Simulations

We have simulate the game for obtained `utility` and `policy` on two start states:
* (W, 0, 0, D, 100)
* (C, 2, 0, R, 100)

**The order of the actions, the state transitions and comment on the results for above start states:** We ran simulations `10` times fr both start state and found that every time it reaches the terminal state i.e. state with last value `0` like `('S', 0, 2, 'R', 0)` and `('E', 0, 0, 'R', 0)`. One of the output is shown below for each start state. One can find all the obtained outputs on running simulation in `outputs/simulations/2_1.txt` file.

### `(W, 0, 0, D, 100)`


```
current_state = ('W', 0, 0, 'D', 100) action_taken = RIGHT reached_state = ('C', 0, 0, 'R', 100)
current_state = ('C', 0, 0, 'R', 100) action_taken = RIGHT reached_state = ('C', 0, 0, 'D', 100)
current_state = ('C', 0, 0, 'D', 100) action_taken = RIGHT reached_state = ('E', 0, 0, 'D', 100)
current_state = ('E', 0, 0, 'D', 100) action_taken = HIT reached_state = ('E', 0, 0, 'D', 100)
current_state = ('E', 0, 0, 'D', 100) action_taken = HIT reached_state = ('E', 0, 0, 'R', 100)
current_state = ('E', 0, 0, 'R', 100) action_taken = HIT reached_state = ('E', 0, 0, 'R', 50)
current_state = ('E', 0, 0, 'R', 50) action_taken = HIT reached_state = ('E', 0, 0, 'D', 75)
current_state = ('E', 0, 0, 'D', 75) action_taken = HIT reached_state = ('E', 0, 0, 'R', 25)
current_state = ('E', 0, 0, 'R', 25) action_taken = HIT reached_state = ('E', 0, 0, 'D', 50)
current_state = ('E', 0, 0, 'D', 50) action_taken = HIT reached_state = ('E', 0, 0, 'D', 50)
current_state = ('E', 0, 0, 'D', 50) action_taken = HIT reached_state = ('E', 0, 0, 'R', 50)
current_state = ('E', 0, 0, 'R', 50) action_taken = HIT reached_state = ('E', 0, 0, 'D', 75)
current_state = ('E', 0, 0, 'D', 75) action_taken = HIT reached_state = ('E', 0, 0, 'D', 75)
current_state = ('E', 0, 0, 'D', 75) action_taken = HIT reached_state = ('E', 0, 0, 'D', 75)
current_state = ('E', 0, 0, 'D', 75) action_taken = HIT reached_state = ('E', 0, 0, 'R', 25)
current_state = ('E', 0, 0, 'R', 25) action_taken = HIT reached_state = ('E', 0, 0, 'R', 0)
```


### `(C, 2, 0, R, 100)`

```
current_state = ('C', 2, 0, 'R', 100) action_taken = UP reached_state = ('N', 2, 0, 'R', 100)
current_state = ('N', 2, 0, 'R', 100) action_taken = CRAFT reached_state = ('N', 1, 3, 'D', 100)
current_state = ('N', 1, 3, 'D', 100) action_taken = DOWN reached_state = ('C', 1, 3, 'D', 100)
current_state = ('C', 1, 3, 'D', 100) action_taken = RIGHT reached_state = ('E', 1, 3, 'R', 100)
current_state = ('E', 1, 3, 'R', 100) action_taken = HIT reached_state = ('E', 1, 0, 'D', 100)
current_state = ('E', 1, 0, 'D', 100) action_taken = HIT reached_state = ('E', 1, 0, 'D', 100)
current_state = ('E', 1, 0, 'D', 100) action_taken = HIT reached_state = ('E', 1, 0, 'D', 100)
current_state = ('E', 1, 0, 'D', 100) action_taken = HIT reached_state = ('E', 1, 0, 'D', 100)
current_state = ('E', 1, 0, 'D', 100) action_taken = HIT reached_state = ('E', 1, 0, 'D', 50)
current_state = ('E', 1, 0, 'D', 50) action_taken = HIT reached_state = ('E', 1, 0, 'D', 50)
current_state = ('E', 1, 0, 'D', 50) action_taken = HIT reached_state = ('E', 1, 0, 'D', 0)
```

# Task - 2
