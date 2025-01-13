## REF: https://edg.uchicago.edu/tutorials/pretty_plots_with_gnuplot/
##      https://raymii.org/s/tutorials/GNUplot_tips_for_nice_looking_charts_from_a_CSV_file.html
##      https://stackoverflow.com/questions/327576/how-do-you-plot-bar-charts-in-gnuplot
##
## $ gnuplot ./csv-stats.gnuplot

## Labels
set title 'Kali NetHunter'
set xlabel 'NetHunter Version'

## CSV Input file contains tab-separated fields
set datafile separator '\t'

## Use the first CSV line as title
set key autotitle columnhead 

## PNG image output 
set term png
set output 'csv-stats.gnuplot.png'
## Console ascii image outputs (DEBUG)
#set term dumb

## Rotate x label (xlabel) 90o
set xtics rotate by 90 right

## CSV: Version	Devices	Builds	Kernels	Images	Method
##   2 ~ Device
##   3 ~ Builds
##   4 ~ Kernels
##   5 ~ Images
plot 'csv-stats.csv' using 2:xtic(1) with lines,\
     'csv-stats.csv' using 3:xtic(1) with lines,\
     'csv-stats.csv' using 4:xtic(1) with lines,\
     'csv-stats.csv' using 5:xtic(1) with lines
