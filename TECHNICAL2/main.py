#1. Set up the two-room environment.
def get_room_state(room):
    while True:
        state = input(f"Enter the state of room {room} (dirty/clean): ").strip().lower()
        if state in ("dirty", "clean"):
            return state
        print("Please enter dirty or clean.")


def is_dirty(environment, room):
    return environment[room] == "dirty"


def clean_room(environment, room):
    environment[room] = "clean"


#2. Create an agent that follows two simple rules.
class VacuumAgent:
    def __init__(self, environment):
        self.environment = environment
        self.location = "A"

    def move(self):
        # Switch to the other room.
        if self.location == "A":
            self.location = "B"
        else:
            self.location = "A"

    def perceive_and_act(self):
        # Rule 1: Clean the current room if it is dirty.
        if is_dirty(self.environment, self.location):
            clean_room(self.environment, self.location)
            return f"Cleaned room {self.location}"

        # Rule 2: Move to the other room if the current room is clean.
        previous_room = self.location
        self.move()
        return f"Moved from room {previous_room} to room {self.location}"


#3. Run the simulation for the user's chosen number of steps.
def main():
    print("RULE-BASED VACUUM CLEANER AGENT")
    environment = {
        "A": get_room_state("A"),
        "B": get_room_state("B"),
    }
    agent = VacuumAgent(environment)

    # Accept a whole number of steps, including zero.
    while True:
        try:
            steps = int(input("Enter the number of simulation steps: "))
            if steps >= 0:
                break
        except ValueError:
            pass
        print("Please enter a whole number of zero or more.")

    print(f"\nInitial location: {agent.location}")
    print(f"Initial environment: {environment}")

    for step in range(1, steps + 1):
        action = agent.perceive_and_act()
        print(f"\nStep {step}")
        print(f"Current location: {agent.location}")
        print(f"Action: {action}")
        print(f"Environment: {environment}")

    print("\nSimulation complete.")


if __name__ == "__main__":
    main()
