import sqlite3

from capture.collector.QueriesList import QueriesList
from collections import defaultdict


class NoWorkflowDatabase:
    def __init__(self, database):
        self.db = database

    @property
    def create_connection(self):
        try:
            return sqlite3.connect(self.db)
        except SystemError:
            print(' Connection Refused! ')
        return None


class ExperimentDataCollector:

    def __init__(self, *args):
        self.q = QueriesList(args[0])
        self.trial = args[0]
        self.cursor = args[1].cursor()

    def selection_args(self, start):
        queries = self.cursor
        queries.execute(self.q.get_arguments(start))
        rows = queries.fetchall()
        if len(rows) > 0:
            return str(rows[0][0])
        else:
            return -1

    def function_check(self, rows):
        """

        :rtype: object
        """
        _first = 0
        _last = 0
        string = defaultdict(list)
        if len(rows) > 0:
            for line in rows:
                _first = line[0]
                _last = line[1]

            string['trial_id'].append(self.trial)
            string['start'].append(_first)
            string['final'].append(_last)

            self.cursor.execute(self.q.get_show_by_function(string, False))
            return self.cursor.fetchall()
        else:
            print('This function does not exist!')
            return False

    @staticmethod
    def queries_check(rows):
        if len(rows) > 0:
            return rows
        else:
            print("Something went wrong in the trial verification!")
            return -1

    def variables_content(self, data):
        functions = {'lines': self.q.get_content_collector_lines,
                     'partial': self.q.get_content_collector_partial,
                     'everything': self.q.get_content_collector,
                     'function': self.q.get_content_collector_function}

        self.cursor.execute(functions[data['filter_type'][0]](data))
        return self.queries_check(self.cursor.fetchall())

    @property
    def trial_check(self):
        """ Check status a trial on noWorkflow """
        self.cursor.execute(self.q.get_status_collector())
        rows = self.cursor.fetchall()
        if len(rows) > 0 and rows[0][0] == "finished":
            return True
        else:
            print("Something is wrong! Maybe the trial "
                  "is not available in noWorkflow! ")
            print("Try running the trial again in noWorkflow! ")
            return False

    @property
    def select_code_def_all(self):
        """ Draw graph with all functions"""
        self.cursor.execute(self.q.get_def_all_collector())
        return self.queries_check(self.cursor.fetchall())

    def runtime_line(self, data):
        """ Draw graph with all code components - list checkpoints"""
        functions = {'lines': self.q.get_checkpoint_collector_lines,
                     'partial': self.q.get_checkpoint_collector_partial,
                     'everything': self.q.get_checkpoint_collector,
                     'function': self.q.get_checkpoint_collector_function}

        self.cursor.execute(functions[data['filter_type'][0]](data))
        return self.queries_check(self.cursor.fetchall())

    @property
    def return_def(self):
        self.cursor.execute(self.q.get_all_def)
        return self.queries_check(self.cursor.fetchall())

    @property
    def return_calls(self):
        self.cursor.execute(self.q.get_all_calls)
        return self.queries_check(self.cursor.fetchall())

    def activation_line(self, data):
        """ Draw graph with all code components - list activations"""
        functions = {'lines': self.q.get_activations_collector_lines,
                     'partial': self.q.get_activations_collector_partial,
                     'everything': self.q.get_activations_collector,
                     'function': self.q.get_activations_collector_function}
        self.cursor.execute(functions[data['filter_type'][0]](data))
        return self.queries_check(self.cursor.fetchall())

    def code_components(self, data):
        functions = {'lines': self.q.list_lines_codes,
                     'partial': self.q.list_partial_codes,
                     'everything': self.q.list_all_codes}
        self.cursor.execute(functions[data['filter_type'][0]](data))
        return self.queries_check(self.cursor.fetchall())

    def code_function(self, data):
        self.cursor.execute(self.q.get_show_by_function(data, True))
        return self.function_check(self.cursor.fetchall())
