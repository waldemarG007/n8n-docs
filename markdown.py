import os
import glob

def read_markdown_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Fehler beim Lesen der Datei {filepath}: {e}")
        return ""

def create_markdown_file(filepath, content):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Datei erstellt: {filepath}")
        return True
    except Exception as e:
        print(f"Fehler beim Erstellen der Datei {filepath}: {e}")
        return False

def concat_markdown_files(output_filepath):
    # Manuell zu durchsuchende Verzeichnisse
    directories = [
        ".",
        "docs",
        "docs-site-feature-tests",
        "document-templates",
        "styles",
        "_doctools",
        "_lychee",
        "_overrides",
        "_snippets",
        "_submodules",
        "_yaml",
        "_snippets/code",
        "_snippets/data",
        "_snippets/data-function-code",
        "_snippets/flow-logic",
        "_snippets/integrations",
        "_snippets/manage-cloud",
        "_snippets/privacy-security",
        "_snippets/self-hosting",
        "_snippets/source-control-environments",
        "_snippets/try-it-out",
        "_snippets/user-management",
        "_snippets/workflows",
        "_snippets/workflows/executions",
        "_snippets/workflows/templates",
        "_self-hosting/configuration/environment-variables",
        "_integrations/builtin",
        "_integrations/creating-nodes",
        "_integrations/builtin/app-nodes",
        "_integrations/builtin/cluster-nodes",
        "_integrations/builtin/core-nodes",
        "_integrations/builtin/credentials",
        "_integrations/builtin/credentials/email",
        "_integrations/builtin/credentials/generic-auth",
        "_integrations/builtin/credentials/google",
        "_integrations/cluster-nodes/langchain-root-nodes/langchaincode"
    ]
    print(f"Zu durchsuchende Verzeichnisse: {directories}")

    combined_content = ""
    for directory in directories:
        # Bereinigen des Pfads, um doppelte Schrägstriche zu vermeiden
        search_pattern = os.path.join(directory, "**/*.md")
        print(f"Suche nach Markdown-Dateien im Verzeichnis: {directory}")
        
        # Glob-Suche nach Markdown-Dateien im aktuellen Verzeichnis
        file_paths = glob.glob(search_pattern, recursive=True)
        print(f"Gefundene Dateien: {file_paths}")
        for file_path in file_paths:
            content = read_markdown_file(file_path)
            if content:
                combined_content += f"\n<!-- Inhalt von {file_path} -->\n"
                combined_content += content

    if combined_content:
        if create_markdown_file(output_filepath, combined_content):
            print(f"Die zusammengeführte Datei wurde erstellt: {output_filepath}")
        else:
            print("Fehler beim Erstellen der zusammengeführten Datei.")
    else:
        print("Kein Inhalt zum Zusammenführen gefunden.")

# Name der Ausgabedatei
output_file = "combined.md"

# Zusammenführen der Markdown-Dateien
concat_markdown_files(output_file)