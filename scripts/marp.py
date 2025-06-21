
import os
import subprocess
import yaml

import config as cfg

def process_markdown_files(base_path):
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith('.md'):
                md_file = os.path.join(root, file)
                print(f"Processing {md_file}")
                with open(md_file, 'r', encoding="utf8") as f:
                    content = f.read()
                    if content.startswith('---'):
                        end = content.find('---', 3)
                        if end != -1:
                            front_matter = yaml.safe_load(content[3:end])
                            if 'marp' in front_matter:
                                if front_matter.get('marp') == True:
                                    remove_links(md_file)
                                    generate_slides(md_file)
                                    append_links(md_file)
                                elif front_matter.get('marp') == False:
                                    remove_generated_files(md_file)
                                    remove_links(md_file)

def run_marp(format, input, output):
    if format in ['html','pdf']:
        cmd = ['marp', '--allow-local-files', f'--{format}','--theme-set', cfg.marp_theme_path, '--output', output, input]
        # cmd = ['marp', '--output', output, input]
        print(" ".join(cmd))
        subprocess.run(cmd)
        # subprocess.run(cmd, shell=True, check=True)
    else:
        print("Bad format type.  Allowed: html or pdf")

def generate_slides(md_file):
    base_name = os.path.splitext(md_file)[0]
    html_file = f"{base_name}_slides.html"
    pdf_file = f"{base_name}_slides.pdf"
    run_marp('html', md_file, html_file)
    run_marp('pdf', md_file, pdf_file)

def append_links(md_file):
    base_name = os.path.splitext(os.path.basename(md_file))[0]
    print("FILE: ",base_name)
    html_file = f"{base_name}_slides.html"
    pdf_file = f"{base_name}_slides.pdf"
    links = f"""\n<div id="slide_menu" class="grid cards" markdown>\n- [:fontawesome-brands-html5: __HTML__ Slides: Slides]({html_file})\n- [:fontawesome-solid-file-pdf: __PDF__ Document: Slides]({pdf_file})</div>"""
    with open(md_file, 'a') as f:
        f.write(links)

def remove_generated_files(md_file):
    base_name = os.path.splitext(md_file)[0]
    html_file = f"{base_name}_slides.html"
    pdf_file = f"{base_name}_slides.pdf"
    if os.path.exists(html_file):
        os.remove(html_file)
    if os.path.exists(pdf_file):
        os.remove(pdf_file)

def remove_links(md_file):
    with open(md_file, 'r', encoding="utf8") as f:
        lines = f.readlines()
    with open(md_file, 'w', encoding="utf8") as f:
        for line in lines:
            if not line.startswith('<div id="slide_menu"') and not line.startswith('- [:fontawesome-brands-html5: __HTML__ Slides: Slides]') and not line.startswith('- [:fontawesome-solid-file-pdf: __PDF__ Document: Slides]'):
                f.write(line)

# Example usage
print (f"Processing markdown files from: {cfg.markdown_source_path}")
process_markdown_files(cfg.markdown_source_path)
print ("Done processing markdown files")
