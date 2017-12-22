# -*- coding: utf-8 -*-
__author__ = 'Brice Olivier'

import numpy as np
import sys
from visuscanpath import config
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def plot_scanpath(dataframe, subj, text, img_path, hue=None, print_col=None,
                  output_file=None, display=True, legend=True):
    """Display a scanpath.

    Args:
        dataframe (pandas.DataFrame): Mandatory columns: ['X', 'Y', 'FIXATION_DURATION', 'SUBJ', 'TEXT'].
        subj (str): Variable in dataframe corresponding to the subject id.
        text (str): Variable in dataframe corresponding to the text id.
        img_path (str): Path to png image.
        hue (str): Variable in dataframe to map fixations to different colors.
        print_col (str or list(str)): Variable[s] in dataframe to display bellow each fixation.
        output_file (str): If given then img is saved at the specified location.
        display (boolean): Display img or not.
        legend (boolean): Anchor scanpath meta data as legend.

    Returns:
        PIL.Image: The scanpath image.

    Examples:
        >>> plot_scanpath(dataframe, 's01', 'art_contemporain-f1', '../images/art_contemporain-f1.png')
        >>> plot_scanpath(dataframe, 's01', 'art_contemporain-f1', \
                          '../images/art_contemporain-f1.png', print_col='READMODE')
        >>> plot_scanpath(dataframe, 's01', 'art_contemporain-f1', \
                          '../images/art_contemporain-f1.png', print_col=['WINC', 'CINC'])
        >>> plot_scanpath(dataframe, 's01', 'art_contemporain-f1', \
                          '../images/art_contemporain-f1.png', hue='READMODE')
        >>> plot_scanpath(dataframe, 's01', 'art_contemporain-f1', \
                          '../images/art_contemporain-f1.png', output_file='plot_scanpath.png', display=False)
    """
    if config.X_COL not in dataframe.columns:
        raise ValueError('VisuScanpath: failed to identify column containing X values.')
    if config.Y_COL not in dataframe.columns:
        raise ValueError('VisuScanpath: failed to identify column containing Y values.')
    if config.FIXATION_DURATION_COL not in dataframe.columns:
        raise ValueError('VisuScanpath: failed to identify column containing FIXATION_DURATION values.')
    if (type(subj) != str) or not dataframe[config.SUBJ_COL].isin([subj]).any():
        raise ValueError('VisuScanpath: failed to identify subj ' + str(subj))

    if (type(text) != str) or not dataframe[config.TEXT_COL].isin([text]).any():
        raise ValueError('VisuScanpath: failed to identify text ' + str(text))

    if (hue is not None) and (hue not in dataframe.columns):
        raise ValueError('VisuScanpath: failed to identify hue variable ' + str(hue))

    if print_col is not None:
        print_col_error = True
        if type(print_col) == str:
            if print_col in dataframe.columns:
                print_col_error = False
        if type(print_col) == list:
            if all([type(type_str) for type_str in print_col]):
                if set(print_col).issubset(dataframe.columns):
                    print_col_error = False
        if print_col_error:
            raise ValueError('VisuScanpath: failed to identify print_col variable ' + str(print_col))

    if hue is not None:
        n_colors = len(dataframe[hue].unique())
        hues = np.linspace(0, 1, n_colors)[:-1]
        hues *= 360
        hues = hues.astype(int)
        color_list = ["hsl(" + str(h_i) + ", " + str(config.COLOR_SATURATION)
                      + "%, " + str(config.COLOR_LIGHTNESS) + "%)" for h_i in hues]
        color_map = dict(zip(dataframe[hue].unique(), color_list))

    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", config.FONT_SIZE)
    except EnvironmentError:
        print('TrueType font arial.ttf could not be loaded. Default will be used instead.', sys.stderr)
        font = ImageFont.load_default().font

    if legend:
        legend_label = str(subj) + ' - ' + str(text)
        if print_col is not None:
            legend_label += ' - ' + str(print_col)
        if hue is not None:
            legend_label += ' - ' + str(hue)
        draw.text((0, 0), legend_label, 'black', font=font)

    first_fixation_index = dataframe[(dataframe['SUBJ'] == subj) & (dataframe['TEXT'] == text)].index[0]

    for fixation_index in dataframe[(dataframe['SUBJ'] == subj) & (dataframe['TEXT'] == text)].index:
        current_x = int(dataframe.at[fixation_index, 'X'])
        current_y = int(dataframe.at[fixation_index, 'Y'])
        fixation_duration = dataframe.at[fixation_index, 'FIXATION_DURATION']
        radius = int(config.RADIUS_SCALE * fixation_duration)
        color = 'black'
        if hue is not None:
            current_hue = int(dataframe.at[fixation_index, hue])
            color = color_map[current_hue]
        draw.ellipse([current_x - radius, current_y - radius, current_x + radius, current_y + radius],
                     outline=color)
        if type(print_col) == str:
            draw.text((current_x, current_y), str(dataframe.at[fixation_index, print_col]), 'black', font=font)
        elif type(print_col) == list:
            shift = 0
            for value in print_col:
                draw.text((current_x, current_y + shift), str(dataframe.at[fixation_index, value]), 'black', font=font)
                shift += config.FONT_SIZE
        if fixation_index != first_fixation_index:
            draw.line([previous_x, previous_y, current_x, current_y], fill=color, width=config.LINE_WIDTH)
        previous_x = current_x
        previous_y = current_y

    if output_file is not None:
        img.save(output_file)
    if display:
        img.show()

    return img
