import itk
import numpy as np
import os
import argparse
import glob
import pandas as pd

from numpy.lib.function_base import average

def getRange(filepath):
    input_image = itk.imread(filepath)
    array_img = np.array(itk.GetArrayViewFromImage(input_image))
    # print(array_img)

    min = np.min(array_img)
    max = np.max(array_img)
    
    return min,max



def main(args):
    
    img_fn_array = []
    total_range = 0
    total_min = 0
    total_max = 0
    outpath = os.path.normpath("/".join([args.out]))

    folder_info = {
        'file': []
    }
    
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

    number_of_files = len(img_fn_array)
                
    folder_info["file"].append(["image","min","max","range"])

    for img_obj in img_fn_array:
        image = img_obj["img"]
        out = img_obj["out"]
        
        if not os.path.exists(out):
            os.makedirs(out)
        min,max = getRange(image)
        range = max - min
        total_range += range
        total_min += min
        total_max += max
        folder_info["file"].append([image,min,max,range])
        
    average_range = total_range/number_of_files
    average_min = total_min/number_of_files
    average_max = total_max/number_of_files

    folder_info["file"].append(["Average",average_min,average_max,average_range])


    print(average_range)
    print(average_min)
    print(average_max)

    doc = pd.DataFrame(folder_info["file"])

    file_name = os.path.join(outpath,"Data.xlsx")

    writer = pd.ExcelWriter(file_name)

    doc.to_excel(writer)

    writer.save()



        
if __name__ ==  '__main__':
	parser = argparse.ArgumentParser(description='MD_reader', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	input_group = parser.add_argument_group('Input files')
	input_params = input_group.add_mutually_exclusive_group(required=True)
	input_params.add_argument('--image', type=str, help='Input 3D image')
	input_params.add_argument('--dir', type=str, help='Input directory with 3D images')

	output_params = parser.add_argument_group('Output parameters')
	output_params.add_argument('--out', type=str, help='Output directory', required=True)

	args = parser.parse_args()

	main(args)

