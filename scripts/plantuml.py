import os
import subprocess

import config as cfg

def process_puml_files(base_path):
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith('.puml'):
                puml_file = os.path.join(root, file)
                generate_graph(puml_file)

def generate_graph(puml_file):
    jar_path = './scripts/plantuml/plantuml-mit-1.2024.6.jar'
    cmd = ['java', '-jar', jar_path, puml_file]
    print("Executing: ", " ".join(cmd))
    subprocess.run(cmd, check=True)

# Example usage
print (f"Processing puml files from: {cfg.markdown_source_path}")
process_puml_files(cfg.markdown_source_path)
print ("Done processing puml files")