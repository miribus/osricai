import json
import os

def load_monsters_from_json(file_path=os.path.join(os.getcwd(), "rogue_monsters","monsters.json")):
    """Load monster data from a JSON file."""
    with open(file_path, "r") as f:
        data = json.load(f)

    monster_list = []
    for monster in data["monsters"]:
        # Create a Monster object (adjust attributes based on your class structure)
        new_monster = monsters.Monster(
            name=monster["name"],
            hp=monster["hp"],
            attack=monster["attack"],
            movement=monster["movement"],
            behavior=monster["behavior"]
        )
        monster_list.append(new_monster)

    return monster_list
