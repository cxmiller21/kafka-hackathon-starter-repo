"""Generate fake songs and users and save them to a json file
to be used in the `kafka-producer.py` script.

Limitations:
- The generated songs are not streamed to Kafka.
- There is only one song per artist.
    - `--num-songs=20` will generate 20 fake songs by 20 different fake artists.

Example:
    # Simple
    python generate-streaming-songs.py
    # Full
    python generate-streaming-songs.py --num-songs 100 --num-users 100 --song-output-file streaming-songs.json --user-output-file streaming-users.json

Args:
    num_songs (int): Optional - Number of songs to generate. Default is 100.
    num_users (int): Optional - Number of users to generate. Default is 100.
    output_file (str): Optional - Path to save the generated songs. Default is `streaming-songs.json`.
    user_output_file (str): Optional - Path to save the generated users. Default is `streaming-users.json`.

Example CSV output:
song_id,song_title,artist_name,album_name,genre,duration_seconds
"e7b2b2f7-5b1d-4b0a-9b1c-1a6f9c9b1f7b","Lose Yourself","Eminem","8 Mile","Hip Hop",313
"""
import argparse
import json
import os
import random

from collections import OrderedDict
from datetime import datetime
from faker import Faker
from loguru import logger as log
from pathlib import Path

fake = Faker() # Defaults to `en_US`

MUSIC_GENRES = ["Pop", "Rock", "Jazz", "Classical", "Hip Hop", "Electronic"]

def generate_song_data(num_songs: int) -> list:
    """Generate fake songs."""
    songs = {}
    for _ in range(num_songs):
        # release_datetime = fake.date_time_between(start_date='-5y', end_date='now')
        # release_datetime_str = datetime.strftime(release_datetime, "%Y-%m-%d")
        song = {
            "song_id": fake.uuid4(),
            "song_title": fake.sentence(nb_words=3),
            "artist_name": fake.name(),
            "album_name": fake.sentence(nb_words=2),
            "release_date": fake.date(),
            "genre": fake.random_element(elements=MUSIC_GENRES),
            "duration_seconds": fake.random_int(min=60, max=300)  # 1 to 5 minutes
        }
        songs[song["song_id"]] = song
    return songs


def generate_user_data(num_users: int) -> dict:
    """Generate fake user profiles."""
    users = {}
    faker_instances = {
        "US": fake,
        "Canada": Faker('en_CA'),
        "Mexico": Faker('es_MX'),
        "France": Faker('fr_FR')
    }
    for _ in range(num_users):
        user_id = fake.uuid4()
        user_country = fake.random_element(
                elements=OrderedDict([
                    ("US", 0.5),            # Generates 50% of the time
                    ("Canada", 0.2),        # Generates 20% of the time
                    ("Mexico", 0.2),        # Generates 20% of the time
                    ("France", 0.1),        # Generates 10% of the time
                ])
            )

        users[user_id] = {
            "user_id": user_id,
            "name": fake.name(),
            "age": fake.random_int(min=18, max=70),
            "country": user_country,
            "address": faker_instances[user_country].address().replace("\n", ", "),
            "subscription_type": fake.random_element(elements=["Free", "Premium", "Family"]),
            "favorite_genres": random.sample(MUSIC_GENRES, random.randint(1, len(MUSIC_GENRES)))
        }
    return users


def save_data_to_json(data: dict, output_file: str) -> None:
    """Save data to a JSON file."""
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    log.info(f"Generated {len(data)} items saved to {output_file}")
    return None


def main():
    parser = argparse.ArgumentParser(description="Generate fake songs for music streaming.")
    parser.add_argument("--num-songs", type=int, default=100, help="Number of songs to generate.", required=False)
    parser.add_argument("--num-users", type=int, default=100, help="Number of users to generate.", required=False)
    parser.add_argument("--song-output-file", type=str, default="streaming-songs.json", help="Path to save the generated songs.", required=False)
    parser.add_argument("--user-output-file", type=str, default="streaming-users.json", help="Path to save the generated users.", required=False)
    args = parser.parse_args()

    # Initialize Faker
    fake = Faker()

    current_dir = Path(__file__).resolve().parent

    # Generate fake songs
    songs = generate_song_data(args.num_songs)
    output_path = current_dir / args.song_output_file
    save_data_to_json(songs, output_path)

    # Generate fake users
    users = generate_user_data(args.num_users)
    output_path = current_dir / args.user_output_file
    save_data_to_json(users, output_path)

    log.info(f"Successfully generated {args.num_songs} songs and {args.num_users} users.")

if __name__ == "__main__":
    main()
