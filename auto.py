import subprocess
import os

os.chdir('../openpose')
openpose_bin = './build/examples/openpose/openpose.bin'
input_dir = "../openpose-web/input"
output_dir = "../openpose-web/output"


def process():
	output = subprocess.check_output([openpose_bin, "--image_dir", input_dir, "--write_images", output_dir, "--write_keypoint_json", output_dir, "--no_display"])
	print output

import time
while 1:
	files = os.listdir(input_dir)
	if len(files) > 0:
		process()
	time.sleep(1.0)


