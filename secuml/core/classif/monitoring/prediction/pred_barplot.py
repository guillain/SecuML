# SecuML
# Copyright (C) 2016-2018  ANSSI
#
# SecuML is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# SecuML is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with SecuML. If not, see <http://www.gnu.org/licenses/>.

import os.path as path

from secuml.core.data import labels_tools
from secuml.core.data.labels_tools import BENIGN, MALICIOUS
from secuml.core.tools.plots.barplot import BarPlot
from secuml.core.tools.plots.dataset import PlotDataset
from secuml.core.tools.color import get_label_color


class PredictionsBarplots(object):

    def __init__(self, has_ground_truth):
        self.ranges = [[] for i in range(10)]
        self.has_ground_truth = has_ground_truth

    def add_fold(self, predictions):
        for i, instance_id in enumerate(predictions.ids.ids):
            proba = predictions.probas[i]
            label = predictions.ground_truth[i]
            # Prb if proba = 1
            if proba == 1:
                proba = 0.999999
            self.ranges[int(proba * 10)].append({'instance_id': instance_id,
                                                 'ground_truth_label': label})

    def display_label(self, barplot, label):
        label_bool = labels_tools.label_str_to_bool(label)
        ranges = [[x for x in l if x['ground_truth_label'] == label_bool]
                  for l in self.ranges]
        dataset = PlotDataset(list(map(len, ranges)), label)
        dataset.set_color(get_label_color(label))
        barplot.add_dataset(dataset)

    def display(self, directory):
        labels = ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%',
                  '50-60%', '60-70%', '70-80%', '80-90%', '90-100%']
        barplot = BarPlot(labels)
        if not self.has_ground_truth:
            dataset = PlotDataset(list(map(len, self.ranges)), 'num_instances')
            dataset.set_color(get_label_color('all'))
            barplot.add_dataset(dataset)
        else:
            self.display_label(barplot, MALICIOUS)
            self.display_label(barplot, BENIGN)
        barplot.export_to_json(path.join(directory, 'predictions_barplot.json'))
