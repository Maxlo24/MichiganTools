# from medpy.io import header
from utils import *

import argparse
import glob
import sys

# import medpy.io

def main(args):

    scan_lst = []
    seg_lst =[]

    outpath = args.out
    
    data_lst = []
    imgs_infos = []
    folder_info = {
        'name': 'input_folder',
        'nifti': 0,
        'gipl': 0,
        'nrrd': 0,
        'scan_info' : [],
        'dimx' : {},
        'dimy' : {},
        'dimz' : {},
        'spx' : {},
        'spy' : {},
        'spz' : {},
    }

    if not os.path.exists(outpath):
        os.makedirs(outpath)
    
    if args.image:
        img_obj = {}
        img_obj["img"] = args.image
        data_lst.append(img_obj)
        folder_info['name'] = args.image
        
    elif args.dir:
        folder_info['name'] = args.dir
        normpath = os.path.normpath("/".join([args.dir, '**', '']))
        for img_fn in sorted(glob.iglob(normpath, recursive=True)):
            if os.path.isfile(img_fn) and True in [ext in img_fn for ext in [".nrrd", ".nrrd.gz", ".nii", ".nii.gz", ".gipl", ".gipl.gz"]]:
                if True in [seg in img_fn for seg in ["Seg","seg"]]:
                    seg_lst.append(img_fn)
                else:
                    scan_lst.append(img_fn)
                # img_obj = {}
                # img_obj["img"] = img_fn
                # img_obj["out"] = os.path.normpath("/".join([args.out]))  # Is it better to do  "out_path = os.path.normpath("/".join([args.out]))" only once at the start
                # img_fn_array.append(img_obj)
    
    if len(scan_lst) != len(seg_lst):

        print("ERROR : folder dont have the same number of scans and seg", file=sys.stderr)
        print("Lead : make sure all the segmentation files have 'seg' or 'Seg' in their name")
        print('       Scan number : ',len(scan_lst))
        print('       Seg number : ',len(seg_lst))
        
        raise 

    for i,scan in enumerate(scan_lst):
        data = {}
        data["scan"] = scan
        data["seg"] = seg_lst[i]
        data_lst.append(data)

    nbr_of_patient = len(data_lst)

    print(nbr_of_patient, " patient in folder")

    for patient in data_lst:

        image = patient["scan"]
        
        img_info, img_type = ReadFile_info(image)
        img_data = {'Path': image,'Dim':img_info[0],'Scale':img_info[1],'Origin':img_info[2],'Type':img_type}
        
        folder_info['dimx'][img_info[0][0]] = folder_info['dimx'].get(img_info[0][0],0) + 1
        folder_info['dimy'][img_info[0][1]] = folder_info['dimy'].get(img_info[0][1],0) + 1
        folder_info['dimz'][img_info[0][2]] = folder_info['dimz'].get(img_info[0][2],0) + 1
        folder_info['spx'][img_info[1][0]] = folder_info['spx'].get(img_info[1][0],0) + 1
        folder_info['spy'][img_info[1][1]] = folder_info['spy'].get(img_info[1][1],0) + 1
        folder_info['spz'][img_info[1][2]] = folder_info['spz'].get(img_info[1][2],0) + 1

        imgs_infos.append(img_data)

        folder_info[img_type]+=1

        ReadFile_info(patient["seg"])

        # print(img_data[1])

    # print(imgs_infos)

    folder_info['scan_info'] = imgs_infos
    GenTxtFile(args.out,folder_info)

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