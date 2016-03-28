#!/bin/sh

python /home/pi/pyOculus/snapper.py >/home/pi/allsky.log
convert -quality 90% -resize 75% /home/pi/images/latest.png /home/pi/images/latest.jpg
/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync images/*.jpg s3://www.zemogle.uk/allsky/
/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync images/*.json s3://www.zemogle.uk/allsky/

# Next make a list of all .png files created in the last 12 hours
#find . -type f -name '*.png' -cmin -720
