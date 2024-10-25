Scripts to generate a Steinbichler / Zeiss comet 3D-Scanner calibration plate and calibration file

CP_P_100.py generates the plates pattern. It has to be printed onto something temperature stable and then photogrammetricly checked
  → use point diameters 1,2 mm and 2,2 mm for CP_P_100 plates
  → I'm still lacking a real CP_P_300 plate to get accurate point diameters from...

GOM_2_Steinbichler_LST.py reads a gom *.refxml file and then writes the reference points as a steinbichler *.lst file
The plate and *.lst-file can then be used to calibrate the scanner.
  → Point orientation must be done in the photogrammetry software. The script expects the points with the right coordinates
  → The script filters out coded reference points and outliers. You maybe have to adjust some parameters.

I've had success calibrating my scanner with a CP_P_100 which has been checked with a GOM Tritop photogrammetry system.
The uploaded *.png and *.svg are just examples generated with old parameters - do not directly use them to build a plate.

If you own a Zeiss, Steinbichler, Aicon / Hexagon, Linearis3d or similar Photogrammetry system, please get in touch :)
