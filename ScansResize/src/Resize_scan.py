from utils import *

import argparse
import glob

def main(args):

	img_fn_array = []
	outpath = os.path.normpath("/".join([args.out]))

	if args.image:
		img_obj = {}
		img_obj["img"] = args.image
		img_obj["out"] = outpath
		img_fn_array.append(img_obj)
		
		
	if args.dir:
		normpath = os.path.normpath("/".join([args.dir, '**', '']))
		for img_fn in glob.iglob(normpath, recursive=True):
			if os.path.isfile(img_fn) and True in [ext in img_fn for ext in [".nrrd", ".nrrd.gz", ".nii", ".nii.gz", ".gipl", ".gipl.gz"]]:
				img_obj = {}
				img_obj["img"] = img_fn
				img_obj["out"] = outpath  # Is it better to do  "out_path = os.path.normpath("/".join([args.out]))" only once at the start
				img_fn_array.append(img_obj)
				
	for img_obj in img_fn_array:
		image = img_obj["img"]
		out = img_obj["out"]
		
		if not os.path.exists(out):
			os.makedirs(out)
		SetSpacing(image, out, args.spacing)

		

if __name__ ==  '__main__':
	parser = argparse.ArgumentParser(description='MD_reader', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	input_group = parser.add_argument_group('Input files')
	input_params = input_group.add_mutually_exclusive_group(required=True)
	input_params.add_argument('--image', type=str, help='Input 3D image')
	input_params.add_argument('--dir', type=str, help='Input directory with 3D images')

	input_group.add_argument('-s','--spacing', type=float, help='Wanted output x spacing', default=0.5)

	output_params = parser.add_argument_group('Output parameters')
	output_params.add_argument('--out', type=str, help='Output directory', required=True)

	args = parser.parse_args()

	main(args)

