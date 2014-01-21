import os, time
from subprocess import Popen, PIPE
import re


path_to_watch = "../../../Desktop/TestWatchFolder"

before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while 1:
  time.sleep (3)
  after = dict ([(f, None) for f in os.listdir (path_to_watch)])
  added = [f for f in after if not f in before]
  removed = [f for f in before if not f in after]
  if added: 
	currentpathandfile = path_to_watch + "/" + str(added[-1])
	tempvar = True
	while tempvar:
		try:
			os.rename(currentpathandfile,currentpathandfile)
			print "renamed"
			tempvar = False
		except WindowsError:
			time.sleep (5)
	print "Added: ", ", ".join (added)
	
	abspathname = os.path.abspath(currentpathandfile)
	
	abspathnameLessEXT = abspathname[:-4]
	abspathnameLessEXT = abspathnameLessEXT.split('\\')
	filenameLestEXT = abspathnameLessEXT[-1]
	abspathnameLessFilenameEXT = abspathnameLessEXT.pop(-1)
	uponedir = abspathnameLessEXT.pop(-1)
	
	abspathWatchFolder = '\\'.join(abspathnameLessEXT)
	destpath = abspathWatchFolder + '\\' + filenameLestEXT + '_xdcam_mxf' + '\\' + filenameLestEXT
	os.system("mkdir " + '"' + abspathWatchFolder + '"' + '\\' + '"' + filenameLestEXT + '"' + "_xdcam_mxf")
	
	runRender = "ffmpeg -i " + '"' + str(abspathname) + '"' + " -pix_fmt yuv422p -vcodec mpeg2video -non_linear_quant 1 -flags +ildct+ilme -top 1 -dc 10 -intra_vlc 1 -qmax 3 -lmin " + '"1*QP2LAMBDA"' + " -vtag xd5c -rc_max_vbv_use 1 -rc_min_vbv_use 1 -g 12 -b:v 50000k -minrate 50000k -maxrate 50000k -bufsize 8000k -acodec pcm_s16le -ar 48000 -bf 2 -ac 2 " + '"' + str(destpath) + '"' + ".mxf"
	dogs = Popen(runRender)
	dogs.wait()
	
  if removed: print "Removed: ", ", ".join (removed)
	
  before = after