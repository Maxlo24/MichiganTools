import medpy.io
import nibabel as nib
import nrrd
import os

import numpy as np
import pandas as pd



# #####################################
# Reading files
# #####################################

def ReadFile_info(filepath, verbose=1):
    if verbose == 1:
        print("Reading:", filepath)

        
    header = None
    if '.nii' in filepath: img_info = Read_nifti_header(filepath)
    elif '.gipl' in filepath: img_info = Read_gipl_header(filepath)
    elif '.nrrd' in filepath: img_info = Read_nrrd_header(filepath)
    return img_info

def Read_nifti_header(filepath):
    img = nib.load(filepath)
    header = img.header
    img_dim = header['dim'][1:4][:]
    img_pixdim = header['pixdim'][1:4][:]
    img_origin = [header['qoffset_x'],header['qoffset_y'],header['qoffset_z']]
    img_info = np.array([img_dim, img_pixdim, img_origin])
    # img_info = np.around(img_info, decimals=2)
    # print(img_info.dtype)
    return img_info,"nifti"

def Read_gipl_header(filepath):
    img, header = medpy.io.load(filepath)
    img = np.array(img)
    # print(img.shape)
    img_dim = img.shape
    img_pixdim = medpy.io.Header.get_voxel_spacing(header)
    img_origin = medpy.io.Header.get_offset(header)
    # img = medpy.io.set_pixel_spacing(header,(0.5,0.5,0.5))
    img_info = np.array([img_dim, img_pixdim, img_origin])
    # img_info = np.around(img_info, decimals=2)
    # print(img_info.dtype)
    return img_info,"gipl"

def Read_nrrd_header(filepath):
    img, header = nrrd.read(filepath)
    # print(header)
    # return img_info,"nrrd"

def GenTxtFile(outdir_path, folderI):

    imgsI = folderI['scan_info']
    file_name = os.path.join(outdir_path,"FolderData.txt")
    f = open(file_name,'w')
    f.write("*********************************************\n")
    f.write("*             Scans information             *\n")
    f.write("*********************************************\n")
    f.write("\n")
    f.write("Folder name : "+ folderI['name'] +"\n")
    f.write("   nifti files : "+ str(folderI['nifti']) +"\n")
    f.write("   gipl files : "+ str(folderI['gipl']) +"\n")
    f.write("   nrrd files : "+ str(folderI['nrrd']) +"\n")
    f.write("   TOTAL files : "+ str(folderI['gipl']+folderI['nifti']+folderI['nrrd']) +"\n")
    # f.write( data + "\n")
    f.close


    file_name = os.path.join(outdir_path,"Data.xlsx")

    #Converting array to dataframe
    all_imgs_info = pd.DataFrame(imgsI)
    dimx = pd.DataFrame(np.transpose(np.array([list(folderI['dimx'].keys()),list(folderI['dimx'].values())])))
    dimy = pd.DataFrame(np.transpose(np.array([list(folderI['dimy'].keys()),list(folderI['dimy'].values())])))
    dimz = pd.DataFrame(np.transpose(np.array([list(folderI['dimz'].keys()),list(folderI['dimz'].values())])))
    spx = pd.DataFrame(np.transpose(np.array([list(folderI['spx'].keys()),list(folderI['spx'].values())])))
    spy = pd.DataFrame(np.transpose(np.array([list(folderI['spy'].keys()),list(folderI['spy'].values())])))
    spz = pd.DataFrame(np.transpose(np.array([list(folderI['spz'].keys()),list(folderI['spz'].values())])))


    writer2 = pd.ExcelWriter(file_name)

    all_imgs_info.to_excel(writer2, sheet_name = 'all_imgs_info',index = False)
    dimx.to_excel(writer2, sheet_name = 'dimx', index = False)
    dimy.to_excel(writer2, sheet_name = 'dimy', index = False)
    dimz.to_excel(writer2, sheet_name = 'dimz', index = False)
    spx.to_excel(writer2, sheet_name = 'spx', index = False)
    spy.to_excel(writer2, sheet_name = 'spy', index = False)
    spz.to_excel(writer2, sheet_name = 'spz', index = False)

    writer2.save()


    return
