import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

source = ROOT / "dict.txt"
output = ROOT / "data" / "dictionary.json"

# Alphabetical order
alphabet = (
    "aäâ"
    "bcç"
    "deê"
    "fgh"
    "iî"
    "jklmn"
    "oöô"
    "prst"
    "uû"
    "vwxz"
)

order = {
    char: index
    for index, char in enumerate(alphabet)
}


def sort_key(word):
    word = word.casefold()

    return tuple(
        order.get(char, len(order) + ord(char))
        for char in word
    )


entries = []
comments = []

with source.open("r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            comments.append(line)
            continue

        parts = line.split(maxsplit=2)

        if len(parts) != 3:
            raise ValueError(
                f"Invalid entry at line {line_number}: {line}"
            )

        part_of_speech, word, translation = parts

        entries.append({
            "partOfSpeech": part_of_speech,
            "word": word,
            "translation": translation
        })


# Sort entries alphabetically by word
entries.sort(key=lambda entry: sort_key(entry["word"]))


# Rewrite dict.txt
with source.open("w", encoding="utf-8", newline="\n") as file:
    for comment in comments:
        file.write(comment + "\n")

    if comments and entries:
        file.write("\n")

    for entry in entries:
        file.write(
            f'{entry["partOfSpeech"]} '
            f'{entry["word"]} '
            f'{entry["translation"]}\n'
        )


# Generate JSON
output.parent.mkdir(parents=True, exist_ok=True)

with output.open("w", encoding="utf-8") as file:
    json.dump(
        entries,
        file,
        ensure_ascii=False,
        indent=2
    )

print("Dictionary sorted successfully.")
print(f"Entries: {len(entries)}")
print(f"JSON generated: {output}")
