"""
Represents a player character with tracking for performance analysis.

Stores player state including room visits, decisions made, alignment/motivation
assignments, and performance scoring. Used for analyzing how well LLMs
maintain consistent character behavior throughout gameplay.

Tracks:
- Room visitation history and movement patterns
- Encounter and loot interaction decisions
- Turn count and completion status
- Actual vs expected points for alignment/motivation consistency
- Test run identification for data analysis

Performance scoring compares actual LLM decisions against expected
behavior for the assigned character profile.
"""

class Player:

    def __init__(self, name, loc, run, alignment=None, motivation=None):
        self.rooms_visited = []
        self.name = name
        self.start_location = loc
        self.alignment = alignment if alignment is not None else getattr(self, 'alignment', None)
        self.motivation = motivation if motivation is not None else getattr(self, 'motivation', None)
        self.encounter_ids = []
        self.loot_ids = []
        self.decision = []
        self.turns = 0
        self.points = 0
        self.expected_points = 0
        self.test_run = run

    def set_points(self, points):
        self.points += points
    def room_visit(self, id):
        self.rooms_visited.append(id)
    def encounter(self, id):
        self.encounter_ids.append(id)
    def loot(self, id):
        self.loot_ids.append(id)
    def decisions(self, option=None, loot_id=None, encounter_id=None):
        self.decision.append((option, loot_id if loot_id is not None else encounter_id))
    def set_turns(self, turns):
        self.turns = turns
    def set_expected_points(self, points):
        self.expected_points += points
    def set_completion(self, completion):
        self.completed = completion
    def print_core_details(self):
        print(f"Player Name: {self.name}\nAlignment: {self.alignment}\nMotivation: {self.motivation}")
        print(f"Test Run: {self.test_run}")
        print(f"Completed: {self.completed}")
        print(f"Points: {self.points}\nExpected Points: {self.expected_points}")
