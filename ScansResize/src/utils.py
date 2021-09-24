import os
import itk
import numpy as np
import shutil
import SimpleITK as sitk

from numpy.ma.core import getdata

# #####################################
#  setFile spacing
# #####################################

def SetSpacing(filepath,outpath,output_spacing=[0.5, 0.5, 0.5],output_size = -1):
    
    print("Reading:", filepath)
    img = itk.imread(filepath)

    spacing = np.array(img.GetSpacing())
    output_spacing = np.array(output_spacing)

    # print(spacing)
    # print(output_spacing)

    if not np.array_equal(spacing,output_spacing):

        size = itk.size(img)
        scale = spacing/output_spacing

        if output_size == -1:
            output_size = (np.array(size)*scale).astype(int).tolist()
        output_origin = img.GetOrigin()

        #Find new origin
        output_physical_size = np.array(output_size)*np.array(output_spacing)
        input_physical_size = np.array(size)*spacing
        output_origin = np.array(output_origin) - (output_physical_size - input_physical_size)/2.0

        img_info = itk.template(img)[1]
        pixel_type = img_info[0]
        pixel_dimension = img_info[1]

        VectorImageType = itk.Image[pixel_type, pixel_dimension]

        if True in [seg in os.path.basename(filepath) for seg in ["seg","Seg"]]:
            InterpolatorType = itk.NearestNeighborInterpolateImageFunction[VectorImageType, itk.D]
            # print("Rescale Seg with spacing :", output_spacing)
        else:
            InterpolatorType = itk.LinearInterpolateImageFunction[VectorImageType, itk.D]
            # print("Rescale Scan with spacing :", output_spacing)

        ResampleType = itk.ResampleImageFilter[VectorImageType, VectorImageType]

        resampleImageFilter = ResampleType.New()
        interpolator = InterpolatorType.New()
        resampleImageFilter.SetOutputSpacing(output_spacing)
        resampleImageFilter.SetOutputOrigin(output_origin)
        resampleImageFilter.SetOutputDirection(img.GetDirection())
        
        resampleImageFilter.SetInterpolator(interpolator)
        resampleImageFilter.SetSize(output_size)
        resampleImageFilter.SetInput(img)
        resampleImageFilter.Update()

        resampled_img = resampleImageFilter.GetOutput()

        itk.imwrite(resampled_img, outpath)

    else:
        # print("Already at the wanted spacing")
        itk.imwrite(img, outpath)



def CloseImage(filepath,closing_radius = 1):
    
    if True in [seg in os.path.basename(filepath) for seg in ["seg","Seg"]]:
        
        print("Reading:", filepath)
        # Read the file into an sitkImage
        image = sitk.ReadImage(filepath)
        
        # Threshold the value [0,2), results in values inside the range 1, 0 otherwise)
        
        closed_image = sitk.BinaryMorphologicalClosing(image, [closing_radius] * image.GetDimension())

        writer = sitk.ImageFileWriter()
        writer.SetFileName(os.path.dirname(filepath) + "/C_" + os.path.basename(filepath))
        writer.Execute(closed_image)

def DilateImage(filepath,closing_radius = 1):
    
    if True in [seg in os.path.basename(filepath) for seg in ["seg","Seg"]]:
        
        print("Reading:", filepath)
        # Read the file into an sitkImage
        image = sitk.ReadImage(filepath)
        
        # Threshold the value [0,2), results in values inside the range 1, 0 otherwise)
        
        dilate_image = sitk.BinaryDilate(image, [closing_radius] * image.GetDimension())

        writer = sitk.ImageFileWriter()
        writer.SetFileName(os.path.dirname(filepath) + "/D_" + os.path.basename(filepath))
        writer.Execute(dilate_image)


