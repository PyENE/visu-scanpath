# -*- coding: utf-8 -*-
__author__ = 'Brice Olivier'

import os.path
import pandas
import visuscanpath


def plot_annotated_hue_scanpath(output_file=None):
    dataframe = pandas.read_csv(os.path.join('data', 'text_reading.csv'))
    display = True
    if output_file is not None:
        display = False
    visuscanpath.plot_scanpath(dataframe, 's01', 'art_contemporain-f2',
                               os.path.join('images', 'art_contemporain-f2.png'),
                               print_col='WINC', hue='PHASE',
                               output_file=output_file, display=display)


def main():
    plot_annotated_hue_scanpath(output_file=os.path.join('scanpaths',
                                                         's01-art_contemporain-f2-pluri-annotated-hue.png'))

if __name__ == '__main__':
    main()
