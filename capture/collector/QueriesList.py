class QueriesList:

    def __init__(self, trial):
        self.trial = trial

    def get_arguments(self, start):
        query = ("select name from code_component "
                 "where trial_id={0} and "
                 "(first_char_line == {1} and "
                 "type == 'arguments')").format(self.trial, start)
        return query

    @property
    def get_all_def(self):
        query = ("select name, type, first_char_line "
                 "from code_component "
                 "where type='function_def' "
                 "and trial_id={0} "
                 ).format(self.trial)
        return query

    @property
    def get_all_calls(self):
        query = ("select name, type, first_char_line "
                 "from code_component "
                 "where type='call' "
                 "and trial_id={0} "
                 ).format(self.trial)
        return query

    def get_else_collector(self, start, last):
        query = ("select first_char_line "
                 "from code_component "
                 "where trial_id={0} "
                 "and type='syntax' "
                 "and name='else:' "
                 "and first_char_line >= {1} "
                 "and last_char_line <= {2} "
                 ).format(self.trial, start, last)
        return query

    def get_status_collector(self):
        query = ("select status from "
                 "trial where id = {0}"
                 ).format(self.trial)
        return query

    def get_def_all_collector(self):
        query = ("select first_char_line, last_char_line "
                 "from code_component "
                 "where trial_id = {0} and type='function_def'"
                 ).format(self.trial)
        return query

    def get_def_name_collector(self, name):
        query = ("select first_char_line, last_char_line "
                 "from code_component "
                 "where trial_id = {0} "
                 "and name = '{1}' "
                 "and type = 'function_def' "
                 ).format(self.trial, name)
        return query

    def get_activations_collector(self, data=None):
        query = ("select code_component.first_char_line, evaluation.checkpoint "
                 "from evaluation join code_component "
                 "where evaluation.code_component_id = code_component.id "
                 "and evaluation.trial_id = code_component.trial_id "
                 "and evaluation.trial_id = {0} "
                 "and code_component.first_char_line != -1 "
                 "order by code_component.first_char_line "
                 ).format(self.trial)
        return query

    def get_activations_collector_partial(self, data):
        query = ("select code_component.first_char_line, evaluation.checkpoint "
                 "from evaluation join code_component "
                 "where evaluation.code_component_id = code_component.id "
                 "and evaluation.trial_id = code_component.trial_id "
                 "and evaluation.trial_id = {0} "
                 "and code_component.first_char_line != -1 "
                 "and code_component.first_char_line >= {1} "
                 "order by code_component.first_char_line "
                 ).format(self.trial, data['start'][0])
        return query

    def get_activations_collector_lines(self, data):
        query = ("select code_component.first_char_line, evaluation.checkpoint "
                 "from evaluation join code_component "
                 "where evaluation.code_component_id = code_component.id "
                 "and evaluation.trial_id = code_component.trial_id "
                 "and evaluation.trial_id = {0} "
                 "and code_component.first_char_line != -1 "
                 "and code_component.first_char_line >= {1} "
                 "and code_component.last_char_line <= {2} "
                 "order by code_component.first_char_line "
                 ).format(self.trial, data['start'][0], data['final'][0])
        return query

    def get_activations_collector_function(self, data):
        query = ("select code_component.first_char_line, evaluation.checkpoint "
                 "from evaluation join code_component "
                 "where evaluation.code_component_id = code_component.id "
                 "and evaluation.trial_id = code_component.trial_id "
                 "and evaluation.trial_id = {0} and code_component.first_char_line != -1 "
                 "and code_component.first_char_line >= {1} "
                 "and code_component.last_char_line <= {2} "
                 "order by code_component.first_char_line "
                 ).format(self.trial, data['start'][0], data['final'][0])
        return query

    def get_checkpoint_collector(self, trial):
        query = ("select code_component.first_char_line, evaluation.checkpoint, "
                 "code_component.first_char_column, "
                 "code_component.type "
                 "from evaluation join code_component "
                 "where evaluation.code_component_id = code_component.id "
                 "and evaluation.trial_id = code_component.trial_id "
                 "and evaluation.trial_id = {0} "
                 "and code_component.first_char_line != -1 "
                 "and code_component.type == 'name' "
                 "order by code_component.first_char_line "
                 ).format(self.trial)
        return query

    def get_checkpoint_collector_partial(self, trial, data):
        query = ("select code_component.first_char_line, evaluation.checkpoint, "
                 "code_component.first_char_column "
                 "from evaluation join code_component "
                 "where evaluation.code_component_id = code_component.id "
                 "and evaluation.trial_id = code_component.trial_id "
                 "and evaluation.trial_id = {0} "
                 "and code_component.first_char_line != -1 "
                 "and code_component.type == 'name' "
                 "and code_component.first_char_line >= {1} "
                 "order by code_component.first_char_line "
                 ).format(self.trial, data['start'][0])
        return query

    def get_checkpoint_collector_lines(self, trial, data):
        query = ("select code_component.first_char_line, evaluation.checkpoint, "
                 "code_component.first_char_column "
                 "from evaluation join code_component "
                 "where evaluation.code_component_id = code_component.id "
                 "and evaluation.trial_id = code_component.trial_id "
                 "and evaluation.trial_id = {0} "
                 "and code_component.first_char_line != -1 "
                 "and code_component.type == 'name' "
                 "and code_component.first_char_line >= {1} "
                 "order by code_component.first_char_line "
                 ).format(self.trial, data['start'][0])
        return query

    def get_checkpoint_collector_function(self, trial, data):
        query = ("select code_component.first_char_line, evaluation.checkpoint, "
                 "code_component.first_char_column "
                 "from evaluation join code_component "
                 "where evaluation.code_component_id = code_component.id "
                 "and evaluation.trial_id = code_component.trial_id "
                 "and evaluation.trial_id = {0} "
                 "and code_component.first_char_line != -1 "
                 "and code_component.type == 'name' "
                 "and code_component.first_char_line >= {1} "
                 "and code_component.last_char_line <= {2} "
                 "order by code_component.first_char_line "
                 ).format(self.trial, data['start'][0], data['final'][0])
        return query

    def get_content_collector(self, data=None):
        query = ("select code_component.first_char_line, evaluation.repr, code_component.name, "
                 "code_component.first_char_column "
                 "from evaluation join code_component "
                 "where evaluation.code_component_id = code_component.id "
                 "and evaluation.trial_id = code_component.trial_id "
                 "and evaluation.trial_id = {0} and code_component.first_char_line != -1 "
                 "and code_component.type == 'name' "
                 "order by code_component.first_char_line "
                 ).format(self.trial)
        return query

    def get_content_collector_partial(self, data):
        query = ("select code_component.first_char_line, evaluation.repr, code_component.name, "
                 "code_component.first_char_column "
                 "from evaluation join code_component "
                 "where evaluation.code_component_id = code_component.id "
                 "and evaluation.trial_id = code_component.trial_id "
                 "and evaluation.trial_id = {0} "
                 "and code_component.first_char_line != -1 "
                 "and code_component.type == 'name' "
                 "and code_component.first_char_line >= {1} "
                 "order by code_component.first_char_line "
                 ).format(self.trial, data['start'][0])
        return query

    def get_content_collector_lines(self, data):
        query = ("select code_component.first_char_line, evaluation.repr, code_component.name, "
                 "code_component.first_char_column "
                 "from evaluation join code_component "
                 "where evaluation.code_component_id = code_component.id "
                 "and evaluation.trial_id = code_component.trial_id "
                 "and evaluation.trial_id = {0} and code_component.first_char_line != -1 "
                 "and code_component.type == 'name' "
                 "and code_component.first_char_line >= {1} and code_component.last_char_line <= {2} "
                 "order by code_component.first_char_line "
                 ).format(self.trial, data['start'][0], data['final'][0])
        return query

    def get_content_collector_function(self, data):
        query = ("select code_component.first_char_line, evaluation.repr, code_component.name "
                 "from evaluation join code_component "
                 "where evaluation.code_component_id = code_component.id "
                 "and evaluation.trial_id = code_component.trial_id "
                 "and evaluation.trial_id = {0} "
                 "and code_component.first_char_line != -1 "
                 "and code_component.type == 'name' "
                 "and (code_component.first_char_line >= {1} "
                 "and  code_component.last_char_line <= {2}) "
                 "order by code_component.first_char_line "
                 ).format(self.trial, data['start'][0], data['final'][0])
        return query

    def list_partial_codes(self, data):
        query = ("select first_char_line, last_char_line, type, name, first_char_column "
                 "from code_component "
                 "where trial_id={0} "
                 "and first_char_line >= {1} "
                 "order by code_component.first_char_line "
                 ).format(self.trial, data['start'][0])
        return query

    def list_lines_codes(self, data):
        query = ("select first_char_line, last_char_line, type, name, first_char_column "
                 "from code_component "
                 "where trial_id={0} "
                 "and first_char_line >= {1} "
                 "and last_char_line <= {2} "
                 "order by code_component.first_char_line "
                 ).format(self.trial, data['start'][0], data['final'][0])
        return query

    def list_all_codes(self, data=None):
        query = ("select first_char_line, last_char_line, type, name, first_char_column "
                 "from code_component "
                 "where trial_id = {0} "
                 "and first_char_line != -1 "
                 "order by code_component.first_char_line "
                 ).format(self.trial)
        return query

    def get_show_by_function(self, data, verify):
        if verify:
            query = ("select first_char_line, last_char_line, type, name, first_char_column "
                     "from code_component "
                     "where trial_id={0} "
                     "and code_component.name='{1}' and code_component.type='function_def' "
                     "order by code_component.first_char_line"
                     ).format(self.trial, data['def_name'][0])
        else:
            query = ("select first_char_line, last_char_line, type, name, first_char_column "
                     "from code_component "
                     "where trial_id={0} "
                     "and (code_component.first_char_line >= {1} "
                     "and code_component.last_char_line <= {2}) "
                     "order by code_component.first_char_line "
                     ).format(self.trial, data['start'][0], data['final'][0])
        return query
