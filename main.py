import os
import csv
import re
from unidecode import unidecode


def sanitize_string(input_str):
    # Sonderzeichen in ihre ASCII-entsprechenden Formen umwandeln
    input_str = unidecode(input_str)
    # Erlaubte Zeichen definieren (a-z, 0-9, -, _, @, space)
    sanitized_str = re.sub(r'[^a-zA-Z0-9-_@ ]', '_', input_str).lower()
    # Mehrere aufeinanderfolgende Unterstriche durch einen einzelnen Unterstrich ersetzen
    sanitized_str = re.sub(r'_+', '_', sanitized_str)
    # Whitespace am Anfang und Ende entfernen
    sanitized_str = sanitized_str.strip()
    # Sicherstellen, dass der String nicht mit einem Unterstrich endet
    if sanitized_str.endswith('_'):
        sanitized_str = sanitized_str[:-1]
    return sanitized_str


def process_csv(input_file_path):
    # Basename der Eingabedatei extrahieren (ohne Pfad)
    base_name = os.path.basename(input_file_path)
    # Dateinamen und Erweiterung trennen
    name, ext = os.path.splitext(base_name)
    # Neuen Dateinamen mit Suffix _nf.csv erstellen
    output_base_name = f"{name}_nf{ext}"
    # Vollständigen Pfad für die Ausgabedatei erstellen
    output_file_path = os.path.join(os.path.dirname(input_file_path), output_base_name)

    with open(input_file_path, mode='r', encoding='utf-8') as infile, \
            open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['label', 'value']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()

        for row in reader:
            label = row['label']
            value = sanitize_string(label)
            writer.writerow({'label': label, 'value': value})


def main():
    input_file_path = input("Bitte geben Sie den Pfad zur CSV-Datei ein: ")

    if not os.path.isfile(input_file_path):
        print(f"Die Datei {input_file_path} existiert nicht.")
        return

    process_csv(input_file_path)
    # Basename der Eingabedatei extrahieren (ohne Pfad)
    base_name = os.path.basename(input_file_path)
    # Dateinamen und Erweiterung trennen
    name, ext = os.path.splitext(base_name)
    # Neuen Dateinamen mit Suffix _nf.csv erstellen
    output_base_name = f"{name}_nf{ext}"
    print(f"Neue CSV-Datei wurde erstellt: {output_base_name}")


if __name__ == "__main__":
    main()