import secrets
import os
from modules import app
from PIL import Image
'''
input: 
processing: 
Output:	None.
'''
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    picture_fn = random_hex + '.jpg'
    picture_path = os.path.join(app.root_path, 'static\profiles', picture_fn)
    form_picture.save(picture_path)
    print(picture_path)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    rgb_im = i.convert('RGB')
    rgb_im.save(picture_path)


    return picture_fn