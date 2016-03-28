#!/bin/sh

python /home/pi/pyOculus/snapper.py >/home/pi/allsky.log
convert -quality 90% -resize 75% images/latest.png images/latest.jpg
/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync images/*.jpg s3://www.zemogle.uk/allsky/
/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync images/*.json s3://www.zemogle.uk/allsky/

# Next make a list of all .png files created in the last 12 hours
#find . -type f -name '*.png' -cmin -720

# Make a movie out of them
#ffmpeg -f image2 -pattern_type glob -i '*.png' -pix_fmt yuv420p -vcodec h264 latest_allsky.mpv
