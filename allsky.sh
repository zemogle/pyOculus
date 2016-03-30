#!/bin/sh

python /home/pi/pyOculus/snapper.py >/home/pi/allsky.log
convert -quality 90% -resize 75% /home/pi/images/latest.png /home/pi/images/latest.jpg
/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync images/*.jpg s3://www.zemogle.uk/allsky/
/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync images/*.json s3://www.zemogle.uk/allsky/

# Next make a list of all .png files created in the last 12 hours & Make a movie out of them
find /home/pi/images/20*.png -type f -cmin -720 -exec cat {} \; | ffmpeg -f image2pipe -r 1  -i - -vcodec libx264 latest.mov -y

/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync /home/pi/images/latest.mov s3://www.zemogle.uk/allsky/
mv /home/pi/images/latest.mov /home/pi/images/latest_$(date +%F).mov
