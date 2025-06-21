import os
import base64

import config as cfg

def encode_images_to_base64(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                if filename == 'topic.png':
                    class_name = "section.topic,section.intro"
                else:
                    class_name = "section"

                print(f"/* {filename} */")
                print(f"{class_name} {{ background-image: url(data:image/png;base64,{encoded_string}); }} \n")

# Example usage
encode_images_to_base64(cfg.marp_theme_image_path)

# delete the existing images from the marp/notebook.css file
# python scripts/encode.py >> marp/notebook/notebook.css