from PIL import Image
from os import listdir
from os.path import splitext

target_directory = '.'
target = '.png'

for file in listdir(target_directory):
	filename, extension = splitext(file)
	try:
	    if extension not in ['.py']:
	        im = Image.open(filename + extension)
	        im = im.resize((72,72))
	        im.save(filename + target)
	except OSError:
	    print('Cannot convert %s' % file)

