import sys
from os.path import abspath
from pypdf import PdfReader




filename=sys.argv[1]
dest_dir='.'
if (len(sys.argv) > 2 and sys.argv[2]):
	dest_dir=sys.argv[2]
dest_dir=abspath(dest_dir)

print(f"Starting convertion of file {filename} and saving it to {dest_dir}.")
try: 
	reader = PdfReader(filename)
except Exception as e:
	print(f"Failed to open {filename}")
	exit(1)

text=''
images=[]
for page in reader.pages:
	text+=page.extract_text()
	for img in page.images:
		images.append(img.data)

	
dest=f"{dest_dir}/{filename.replace('.pdf','.txt')}"
print(f'Saving text to {dest}...')

with open(dest, 'w', encoding='utf-8') as f:
	f.write(text)
dest=dest.replace('.txt', '')
print(f'Saving images to {dest}-x.png')
for i, img in enumerate(images):
	with open(f'{dest}-{i+1}.png', 'wb') as i:
		i.write(img)




