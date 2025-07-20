# NPC Profile Creation

A text-based dungeon crawler that creates NPCs/PCs using structured belief systems (D&D alignments) and motivations, implemented as a research framework for studying LLM-driven character behavior.

## Disclaimer

This code is provided as-is, configured for the original research environment. No support is provided for adapting it to other systems or configurations.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/jstarace/NPC-Profile-Creation.git
    cd NPC-Profile-Creation
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On macOS/Linux
    # or
    venv\Scripts\activate     # On Windows
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up MongoDB (see [MongoDB documentation](https://docs.mongodb.com/manual/installation/))

## Configuration

### Environment Variables
Create a `.env` file in the root directory with the following variables:
```
MONGO_DB_USER=your_mongo_db_user
MONGO_DB_PASSWORD=your_mongo_db_password
OPENAI_API_KEY=your_openai_api_key
```

### Database Setup
Before running the game, you must populate the MongoDB database by running these scripts in order:

1. Populate game definitions:
    ```sh
    python utilities/populate_definitions.py
    ```

2. Populate random encounters:
    ```sh
    python utilities/populate_random_encounters.py
    ```

3. Populate random loot:
    ```sh
    python utilities/populate_random_loot.py
    ```

**Note**: The current implementation captures more detailed data than was used in the original research analysis.

### OpenAI Assistant Setup
The `the_assistant.py` file contains pre-configured OpenAI assistant IDs that are specific to the original research account. You'll need to create your own assistants in the OpenAI platform and update the `assistants` dictionary with your own IDs.

## Usage

### Starting Ollama (for Llama LLM)
If using Llama, first start the Ollama service:
```sh
ollama serve
```

### Running the Game
Run the main script and follow the interactive prompts:

```sh
python dungeon_crawler.py
```

### Example: Full Run with Llama
For a complete test using Llama with both alignment and motivation testing:

```
Please select the game type:
1.	Validate player control
2.	Generate Training Data
> 1

Please select the LLM you'd like to control your character (enter the number):
1. ChatGPT4o
2. Llama70B
3. Anthropic?
> 2

Do you want to generate control data (y/n)?:
> n

Please enter the name of the run:
> TestRun

Enter how many times you want to run the game:
> 1

What type of game (A)lignment, (L)oot, or (B)oth?
> b

Would you like to run the game with a specific alignment and motivation? (y/n):
> n

Would you like to run tests on a specific group? (y/n):
> n
```

This will run the full experiment testing all 36 alignment-motivation combinations.

## Project Structure

```
├── classes/              # Core game classes
├── connections/          # Database connections and operations
├── game_play/           # Main game logic
├── map_creation/        # Map generation modules
├── map_population/      # Content loading modules
├── map_visualization/   # Map display utilities
├── misc_files/          # Miscellaneous data files
├── utilities/           # Utility functions and database population
├── dungeon_crawler.py   # Main entry point
└── requirements.txt     # Python dependencies
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.