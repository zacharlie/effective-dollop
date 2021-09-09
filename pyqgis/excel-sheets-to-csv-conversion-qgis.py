# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterFolderDestination)
from qgis import processing
import xlrd
import csv

class ExcelSheetsToCsvAlgorithm(QgsProcessingAlgorithm):
    """This extracts sheets from an xlsx and creates csvs"""

    # Constants used to refer to parameters and outputs.
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ExcelSheetsToCsvAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'excel2csvscript'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Excel Sheets To Csv Conversion')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Helper scripts')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'helperscripts'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Script for extracting sheets from an excel xlsx and creating csv files. "
                       "Using a temporary directory for outputs may result in errors.")

    def initAlgorithm(self, config=None):
        """
        Algo input and param definition
        """

        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT,
                self.tr('Excel workbook')
            )
        )

        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT,
                self.tr('Output directory')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Execute
        """

        source = self.parameterAsString(
            parameters,
            self.INPUT,
            context
        )

        outpath = self.parameterAsString(
            parameters,
            self.OUTPUT,
            context
        )

        workbook = xlrd.open_workbook(source)
        # Send some information to the user
        feedback.pushInfo('{} sheets to process'.format(workbook.nsheets))

        # Compute the number of steps to display within the progress bar
        total = 100.0 / workbook.nsheets if workbook.nsheets else 0
        sheets = workbook.sheet_names()

        for current, sheetname in enumerate(sheets):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break

            csvfile = '{}/{}.csv'.format(outpath,sheetname)
            feedback.pushInfo('{} writing'.format(csvfile))

            sheet = workbook.sheet_by_index(current)
            # csv file writer object
            fw = csv.writer(open(csvfile, 
                                 'w',
                                 newline=""),
                            dialect='excel')

            for row in range(sheet.nrows):
                fw.writerow(sheet.row_values(row))

            # Update the progress bar
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: True}
