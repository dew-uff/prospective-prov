
from collections import defaultdict
from .ExecutionProvenance import ExecutionProvenanceAnalyzer


class ExecutionProvenance(object):
    """ Get script execution information in noWorkflow """
    def __init__(self, *args):
        self.trial = args[0]
        self.provenance = args[1]
        self.node_hash = args[2]
        self.start = args[3]
        self.data_set = args[4]
        self.sqlite = args[5]
        self.column = args[6]
        self.hash_code = args[7]
        self.arrayHashing = args[8]

    def activations_provenance(self):
        """ Get script execution information about code activations """
        _activation_data = self.sqlite.activation_line(self.data_set)
        _activation = [element[0] for element in _activation_data]
        retrospective = ExecutionProvenanceAnalyzer(self.provenance,
                                                    self.node_hash,
                                                    self.start, None, None,
                                                    self.arrayHashing)
        retrospective.make_activations(_activation)

    def contents_provenance(self):
        """ Get script execution information about variable contents """
        _key_content = []
        _key_column = []
        _var_content = []
        _title_codes = []
        data_cont = self.sqlite.variables_content(self.data_set)
        for data in data_cont:
            _key_content.append(data[0])
            _var_content.append(data[1])
            _title_codes.append(data[2])
            _key_column.append(data[3])
        retrospective = ExecutionProvenanceAnalyzer(self.provenance,
                                                    self.node_hash,
                                                    self.start,
                                                    self.column,
                                                    self.hash_code,
                                                    self.arrayHashing)
        retrospective.make_contents(_var_content,
                                    _key_content,
                                    _title_codes)

    def runtime_provenance(self):
        """ Get script execution information about checkpoints """
        array_key = []
        array_check = []
        array_key_type = []
        checkpoints = defaultdict(list)
        data_check = self.sqlite.runtime_line(self.data_set)
        array_key_column = []
        for data in data_check:
            array_key.append(data[0])
            time = round(float(data[1]), 6)
            array_check.append(time)
            array_key_column.append(data[2])
            array_key_type.append(data[3])
            dictionary = '{}{}{}'.format(data[0], data[3], data[2])

            checkpoints[dictionary].append(round(float(data[1]), 6))

        retrospective = ExecutionProvenanceAnalyzer(self.provenance,
                                                    self.node_hash,
                                                    self.start,
                                                    self.column,
                                                    self.hash_code,
                                                    self.arrayHashing)
        retrospective.make_checkpoints(checkpoints)