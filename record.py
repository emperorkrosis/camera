import urllib2
import base64
import time
from PIL import Image
from PIL import ImageChops
from StringIO import StringIO
import math
import operator
import sys
import os


# Global variables for keeping track of the previous image captured by the
# camera.
prevImage = None
prevName = None
# Hardcoded camera url (D-Link DCS-932L).
camera_url = 'http://192.168.1.55/image.jpg'


def printUsage():
  """Print usage for the scruipt."""
  print 'Usage: record.py [username] password'


def getImageData(usr, pwd):
  """Request image from security camera using HTTP gateway.
  Parameters:
    usr - username for authentication with the camera.
    pwd - password for authentication with the camera.
  Return:
    image response from the camera as a JPG image.
  """
  global camera_url
  request = urllib2.Request(camera_url)
  base64string = base64.encodestring('%s:%s' % (usr, pwd)).replace('\n', '')
  request.add_header("Authorization", "Basic %s" % base64string)   
  result = urllib2.urlopen(request)
  data = result.read()
  return data


def snapshot(usr, pwd):
  """Detect a diff in the most recent camera images and save.
  Parameters:
    usr - username for authentication with the camera.
    pwd - password for authentication with the camera.
  """
  global prevImage
  global prevName
  # Get the new image.
  data = getImageData(usr, pwd)
  epoch_time = long(time.time() * 1000)
  filename = 'img' + str(epoch_time) + '.jpg'
  # Compare images and save if the diff is greater than the threshold.
  if prevImage is not None:
    i1 = Image.open(StringIO(prevImage))
    i2 = Image.open(StringIO(data))
    rms = rmsdiff_2011(i1, i2)
    print rms
    if rms > 15:
      saveFile(filename, data)
  # Save the previous image for the next comparison.
  prevImage = data
  prevName = filename


def saveFile(name, data):
  """Save the given image with the given name to a file.
  Parameters:
    name - the filename to save.
    data - the image data to save.
  """
  print 'Saving ' + name + ' ... (' + str(len(data)) + ')'
  with open('./data/' + name, 'w') as f:
    f.write(data)


def rmsdiff_2011(im1, im2):
    """Calculate the root-mean-square difference between two images.
    Parameters:
      im1 - the first PIL Image to compare.
      im2 - the second PIL Image to compare.
    Return:
      the root mean square difference between the two images.
    """
    diff = ImageChops.difference(im1, im2)
    h = diff.histogram()
    r = h[0:256]
    g = h[256:512]
    b = h[512:768]
    sq_r = (value*(idx**2) for idx, value in enumerate(r))
    sq_g = (value*(idx**2) for idx, value in enumerate(g))
    sq_b = (value*(idx**2) for idx, value in enumerate(b))
    sum_of_squares = sum(sq_r) + sum(sq_g) + sum(sq_b)
    rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
    return rms


def run(usr, pwd):
  """Repeatedly check images, runs indefinitely."""
  while(1):
    snapshot(usr, pwd)
    time.sleep(1)


# Bootstrap code that parses the username and password from the command line
# and starts running.
if len(sys.argv) == 3:
  run(sys.argv[1], sys.argv[2])
elif len(sys.argv) == 2:
  password = sys.argv[1]
  run(os.environ['USER'], sys.argv[1])
else:
  printUsage()
