import os
from evolve_chip import evolve, EvolutionGoal, DefaultAIEngine

ai_engine = DefaultAIEngine()

@evolve(goals=[EvolutionGoal.READABILITY, EvolutionGoal.PERFORMANCE], ai_engine=ai_engine)
def say_hello(name: str = "World") -> None:
    print(f"Hello, {name}!")

if __name__ == "__main__":
    os.environ["EVOLVE_MODE"] = "development"
    say_hello("Alice")
