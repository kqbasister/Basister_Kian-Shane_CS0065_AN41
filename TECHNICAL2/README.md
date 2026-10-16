# Technical Assessment 2: Rule-Based Vacuum Cleaner Agent

A simple Python program that simulates a vacuum cleaner agent in two rooms, A and B. The agent follows predefined rules to clean rooms or move between them.

## Requirements

- Python 3.6 or newer
- No additional libraries are needed.

## How to Run

1. Open a terminal in this folder.
2. Run the program:

   ```bash
   python main.py
   ```

3. Enter `dirty` or `clean` for each room.
4. Enter the number of simulation steps as a whole number of zero or more.

The agent starts in room A. Each step performs one action and displays the agent's location after the action, the action taken, and the current state of both rooms.

## Task Breakdown

### Task 1: Set Up the Environment

- Stores rooms A and B in a Python dictionary.
- Lets the user choose each room's initial state.
- Uses `is_dirty()` to check a room and `clean_room()` to change its state to clean.

### Task 2: Implement the Rule-Based Agent

- Defines the `VacuumAgent` class.
- Uses `perceive_and_act()` to apply two rules: clean the current room if it is dirty, or move to the other room if it is clean.
- Uses `move()` to switch between rooms A and B.

### Task 3: Run the Simulation

- Asks the user how many steps to run.
- Runs the agent in a loop for exactly that number of steps.
- Prints the location, action, and environment after every step.

## Example

With both rooms set to `dirty` and the number of steps set to `4`, the simulation follows this sequence:

| Step | Action | Location after action | Room A | Room B |
| --- | --- | --- | --- | --- |
| 1 | Clean room A | A | clean | dirty |
| 2 | Move from A to B | B | clean | dirty |
| 3 | Clean room B | B | clean | clean |
| 4 | Move from B to A | A | clean | clean |

## Program Behavior

- Invalid room states and step counts prompt the user to try again.
- Room input accepts uppercase or lowercase letters and ignores surrounding spaces.
- Entering zero steps displays the initial state and ends the simulation without taking an action.
- When both rooms are clean, the agent continues moving between them until the requested steps are complete.
