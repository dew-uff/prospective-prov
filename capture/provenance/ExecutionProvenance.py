from collections import defaultdict


class ExecutionProvenanceAnalyzer:
    def __init__(self, *args):
        self.graph = args[0]
        self.node_hash = args[1]
        self.node_start = args[2]
        self.node_column = args[3]
        self.node_generic = args[4]
        self.arrayHashing = args[5]

        # print(self.arrayHashing)

    def make_checkpoints(self, checkpoint):
        average = defaultdict(list)
        for index in checkpoint:
            valueIndex = 0
            countIndex = 0
            for nodeBlock in checkpoint[index]:
                valueIndex = valueIndex + nodeBlock
                countIndex = countIndex + 1

            mean = float(valueIndex/countIndex)
            mean = round(mean, 6)
            average[index].append(mean)
            average[index].append(mean)

        for lineBlock in average:
            # print("Line: ", lineBlock)
            if lineBlock in self.node_generic:
                accessNode = self.node_generic.index(lineBlock)
                myItem = self.node_hash[accessNode]
                hashNode = 'time{}'.format(myItem)

                self.graph.node(hashNode, str(average[lineBlock][0]),
                                shape='cds',
                                fillcolor='#FFDE6A',
                                fontsize='12')
                self.graph.edge(hashNode, self.node_hash[accessNode],
                                arrowhead='none',
                                style='dashed')

    def make_activations(self, activation):
        def toHidden(node):
            self.graph.node(node, fillcolor='#EBEBEB')

        def toShow(node):
            self.graph.node(node, fillcolor='#85CBD0')

        for i, nodeBlock in enumerate(self.node_hash):
            before = self.node_hash[i - 1]
            if i == 0:
                continue
            elif 'end' in nodeBlock:
                toShow(nodeBlock)
            elif self.node_start[i] not in list(activation):
                if 'def' in before:
                    toHidden(before)
                toHidden(nodeBlock)
            elif 'else' in before or 'try' in before:
                toShow(before)

    def make_contents(self, content, key, title):
        collections = defaultdict(list)
        names = defaultdict(list)
        codes = defaultdict(list)
        var = defaultdict(list)

        for index, item in enumerate(key):
           # print('item:',item, 'title:', title[index],'cont:', content[index])
            var[item, title[index]].append(content[index])
            names[title[index]].append(None)
            codes[item].append(None)

        for line in codes:
            # print('Linha: ', line)
            for title in names:
                # print('Line {} - Title {}'.format(line, title))
                n = len(var[line, title])
                if n > 0:
                    if n > 4:
                        textBox = "{}: {},{}: {} ...{}: {},{}: {}\n".format(
                                                      title, var[line, title][0],
                                                      title, var[line, title][1],
                                                      title, var[line, title][n - 2],
                                                      title, var[line, title][n - 1])
                        collections[line].append(textBox)
                    else:
                        textBox = ''
                        textBox = [textBox + '{}: {},'.format(title, var[line, title][idx]) for idx in range(0, n)]
                        collections[line].append(textBox[0])

        for dictionary in collections:
            textBox = ''
            for indexes in range(0, len(collections[dictionary])):
                textBox += str(collections[dictionary][indexes])

                # print(textBox)

                if dictionary in self.node_start:
                    # print('dict ',dictionary)
                    hashing = '{}{}'.format('content', dictionary)
                    self.graph.node(hashing, textBox,
                                    shape='note',
                                    fillcolor='#FFDE6A',
                                    fontsize='12')
                    self.graph.edge(hashing,
                                    self.node_hash[self.node_start.index(dictionary)],
                                    arrowhead='none',
                                    style='dashed')
