import random
import json
import os

# Trigram mapping from binary (bottom, middle, top) where 1 is Yang, 0 is Yin
TRIGRAM_MAP = {
    (1, 1, 1): "乾",
    (0, 0, 0): "坤",
    (1, 0, 0): "震",
    (0, 1, 0): "坎",
    (0, 0, 1): "艮",
    (0, 1, 1): "巽",
    (1, 0, 1): "離",
    (1, 1, 0): "兌",
}

def simulate_coin_toss():
    """
    Simulate 6 coin tosses.
    Each toss consists of 3 coins.
    Head (Yang) = 3, Tail (Yin) = 2.
    Returns a list of 6 integers (between 6 and 9).
    The list represents lines from bottom (初爻) to top (上爻).
    """
    tosses = []
    for _ in range(6):
        # random.choice([2, 3]) for 3 coins
        coins = [random.choice([2, 3]) for _ in range(3)]
        tosses.append(sum(coins))
    return tosses

def get_line_types(tosses):
    """
    Convert toss sums (6, 7, 8, 9) to Yin/Yang and distinguish moving lines.
    Returns a list of dictionaries with original and changed boolean values.
    6 (Old Yin): Original 0, Changed 1, Moving True
    7 (Young Yang): Original 1, Changed 1, Moving False
    8 (Young Yin): Original 0, Changed 0, Moving False
    9 (Old Yang): Original 1, Changed 0, Moving True
    """
    lines = []
    for toss in tosses:
        if toss == 6:
            lines.append({"original": 0, "changed": 1, "moving": True, "value": 6, "symbol": "x"})
        elif toss == 7:
            lines.append({"original": 1, "changed": 1, "moving": False, "value": 7, "symbol": "—"})
        elif toss == 8:
            lines.append({"original": 0, "changed": 0, "moving": False, "value": 8, "symbol": "--"})
        elif toss == 9:
            lines.append({"original": 1, "changed": 0, "moving": True, "value": 9, "symbol": "o"})
    return lines

def get_trigrams(lines_binary):
    """
    Convert a list of 6 binary values (0/1) to lower and upper trigram names.
    lines_binary[0] is the bottom-most line.
    """
    lower_binary = tuple(lines_binary[0:3])
    upper_binary = tuple(lines_binary[3:6])
    
    lower_name = TRIGRAM_MAP[lower_binary]
    upper_name = TRIGRAM_MAP[upper_binary]
    
    return {"lower": lower_name, "upper": upper_name}

def load_hexagrams_data():
    """Load the 64 hexagrams JSON data."""
    # Handle the path relative to this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "data", "hexagrams", "64_hexagrams.json")
    
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_hexagram(trigrams, hexagrams_data):
    """Find a hexagram in the data by its upper and lower trigrams."""
    for h in hexagrams_data:
        if h["trigrams"]["upper"] == trigrams["upper"] and h["trigrams"]["lower"] == trigrams["lower"]:
            return h
    return None

def perform_divination():
    """
    Execute the full divination process.
    Returns a dictionary with all the results.
    """
    tosses = simulate_coin_toss()
    lines_info = get_line_types(tosses)
    
    original_binary = [line["original"] for line in lines_info]
    changed_binary = [line["changed"] for line in lines_info]
    
    original_trigrams = get_trigrams(original_binary)
    changed_trigrams = get_trigrams(changed_binary)
    
    hexagrams_data = load_hexagrams_data()
    
    original_hexagram = find_hexagram(original_trigrams, hexagrams_data)
    changed_hexagram = find_hexagram(changed_trigrams, hexagrams_data)
    
    # Are there any moving lines?
    has_moving_lines = any(line["moving"] for line in lines_info)
    
    return {
        "tosses": tosses,
        "lines_info": lines_info,
        "original_hexagram": original_hexagram,
        "changed_hexagram": changed_hexagram if has_moving_lines else None,
        "original_trigrams": original_trigrams,
        "changed_trigrams": changed_trigrams if has_moving_lines else None,
        "has_moving_lines": has_moving_lines
    }
