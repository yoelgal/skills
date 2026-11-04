"""The spoken script: the single source of truth for tts.py, the scenes and make_script.py.

CHAPTERS: one entry per chapter, in order: (scene class, title, [(beat id, spoken text), ...]).
Chapter N renders from scenes/chNN.py. Write spoken text for the ear.
"""

TITLE = "How a hash table finds a key"
OUTPUT = "explainer.mp4"
VOICE = "af_heart"
SPEED = 1.0

CHAPTERS = [
    (
        "Ch01Problem",
        "1. Finding one key in a million",
        [
            ("c1a", "Say you keep a million names, and you want to know if one of them is on the list."),
            ("c1b", "A plain list makes you check names one at a time. On average, that is half a million checks."),
        ],
    ),
    (
        "Ch02Buckets",
        "2. Buckets and a hash",
        [
            ("c2a", "A hash table splits the names into buckets. A hash function turns each name into a bucket number."),
            ("c2b", "To find a name, hash it, go straight to its bucket, and check only the few names inside."),
        ],
    ),
]
