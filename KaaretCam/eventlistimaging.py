import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import pandas as pd
from pathlib import Path

def make_event_fits(csv : str, output_path : str | None = None, energy_range : tuple[int, int] | None = None, overwrite : bool = False, show_hist : bool = False, binning_factor : int = 1, save_fits : bool = True, show_spectrum : str | None=None):
    csv_path = Path(csv)
    supplied_output_path = Path(output_path) if output_path else None

    saveout_path = get_output_path(csv_path=csv_path, supplied_out_path=supplied_output_path, energy_range=energy_range)
    image_data = make_2dhist(csv_path=csv_path, show_hist=show_hist, energy_range=energy_range, binning_factor=binning_factor, show_spectrum=show_spectrum)
    if save_fits:
        saveout_hist(counts=image_data, output_path=saveout_path, overwrite=overwrite)

    

def get_output_path(csv_path : Path, supplied_out_path : Path | None = None, energy_range : tuple[int,int] | None = None):
    if supplied_out_path:
        if not supplied_out_path.exists():
            if not supplied_out_path.suffix:
                supplied_out_path.mkdir()
        if supplied_out_path.is_dir():
            filename = Path(f"{csv_path.stem}{((f"_{energy_range[0]}_to_{energy_range[1]}") if energy_range else "")}").with_suffix(".fits")
            output_path = supplied_out_path / filename
        else:
            output_path = supplied_out_path.with_suffix(".fits")
    else:
        output_path = csv_path.with_name(f"{csv_path.stem}" + ((f"_{energy_range[0]}_to_{energy_range[1]}") if energy_range else "")).with_suffix(".fits")
    return output_path

def make_2dhist(csv_path : Path, show_hist : bool, binning_factor : int, energy_range : tuple[int,int] | None=None, show_spectrum : str | None = None):
    # print(csv_path)
    # print(csv_path.exists())
    eventdata = pd.read_csv(csv_path, header=None, usecols=[0, 1, 2])
    if energy_range:
        energy_range_mask = (eventdata[0] <= energy_range[1]) & (eventdata[0] >= energy_range[0])
    filtered_data = eventdata[energy_range_mask] if energy_range else eventdata
    make_spectrum_fig(show_spectrum=show_spectrum, event_data=eventdata, filtered_data=filtered_data, energy_range=energy_range)
    
    x = filtered_data[1].to_numpy()
    y = filtered_data[2].str.split(':').str[0].astype(int).to_numpy()


    height = 1096
    width = 1936
    dpi = 150
    plt.figure(figsize=(width/dpi, height/dpi), dpi=dpi)
    counts, xedges, yedges, image = plt.hist2d(x, y, bins=(int(1936/binning_factor), int(1096/binning_factor)), range=[[0.5, 1936.5], [0.5, 1096.5]], vmin=0, vmax=1, cmap="gray")
    plt.colorbar(cmap='gray')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title(f"Event Image ({csv_path.name})" + (f"Energies: [{energy_range[0]}, {energy_range[1]}]" if energy_range else "No Energy Filtering"))
    plt.xlabel("X Pos (px)")
    plt.ylabel("Y Pos (px)")
    if show_hist:
        plt.show()
    else:
        plt.close()
    return(counts)

def saveout_hist(counts : np.ndarray, output_path : Path, overwrite):
    #print(np.max(counts))
    fits.writeto(filename=output_path, data=counts.transpose().astype(np.int16), overwrite=overwrite)

def make_spectrum_fig(show_spectrum, event_data : pd.DataFrame, filtered_data : pd.DataFrame, energy_range : tuple[int, int] | None = None):
    if not show_spectrum:
        return
    
    if show_spectrum == "Filtered":
        if energy_range:
            make_filtered_hist(filtered_data=filtered_data, energy_range=energy_range, show=True)
            return

    if show_spectrum == "Full":
        make_full_hist(event_data=event_data, show=True)
        return

    if show_spectrum == "Both":
        if(energy_range):
            plt.figure(figsize=(12, 5))

            plt.subplot(1, 2, 1)
            make_full_hist(event_data=event_data, show=False)

            plt.subplot(1, 2, 2)
            make_filtered_hist(
                filtered_data=filtered_data, energy_range=energy_range, show=False
            )

            plt.tight_layout()
            plt.show()
            return
    print("An invalid option was passed to the show_spectrum argument. Use 'Both', 'Full', or 'Filtered'.")
    return

        

def make_filtered_hist(filtered_data : pd.DataFrame, energy_range : tuple[int, int], show : bool):
    adu = filtered_data[0]
    hist = plt.hist(adu, bins=int((energy_range[1] - energy_range[0])/10))
    plt.xlabel("Energy (ADU)")
    plt.ylabel("Events")
    plt.title(f"Filtered Spectrum: {energy_range[0]}-{energy_range[1]} ADU")
    if show:
        plt.show()
    else:
        return hist

def make_full_hist(event_data : pd.DataFrame, show : bool):
    adu = event_data[0]
    hist = plt.hist(adu, bins=int((max(adu) - min(adu))/10))
    plt.xlabel("Energy (ADU)")
    plt.ylabel("Events")
    plt.title(f"Full Spectrum")
    if show:
        plt.show()
    else:
        return hist
    

        

if __name__ == "__main__":
    make_event_fits("test_imx_data/data/events.csv", "results", overwrite=True, show_hist=True, energy_range=(250, 700), show_spectrum="Full")