"""
Copyright (c) 2019 Universidade Federal Fluminense (UFF). All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NON INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 1OTHER DEALINGS IN THE SOFTWARE.
"""

import argparse
import os.path
import sqlite3

from collections import defaultdict
from capture.collector.ExperimentDataCollector import ExperimentDataCollector
from capture.provenance.DefinitionProvenance import DefinitionProvenanceAnalyzer


class ProspectiveProv(object):
    """ ProspectiveProv object. Functions for starting the script here!
        _get_components: return all code components of script
        _get_function: return code component of specific function
        run_prospective: runtime prospectiveProv
    """

    def __init__(self, settings):
        self.conf = settings
        self.run()

    def getComponents(self, sqlite):
        """Get all code components by trial_id"""
        return sqlite.code_components(self.conf)

    def getSubscript(self, sqlite):
        """Get all code components by trial_id"""
        return sqlite.code_subscript(self.conf)


    def getFunction(self, sqlite):
        """Get all code of a function by name_def and trial_id"""
        return sqlite.code_function(self.conf)

    def noWorkflowConnect(self):
        """Connects to the .sqlite database"""
        return sqlite3.connect(self.conf['database'][0])

    def run(self):
        """Call modules and run prospectiveProv"""
        """ There are currently four filter types in prospective Prov.
                partial: select code components based on start and last line: not active!
                everything: select all code components: active!
                function: select a specific function on script: active!
        """
        """ There are currently four types of collection model in prospective Prov
                only prospective: It builds only graphs prospective provenance: active!
                prospective+activation: It lists in graph all blocks activated in code execution: active!
                prospective+checkpoint: It lists in graph the execution time of each line: active!
                prospective+content: It lists the contents of all variables in the script: active!
        """
        conn = self.noWorkflowConnect()
        sqlite = ExperimentDataCollector(self.conf['trial_id'][0], conn)

        with conn:
            """ check trial status """
            status = sqlite.trial_check
            if status:
                prov = DefinitionProvenanceAnalyzer(self.conf['trial_id'][0])
                codes = {'lines': self.getComponents,
                         'everything': self.getComponents,
                         'function': self.getFunction}

                tables = codes[self.conf['filter_type'][0]](sqlite)
                if tables:
                    prov.componentAnalyzer(sqlite, conn, tables, self.conf)
                else:
                    print("Something went wrong while getting the data."
                          "Make sure all parameters are correct!")
            else:
                print("Trial not found!")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("trial", help="trial id", nargs='+')
    parser.add_argument("--var", type=str, dest="content",
                        help="insert the value 1 to show "
                             "the content of each variable in "
                             "the experiment in provenance graph.",
                        default=0)
    parser.add_argument('--act', type=str, dest="activation",
                        help="Insert the value 1 to show "
                             "all code activations in provenance graph.",
                        default=0)

    parser.add_argument('--show', type=str, nargs='+', dest="show",
                        help="--show s: show all script\n "
                             "--show f <function_name>: Show diagram by function (using function name as search filter)"
                             "--show l <line_start> <line_end>: Generate diagram from a script subset (using start "
                             "line and end line as filter) "
                             "Generate diagram from a script subset.",
                        default='s')

    parser.add_argument('--line', type=str, dest="line",
                        help="Insert the start line and end line "
                             "Generate diagram from a script subset.",
                        default=False)

    parser.add_argument('--run', type=str, dest="runtime",
                        help="Insert the value 1 to show "
                             "the execution time of each code block.",
                        default=0)
    parser.add_argument('--i', type=str, dest="indented",
                        help="Insert the value 1 to show "
                             "indented of each code block.",
                        default=0)
    parser.add_argument("--dir", type=str, dest="database",
                        help="Set project path where is the db.sqlite file. "
                             "Default to current directory ",
                        default='.noworkflow/db.sqlite')

    argument = parser.parse_args()
    indented = bool(argument.indented)
    activations = bool(argument.activation)
    checkpoints = bool(argument.runtime)
    contents = bool(argument.content)
    filter_mode = argument.show

    start_line = 0
    final_line = 0
    name_def = None
    provenance_types = "everything"

    if len(filter_mode) > 0:
        if filter_mode[0] == 's':
            provenance_types = "everything"
        if filter_mode[0] == 'f':
            provenance_types, name_def = "function", filter_mode[1]
        if filter_mode[0] == 'l':
            provenance_types = "lines"
            start_line = filter_mode[1]
            final_line = filter_mode[2]



    if argument.trial[0] == "trial":
        trial_id = argument.trial[1]
    elif argument.trial[0].startswith("trial") == "trial":
        trial_id = argument.trial[0].replace("trial", "")
    else:
        trial_id = argument.trial[0]

    db = argument.database
    data = defaultdict(list)

    data['database'].append(db)
    data['trial_id'].append(trial_id)
    data['indented'].append(indented)
    data['activations_v'].append(activations)
    data['checkpoints_v'].append(checkpoints)
    data['start'].append(start_line)
    data['final'].append(final_line)
    data['contents_v'].append(contents)
    data['filter_type'].append(provenance_types)
    data['def_name'].append(name_def)

    file = os.path.exists(db)
    if file:
        ProspectiveProv(data)
    else:
        print("File db.sqlite not found!")


if __name__ == "__main__":
    main()
