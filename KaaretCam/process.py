import numpy as np
from pathlib import Path
import argparse
from tiff2fits.tiff2fits import convert_dir
import CU
from eventlistimaging import make_event_fits


def get_image_paths(data_path : str, dark_path : str):
    datap = Path(data_path)
    darkp = Path(dark_path)
    if not datap.is_dir() or not darkp.is_dir():
        raise NotADirectoryError("You must pass paths to your data and dark directories, which must exist.")

    

    datap_tiff = Path(datap/"tiff")
    datap_fits = Path(datap/"fits")
    darkp_tiff = Path(darkp/"tiff")
    darkp_fits = Path(darkp/"fits")

    for dir in [datap_fits, darkp_fits]:
        dir.mkdir(exist_ok=True)
    print("Fits directories created or already existed. Moving on...")
    

        

    return datap_tiff, datap_fits, darkp_tiff, darkp_fits

def convert_all_files(datap_tiff : Path, datap_fits : Path, darkp_tiff : Path, darkp_fits : Path):
    if not any(darkp_fits.iterdir()): #If darkp_fits is empty:
        print("Converting darks to fits...")
        convert_dir(darkp_tiff, darkp_fits)
    print("Darks converted.")
    if not any(datap_fits.iterdir()): #If datap_fits is empty:
        convert_dir(datap_tiff, datap_fits)
        print("Converting data to fits...")
    print("Data converted.")

    

def get_darks_csv(darkp : Path, darkp_tiff : Path, darkp_fits : Path):
    darks_csv = next(darkp_fits.glob("*.csv"), None)

    if not darks_csv:
        print("Creating dark pixel csv and average dark...")
        CU.getBadPix(str(darkp_fits / "dark_"))
    else:
        print("Dark frames already processed. Moving on.")

    darks_csv = next(darkp_fits.glob("*.csv"), None)
    return(darks_csv)

def count_events(datap_fits, darkp_fits, datap, thresp, thres, hthr, hrep):
    savep = Path(datap/"events")
    csv_path = next(datap.glob("*.csv"), None)

    if not csv_path:
        print("Counting events...")
        CU.fileAnalysis(filePath = str(Path(datap_fits/"image_")), darkPath=str(Path(darkp_fits/"dark_")), savePath=str(savep), thres=thres, thresp=thresp, hrep=hrep)
    else:
        print("Events have already been counted for these data. Moving on.")
    return csv_path






    


def __get_args__():
    parser = argparse.ArgumentParser(
    prog='KaaretCam Data Processor',
    description='Processes KaaretCam  event data into fits images for given energy ranges.'

    )
    parser.add_argument('data_path', help="Path to data folder (should contain individual tiff and fits directories.)")
    parser.add_argument('dark_path', help="Path to darks folder (should contain individual tiff and fits directories.)")
    parser.add_argument('energy_min', )
    parser.add_argument('energy_max')
    parser.add_argument('output_path')

    args = parser.parse_args()
    return args

def main():
    #Structure of data folder:
    #Darks
    #--tiff
    #--fits
    #Data
    #--tiff
    #--fits
    
    hthr_value=20
    args = __get_args__()
    datap = Path(args.data_path)
    darkp = args.dark_path
    datap_tiff, datap_fits, darkp_tiff, darkp_fits = get_image_paths(data_path=str(datap), dark_path=darkp)
    convert_all_files(datap_fits=datap_fits, darkp_fits=darkp_fits, datap_tiff=datap_tiff, darkp_tiff=darkp_tiff)
    darks_csv = get_darks_csv(darkp=darkp, darkp_tiff=darkp_tiff, darkp_fits=darkp_fits)
    events_csv = count_events(datap_fits=datap_fits, darkp_fits=darkp_fits, datap=datap, hthr=hthr_value, thres=26, thresp=9, hrep=6)
    make_event_fits(str(events_csv), energy_range=(int(args.energy_min), int(args.energy_max)), output_path=args.output_path)
    return



if __name__ == "__main__":
    main()


