#!/bin/bash

/home/pi/allsky/bin/python /home/pi/pyOculus/snapper.py
convert -quality 90% -resize 75% /home/pi/images/latest.png /home/pi/images/latest.jpg
/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync images/*.jpg s3://gomez.me.uk/allsky/
/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync images/*.json s3://gomez.me.uk/allsky/

# Next make a list of all .png files created in the last 24 hours & Make a movie out of them
find /home/pi/images/20*.png -type f -cmin -1440 -exec cat {} \; | ffmpeg -f image2pipe -framerate 10 -i - -s 696x520 -vcodec libx264  -pix_fmt yuv420p latest.mp4 -y
/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync /home/pi/latest.mp4 s3://gomez.me.uk/allsky/
mv /home/pi/latest.mp4 /home/pi/images/latest_$(date +%F).mp4
/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync /home/pi/images/*_.mp4 s3://gomez.me.uk/allsky/archive/
