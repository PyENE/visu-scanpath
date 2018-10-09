# -*- coding: utf-8 -*-
__author__ = 'Brice Olivier'

import os.path
import pandas
import visuscanpath


def plot_mono_annotated_scanpath(dataframe, output_file=None):
    display = True
    if output_file is not None:
        display = False
    visuscanpath.plot_scanpath(dataframe, 's01', 'art_contemporain-f1',
                               os.path.join('images', 'art_contemporain-f1.png'),
                               print_col='WINC', output_file=output_file, display=display)


def plot_pluri_annotated_scanpath(dataframe, output_file=None):
    display = True
    if output_file is not None:
        display = False
    visuscanpath.plot_scanpath(dataframe, 's01', 'art_contemporain-f1',
                               os.path.join('images', 'art_contemporain-f1.png'),
                               print_col=['WINC', 'CINC'],
                               output_file=output_file, display=display)


def main():
    dataframe = pandas.read_csv(os.path.join('data', 'text_reading.csv'))
    plot_mono_annotated_scanpath(dataframe, output_file=os.path.join('scanpaths',
																	 's01-art_contemporain-f1-mono-annotated.png'))
    plot_pluri_annotated_scanpath(dataframe, output_file=os.path.join('scanpaths',
																	  's01-art_contemporain-f1-pluri-annotated.png'))

if __name__ == '__main__':
    main()
