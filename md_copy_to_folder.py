import os
import shutil

# Pfad zum Zielordner
zielordner = "md_docs"

# Überprüfen, ob der Zielordner existiert, wenn nicht, erstellen
if not os.path.exists(zielordner):
    os.makedirs(zielordner)

# Liste der Ordner, die durchsucht werden sollen
ordner_liste = ["."]  # Hauptordner und alle Unterordner

# Liste der Dateien, die kopiert werden sollen
files_to_copy = ["configuration.md", "deployment.md"]

# Durchsuchen der Ordner und Kopieren der Markdown-Dateien
for ordner in ordner_liste:
    for root, dirs, files in os.walk(ordner):
        for file in files:
            if file.endswith(".md"):
                src_path = os.path.join(root, file)
                dst_path = os.path.join(zielordner, file)
                if src_path != dst_path:
                    try:
                        shutil.copy2(src_path, dst_path)
                    except PermissionError:
                        print(f"Fehler beim Kopieren von {src_path}: Datei wird von einem anderen Prozess verwendet")

# Kopieren der spezifischen Dateien
for file in files_to_copy:
    if os.path.exists(file):
        src_path = os.path.join(os.getcwd(), file)
        dst_path = os.path.join(zielordner, file)
        if src_path != dst_path:
            try:
                shutil.copy2(src_path, dst_path)
            except PermissionError:
                print(f"Fehler beim Kopieren von {src_path}: Datei wird von einem anderen Prozess verwendet")

print("Markdown-Dateien wurden erfolgreich kopiert.")