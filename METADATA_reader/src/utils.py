import SimpleITK as sitk
import numpy as np
import pandas as pd
import os



# #####################################
# Reading files
# #####################################

def ReadFile_info(filepath, verbose=1):
    if verbose == 1:
        print("Reading:", filepath)

        
    header = None
    if '.nii' in filepath: img_type = "nifti"
    elif '.gipl' in filepath: img_type = "gipl"
    elif '.nrrd' in filepath: img_type = "nrrd"

    ref = sitk.ReadImage(filepath)
    ref_size = np.array(ref.GetSize())
    ref_spacing = np.array(ref.GetSpacing())
    ref_origin = np.array(ref.GetOrigin())


    img_info = [ref_size, ref_spacing, ref_origin]
    return img_info,img_type



def GenTxtFile(outdir_path, folderI):

    imgsI = folderI['scan_info']
    patient_nbr = folderI['gipl']+folderI['nifti']+folderI['nrrd']

    file_name = os.path.join(outdir_path,"FolderData.txt")
    f = open(file_name,'w')
    f.write("*********************************************\n")
    f.write("*             Scans information             *\n")
    f.write("*********************************************\n")
    f.write("\n")
    f.write("Folder name : "+ folderI['name'] +"\n")
    f.write("   nifti files : "+ str(folderI['nifti']*2) +"\n")
    f.write("   gipl files : "+ str(folderI['gipl']*2) +"\n")
    f.write("   nrrd files : "+ str(folderI['nrrd']*2) +"\n")
    f.write("   TOTAL files : "+ str(patient_nbr*2) +"\n")
    f.write("   Number of patients : "+ str(patient_nbr) +"\n")
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
