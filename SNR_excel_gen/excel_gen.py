import argparse
import glob
import subprocess
import os
import pandas as pd

def main(args):

    before_d = os.path.normpath("/".join([args.before_d]))
    after_d = os.path.normpath("/".join([args.after_d]))

    data = []
    snr_graph = []
    snr_file = []

    data.append(["Before file","After file","Signa average","Noise average","Noise standard deviation","SNR"])
    b_normpath = os.path.normpath("/".join([before_d, '*', '']))
    for b_f in glob.iglob(b_normpath, recursive=True):
        # data.append(f)
        a_dir = os.path.join(after_d,os.path.basename(b_f.replace('.nrrd','')))
        # print(a_dir)
        a_normpath = os.path.normpath("/".join([a_dir, '*', '']))
        for a_f in glob.iglob(a_normpath, recursive=True):
            Saverage,Naverage,NStDev,Snr = getValues(b_f,a_f)
            # print(Saverage,Naverage,NStDev,Snr)
            snr_graph.append(Snr)
            snr_file.append(os.path.basename(a_f))
            data.append([os.path.basename(b_f),os.path.basename(a_f),Saverage,Naverage,NStDev,Snr])

        print(b_f)
    
    doc = pd.DataFrame(data)
    graph = pd.DataFrame(
    {   'A': snr_file,
        'B': snr_graph}
    )

    max_row = len(graph)
    col_x = graph.columns.get_loc('A') + 1
    col_y = graph.columns.get_loc('B') + 1

    file_name = os.path.join("SNR_Data.xlsx")

    writer = pd.ExcelWriter(file_name)

    doc.to_excel(writer, sheet_name = 'data')
    graph.to_excel(writer, sheet_name = 'graph')

    workbook = writer.book
    worksheet = writer.sheets['graph']
    chart = workbook.add_chart({'type': 'column'})

    # Create the scatter plot, use a trendline to fit it
    chart.add_series({
        'categories': ['graph', 1, col_x, max_row, col_x],
        'values':     ['graph', 1, col_y, max_row, col_y],
    })

    worksheet.insert_chart('E2', chart)



    writer.save()

    # Saverage,Naverage,NStDev,Snr = getValues(b,a)
    # print(data)

def getValues(before_f,after_f):
    out = subprocess.Popen(['./build_ImageNoise/bin/ImageNoise', before_f,'-s',after_f,'-i', before_f], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    # print(stdout)
    
    stdout = str(stdout)
    stdout = stdout[2:-3]
    stdout = stdout.replace(' ','')
    result = stdout.split(':')
    result = result[1:5]

    Saverage = float(result[0][0:-14])
    Naverage = float(result[1][0:-24])
    NStDev = float(result[2][0:-5])
    Snr = float(result[3])
    return Saverage,Naverage,NStDev,Snr

if __name__ ==  '__main__':
	parser = argparse.ArgumentParser(description='MD_reader', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('-b','--before_d', type=str, help='before dir')
	parser.add_argument('-a','--after_d', type=str, help='after dir', required=True)

	args = parser.parse_args()

	main(args)