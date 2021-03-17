from os import walk
import os, sys, stat
#from mtlib import rotate_image

#mtlib cut start
def printc(*t):# print to console
	tc=()
	for l in t:
		lc=str(l).encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
		tc+=(lc,)
	print(*tc)
def rotate_image(path_name_arr):
				#exif_bytes = piexif.dump(exif_data)
				#exif_bytes = image.info['exif']				
				root,justname,ext=path_name_arr
				path_name=os.path.join(root,justname+'.'+ext)
				if ext.upper() in ('JPG','TIFF'):	
					printc(path_name)
					import piexif
					try:
						exif_dict_dig=piexif.load(path_name)
					except BaseException as e:
						if hasattr(e, 'message'): printc(e.message)
					else:
						ori=exif_dict_dig['0th'].get(0x0112)#exif_data['Orientation']	
						#print(ori)
						if ori and ori != 1:	#vendor=exif_dict_dig['0th'].get(0x010f).decode()#'Make'
							model_by=exif_dict_dig['0th'].get(0x0110)
							version=exif_dict_dig['Exif'].get(0x9000)
							is_modern_version=version==b'0221'
							#print('v',version,is_modern_version)
							if model_by:
								model=model_by.decode()
								model_w=('iPhone SE','iPhone 4','iPhone 4S','COOLPIX S4300','iPad','DMC-LS80','NIKON D5100','GT-I9192')
								model_b=('Canon EOS 500D','NIKON D70','C2Z,D520Z,C220Z','Canon PowerShot A2200')
								#if vendor in ('Apple',):
								
							if is_modern_version or (model in model_w):
								from PIL import Image	
								image=Image.open(path_name)
								if ori == 3:
									image=image.rotate(180, expand=True)
								elif ori == 6:
									image=image.rotate(270, expand=True)
								elif ori == 8:
									image=image.rotate(90, expand=True)#Left
								#exif_data['Orientation']=1
								exif_dict_dig['0th'][0x0112]=1 #Orientation				
								#print(exif_dict_dig['0th'].keys())	
								#try:
								exif_bytes = piexif.dump(exif_dict_dig)
								#image.save(root+justname+'_R.'+ext, quality=90, exif=exif_bytes)
								os.chmod(path_name, stat.S_IWRITE)
								image.save(path_name, quality=90, exif=exif_bytes)
								print('rotated')
								'''except BaseException as e:
									if hasattr(e, 'message'): printc(e.message)'''
								image.close()									
							else:
								if model not in model_b and 'C2Z' not in model:
									print('Check orientation and add camera model to black or white list:',ori,model)
									input()#skip
#mtlib cut end

#start 
# py photo_rotate.py #current folder
# py photo_rotate.py "d:\temp\106APPLE\1"

# pyinstaller --onefile --windowed photo_rotate.py
if len(sys.argv)<2:     
	'''print('No directory set.')    
	exit()'''
	print('Usage: py '+sys.argv[0]+' [path_to_folder]')
	print('Working with current directory...')
	top=os.getcwd()
else: top=sys.argv[1].replace('"','').replace("'","")
		
def rotate_sub():
	global root,files
	a=''
	for name in files:		
		#ext=name.split('.')[1]
		#justname=name.split('.')[0]
		justname,ext=os.path.splitext(name)
		ext=ext[1:]             

		#rotate
		rotate_image((root,justname,ext))			

		#break
		'''for name in dirs:
			os.rmdir(os.path.join(root, name))'''

if os.path.isfile(top):
	root=os.path.split(top)[0]
	files=[top,]
	rotate_sub()
else:	
	for root, dirs, files in os.walk(top, topdown=False):
	#for root, dirs, files in os.walk('D:/temp/!photo/2019/105APPLE', topdown=False):
		rotate_sub()