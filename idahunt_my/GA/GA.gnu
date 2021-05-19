#!/usr/bin/gnuplot
set term pngcairo
set size ratio 0.75
set output 'GA.png'
plot "GA.log" using 1:2 title "max" with lines, \
      "GA.log" using 1:3 title "ave" with lines, \
      "GA.log" using 1:4 title "min" with lines
