import POI_flickr
import urllib
import shutil

def IsinTas(lat, longt):
	flag = 0
	if(lat < -43.5):
		return False;
	if lat > -40.5 :
		return False;
	if longt > 149.0:
		return False;
	if longt < 143.0:
		return False;
	return True;

def FindPhotosByText(in_text):
	photos = POI_flickr.photos_search(text=in_text)
	users = []
	for photo in photos:
		try:
			# print photo.owner
			user_id = str(photo.owner).split('>')[0].split(' ')[2]
			# print user_id
			ulat, ulongt = photo.getLocation()
			# des = photo.title.text
			if(IsinTas(float(ulat),float(ulongt))):
				# print "Yes"
				users.append(user_id)
			# urls.append(url)
			# print title
			print user_id
		except:
			continue
	# for url in urls:
	# 	filename, mime = urllib.urlretrieve(url)
	# 	name = url.split('/')[-1]
	# 	print name
	# 	shutil.copy(filename, './'+name)
	return users
def FindPhotosByUser(user, file):
	photos = POI_flickr.photos_search(user_id=user)
	ct = 0
	for photo in photos:
		file.write( str(photo.getLocation()) )
		ct = ct+1
		if ct > 20:
			break


def PrintPOI(POI):
	f = open(POI+'.txt','w')
	users=FindPhotosByText(in_text=POI+' tasmania')
	print users
	Users= list(set(users))
	print Users
	for user in Users:
		f.write(user)
		FindPhotosByUser(user, f)
	f.close()

if __name__ =='__main__':
	
	PrintPOI("Bicheno");
	PrintPOI("Coles Bay");


