#!/bin/sh

python /home/pi/pyOculus/snapper.py >/home/pi/allsky.log
convert -quality 90% -resize 75% /home/pi/images/latest.png /home/pi/images/latest.jpg
/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync images/*.jpg s3://www.zemogle.uk/allsky/
/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync images/*.json s3://www.zemogle.uk/allsky/

# Next make a list of all .png files created in the last 12 hours
find 20*.png -type f -cmin -720 -printf "file '%f'\n" > /home/pi/images/image_files.txt

# Make a movie out of them
ffmpeg -f concat -i /home/pi/images/image_files.txt  -pix_fmt yuv420p -vcodec h264 /home/pi/images/latest.mov -y
/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync images/*.mov s3://www.zemogle.uk/allsky/
mv /home/pi/images/latest.mov /home/pi/images/latest_$(date +%F).mov
