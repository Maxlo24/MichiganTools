import os
import itk

# #####################################
#  setFile spacing
# #####################################

def SetSpacing(filepath,outpath,spacing=0.5):
    print("Reading : " + filepath)
    input_image = itk.imread(filepath)

    input_size = itk.size(input_image)
    input_spacing = itk.spacing(input_image)
    input_origin = itk.origin(input_image)
    Dimension = input_image.GetImageDimension()
    scale = input_spacing[0]/spacing

    output_size = [int(input_size[d] * scale) for d in range(Dimension)]
    output_spacing = [input_spacing[d] / scale for d in range(Dimension)]
    output_origin = [input_origin[d] + 0.5 * (output_spacing[d] - input_spacing[d]) for d in range(Dimension)]

    interpolator = itk.LinearInterpolateImageFunction.New(input_image)

    resampled = itk.resample_image_filter(
        input_image,
        interpolator=interpolator,
        size=output_size,
        output_spacing=output_spacing,
        output_origin=output_origin,
    )

    itk.imwrite(resampled, os.path.join(outpath,os.path.basename(filepath)))