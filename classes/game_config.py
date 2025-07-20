class GameConfig:
    def __init__(self, populated_map, game_ids, player_name, run_name, game_type, alignment_key, motivation_key, key, is_control, llm, training_data, starting_positions=None):
        self.populated_map = populated_map
        self.game_ids = game_ids
        self.player_name = player_name
        self.run_name = run_name
        self.game_type = game_type
        self.alignment_key = alignment_key
        self.motivation_key = motivation_key
        self.key = key
        self.is_control = is_control
        self.llm = llm
        self.training_data = training_data
        self.starting_positions = starting_positions

    def __str__(self):
        return (f"GameConfig(\n"
                f"  populated_map={self.populated_map},\n"
                f"  game_ids={self.game_ids},\n"
                f"  player_name={self.player_name},\n"
                f"  run_name={self.run_name},\n"
                f"  game_type={self.game_type},\n"
                f"  alignment_key={self.alignment_key},\n"
                f"  motivation_key={self.motivation_key},\n"
                f"  key={self.key},\n"
                f"  is_control={self.is_control},\n"
                f"  llm={self.llm}\n"
                f"  training_data={self.training_data}\n"
                f"  starting_positions={self.starting_positions}\n"
                f")")

    def to_dict(self):
        return {
            'populated_map': [room.to_dict(pop_map=self.populated_map) for room in self.populated_map],
            'game_ids': [str(game_id) for game_id in self.game_ids],
            'player_name': self.player_name,
            'run_name': self.run_name,
            'game_type': self.game_type,
            'alignment_key': self.alignment_key,
            'motivation_key': self.motivation_key,
            'key': self.key,
            'is_control': self.is_control,
            'llm': self.llm,
            'training_data': self.training_data,
            'starting_positions': self.starting_positions
        }