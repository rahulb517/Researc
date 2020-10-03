## Crop Monitoring 

Part two of the project was to monitor crops, to detect any signs of crop stress, which would decrease agricultural yields. Here, we used a Raspberry Pi to control 3 USB cameras. The Pi sends a command every at a consistent time interval to the USB cameras to take 3 pictures from different angles. The Rapsberry Pi then stitches the three images into one so that we get a 360 view of the surroundings, and the resulting image is uploaded directly to Dropbox.
