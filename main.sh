#!/bin/sh

wdir=/home/fmuser2/scripts/4g_cell_status
cd ${wdir}/
mv ${wdir}/4g_cells_all.csv ${wdir}/old/4g_cells_all_$(date '+DATE: %d_%m_%Y_%H_%M' | sed 's/DATE: //').csv
mv ${wdir}/4g_cells_all.txt  ${wdir}/old/4g_cells_all_$(date '+DATE: %d_%m_%Y_%H_%M' | sed 's/DATE: //').txt

#Make data export from Topology DB
sudo /opt/ericsson/nms_cif_cs/etc/unsupported/bin/cstest -s Seg_masterservice_CS lt EUtranCellFDD -an operationalState administrativeState >  ${wdir}/4g_cells_all.txt

#Parsing txt file to csv file
python ${wdir}/parse.py

#Prepare file for Optima
cp -p ${wdir}/4g_cells_all.csv ${wdir}/out/4g_cells_all_$(date '+DATE: %d_%m_%Y_%H_%M' | sed 's/DATE: //').csv 

#clean old files
find ${wdir}/old -name "*.txt" -mtime +15 -exec rm '{}' \;
find ${wdir}/old -name "*.csv" -mtime +15 -exec rm '{}' \;
find ${wdir}/out -name "*.csv" -mtime +3 -exec rm '{}' \;
