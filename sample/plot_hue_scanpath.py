# -*- coding: utf-8 -*-
__author__ = 'Brice Olivier'

import os.path
import pandas
import visuscanpath


def plot_raw_scanpath(output_file=None):
    dataframe = pandas.read_csv(os.path.join('..', 'data', 'text_reading.csv'))
    display = True
    if output_file is not None:
        display = False
    visuscanpath.plot_scanpath(dataframe, 's01', 'art_contemporain-f1',
                               os.path.join('..', 'images', 'art_contemporain-f1.png'),
                               hue='WORD_INCREMENT', output_file=output_file, display=display)


def main():
    plot_raw_scanpath(output_file='scanpaths/s01-art_contemporain-f1-hue.png')

if __name__ == '__main__':
    main()
