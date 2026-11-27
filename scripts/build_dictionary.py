import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

source = ROOT / "dict.txt"
output = ROOT / "data" / "dictionary.json"

dictionary = []

with source.open("r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        parts = line.split(maxsplit=2)

        if len(parts) != 3:
            raise ValueError(
                f"Invalid entry at line {line_number}: {line}"
            )

        part_of_speech, word, translation = parts

        dictionary.append({
            "partOfSpeech": part_of_speech,
            "word": word,
            "translation": translation
        })

output.parent.mkdir(parents=True, exist_ok=True)

with output.open("w", encoding="utf-8") as file:
    json.dump(
        dictionary,
        file,
        ensure_ascii=False,
        indent=2
    )

print(f"Successfully generated {output}")
print(f"Entries: {len(dictionary)}")
