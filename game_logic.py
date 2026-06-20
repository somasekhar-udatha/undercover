import json
import random


def load_word_pairs():
    with open("data.json", "r") as f:
        return json.load(f)


def initialize_game(players):
    pairs = load_word_pairs()
    pair = random.choice(pairs)

    # 50-50 which word is civilian vs imposter
    if random.random() < 0.5:
        civilian_word = pair["word_1"]
        imposter_word = pair["word_2"]
    else:
        civilian_word = pair["word_2"]
        imposter_word = pair["word_1"]

    imposter = random.choice(players)

    player_data = {}
    for p in players:
        if p == imposter:
            player_data[p] = {"word": imposter_word, "role": "imposter"}
        else:
            player_data[p] = {"word": civilian_word, "role": "civilian"}

    alive_players = list(players)

    return {
        "player_data": player_data,
        "imposter": imposter,
        "civilian_word": civilian_word,
        "imposter_word": imposter_word,
        "alive_players": alive_players,
    }


def eliminate_player(alive_players, player):
    alive_players = [p for p in alive_players if p != player]
    return alive_players


def check_winner(alive_players, imposter, eliminated_player=None):
    # Just eliminated the imposter
    if eliminated_player == imposter:
        return "civilian"

    # Imposter is still alive and only 2 players remain
    if imposter in alive_players and len(alive_players) <= 2:
        return "imposter"

    return None