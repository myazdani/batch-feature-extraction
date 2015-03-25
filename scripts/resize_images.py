import os
from PIL import Image 

file_save_type = ".gif"

src_path, image_type = "/Users/myazdaniUCSD/Documents/misc_scripts/norooz2048/img/212", ".jpg"
 
image_paths = []  
for root, dirs, files in os.walk(src_path):
  image_paths.extend([os.path.join(root, f) for f in files if f.endswith(image_type)])

for image_path in image_paths:
	pil_im = Image.open(image_path)
	pil_im.save(image_path.split(".")[0] + file_save_type)