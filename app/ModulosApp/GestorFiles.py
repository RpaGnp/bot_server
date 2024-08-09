import tempfile
import shutil

def tempdriver(Pathdriver):	
	dirtemp=tempfile.mkdtemp()
	shutil.copy(Pathdriver,dirtemp)
	return dirtemp+"\\chromedriver.exe"



