import pyimgur
import keys

CLIENT_ID = keys.CLIENT_ID


# im = pyimgur.Imgur(CLIENT_ID)
# image = im.get_image('S1jmapR')
# print(image.title) # Cat Ying & Yang
# print(image.link) # http://imgur.com/S1jmapR.jpg

def upload_file(path, title):
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(path, title=title)
    return uploaded_image.link

