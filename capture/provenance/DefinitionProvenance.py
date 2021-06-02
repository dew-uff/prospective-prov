from collections import defaultdict
from capture.build.ConditionNodes import Nodes
from capture.build.GraphDrawer import GraphDrawer
from capture.build.Graphviz import Graphviz
from capture.build.HashingMapper import HashingMapper
from capture.build.SyntaxWrite import SyntaxWrite
from .ExecutionProvenanceCollector import ExecutionProvenance
from capture.collector.ExperimentDataCollector import ExperimentDataCollector


class DefinitionProvenanceAnalyzer:
    def __init__(self, trial):
        self.provenance = Graphviz(trial).initialize()

        self.def_list = []

        self.call = defaultdict(list)
        self.defs = defaultdict(list)
        self.visited_x = []
        self.visited_y = []

        self.def_method = defaultdict(list)

        self.class_method = []

        self.class_def_name = []
        self.class_def_start = []
        self.class_def_final = []

        self.hash_index = []

        self.trial = trial
        ''' Array List - Try components '''
        self.try_except = defaultdict(list)

        self.def_function = []
        self.singleIF = []
        self.generic_hash = []
        self.def_function_final = []
        self.def_function_after = []
        ''' Array List - Lines and code components'''
        self.class_list = []
        self.start = []
        self.column = []
        self.last = []
        self.block = []
        self.type = []
        ''' Array List - All nodes '''
        self.node_hash = []
        self.node_else = []
        self.node_if = []
        self.node_for = []
        self.node_for_sup = []
        self.node_end_for = []
        self.arrayHashing = defaultdict(list)

    def syntaxRulesIF(self):
        """
        Step 1: format_Condition_Node
        Step 2: create_Condition_Node()
        Step 3: organize_Sequences_IF_ELSE()
        Step 4: update_Sequences_IF_ELSE()
        """
        """ Detect conditional structures within others """
        self.format_Condition_Node()
        """ Link conditional structures that belong to them """
        self.create_Condition_Node()
        """ Arrange and link IF and ELSE sequences """
        self.organize_Sequences_IF_ELSE()
        """ Report conditional items already covered and rearranged """
        self.update_Sequences_IF_ELSE()

    def syntaxRulesFOR(self):
        """
        Step 1: get_Call_Back()
        Step 2: get_Call_Ends()
        Step 3: get_Last_Loop()
        """
        """ Create a back edge within a loop [WHILE, FOR] """
        self.get_Call_Back()
        """ Create an ending edge within a loop [WHILE, FOR] """
        self.get_Call_Ends()
        """ Create and check for a next loop [WHILE, FOR] in sequence """
        self.get_Last_Loop()

    def syntaxRulesTRY(self):
        """
        Step 1: check_Try()
        Step 2: getCallTryException()
        """
        self.check_Try()
        self.getCallTryException()

    def show(self):
        # print('i|INDEX|START|LAST|NODE-HASH|NODE-ELSE|NODE-IF|NODE-END-FOR|NODE-FOR|COLUMN| DEF-LIST|\n')
        for i in range(0, len(self.node_hash)):
            string = '{}|{}* {} {} {} {} {} {} {} {} {} '.format(i, self.hash_index[i], self.start[i], self.last[i],
                                                                 self.node_hash[i], self.node_else[i], self.node_if[i],
                                                                 self.node_end_for[i], self.node_for[i], self.column[i],
                                                                 self.def_list[i])
            # print(string)

    def createBoxesInFunctions(self):
        """
        Create a boundary for the representation of functions.
        Here, all content within functions is bounded by boxes, just as in classes.
        """
        for index, node in enumerate(self.node_hash):
            if 'function_def' in node:
                border = SyntaxWrite().getIndexArray(self.last[index], self.start)
                for index_2 in range(index, border + 1):
                    nameBoxes = 'cluster{}'.format(index)
                    with self.provenance.subgraph(name=nameBoxes) as subgroupA:
                        nodes = self.node_hash[index_2]
                        subgroupA.attr(style='dashed')
                        subgroupA.node(nodes)
                        condition = ['for', 'while', 'if', 'elif']
                        if any(x in nodes for x in condition):
                            subgroupA.node(nodes + 'c')

    def createBoxInClass(self):
        for cName, cStart, cLast in zip(self.class_def_name,
                                        self.class_def_start,
                                        self.class_def_final):
            for index, nodes in enumerate(self.node_hash):
                show_name = True
                startNode = self.start[index]
                getLimitX = startNode >= cStart
                getLimitY = startNode <= cLast
                if getLimitX and getLimitY:
                    nameCluster = 'cluster{}'.format(cName)
                    with self.provenance.subgraph(name=nameCluster) as subgroupA:
                        if show_name:
                            nameClass = 'Class {}'.format(cName)
                            subgroupA.attr(label=nameClass, style='dashed')
                            show_name = False
                        if 'function_def' in nodes:
                            functionStart = self.start[index]
                            functionFinal = self.last[index]
                            indexStart = index
                            functionName = 'cluster{}'.format(nodes)
                            with subgroupA.subgraph(name=functionName) as subgroupB:
                                subgroupA.attr(label='', style='dashed')
                                while True:
                                    getLimitX = self.start[indexStart] >= functionStart
                                    getLimitY = self.start[indexStart] <= functionFinal
                                    if getLimitX and getLimitY:
                                        subgroupB.node(self.node_hash[indexStart])
                                    else:
                                        break
                                    indexStart = indexStart + 1
                        else:
                            subgroupA.node(self.node_hash[index])

    def verify_function_check(self):
        for index, node in enumerate(self.node_hash):
            node_else = self.node_else[index]
            node_function = self.def_list[index]
            null_check = node_else is not None and node_function is not None
            if node_else != node_function and null_check:
                #self.node_else[index] = 'end{}'.format(node_function)
                self.node_else[index] = node_function

    def indented_label(self):
        for index, node in enumerate(self.node_hash):
            string_column = '{' + str(self.column[index]) + '}'
            self.provenance.node(node, xlabel=string_column)

    def format_column(self):
        keys = defaultdict(list)
        for index, item in enumerate(self.start):
            keys[item].append(index)

        for values in keys:
            if len(keys[values]) > 1:
                min_column = self.column[min(keys[values])]
                for element in keys[values]:
                    self.column[element] = min_column

    def linking_nodes_graph(self):
        hash_loop = []
        for i in range(1, len(self.node_hash) - 1):
            current = self.node_hash[i]
            next_node = self.node_hash[i + 1]
            ''' Visited node X (Any node)'''
            visitX = (current not in self.visited_x)
            ''' Visited node Y (Any node)'''
            visitY = (next_node not in self.visited_y)
            ''' Visited node Z (only loop node)'''
            visitZ = (current not in hash_loop)
            checking = visitX and visitY and visitZ
            '''
            Check limit in def function
            if self.def_list[i] != None:
                limite_1 = self.node_hash.index(self.def_list[i])
                limite = self.last[limite_1]
                check_return = self.start[i + 1] <= limite
            '''
            if checking:
                if (('if' not in current) and ('else' not in current)) and (
                        (self.node_else[i] != None) and (self.node_for[i] != None)):
                    self.provenance.edge(current, self.node_for[i], style="dashed")

                elif current in self.def_function_after:
                    continue
                elif 'function_def' in next_node:
                    if next_node in self.def_function:
                        index_def_node = self.def_function.index(next_node)
                        self.provenance.edge(current, self.def_function_final[index_def_node])
                elif 'if' in current:
                    self.provenance.edge(current, next_node, label='   True')
                    if '*' in self.node_else[i]:
                        hash_string = self.node_else[i]
                        if self.node_for[i] is not None:
                            hash_for = self.node_for[i]
                            item_false = self.node_hash.index(hash_string[0:len(hash_string) - 1])
                            if self.node_for[i] != self.node_for[item_false]:
                                self.provenance.edge(current, self.node_for[i], label='   False')
                            else:
                                self.provenance.edge(current, hash_string[0: len(hash_string) - 1], label='   False')
                    '''
                    elif '-' in self.node_else[i]:
                        lastNode = SyntaxWrite().getIndexArray(self.last[i], self.start)
                        self.provenance.edge(current, self.node_hash[lastNode], label='   False')
                    '''
                elif 'try' in current:
                    self.provenance.edge(current, next_node)
                elif 'exception' in current:
                    self.provenance.edge(self.node_if[i], self.node_hash[i])
                    self.provenance.edge(current, next_node)
                elif 'else' in current:
                    self.provenance.edge(self.node_if[i], self.node_hash[i], label='   False')
                    self.provenance.edge(current, next_node)
                elif 'for' in current or 'while' in current:
                    self.provenance.edge(current, next_node)
                else:
                    if self.node_else[i] is None:
                        self.provenance.edge(current, next_node)
                    else:
                        self.provenance.edge(current, self.node_else[i])

        self.createBoxesInFunctions()

    def create_Global_End_Node(self):
        self.node_hash.append('end')
        self.node_else.append(None)
        self.node_if.append(None)
        self.last.append(self.last[-1] + 1)
        self.last.append(self.last[-1] + 1)
        self.start.append(self.last[-1] + 1)
        self.column.append(0)
        self.block.append('End')
        self.type.append('end-code')
        self.provenance.node('end', label='End')
        element = '{}{}'.format(self.last[-1] + 1, 0)
        self.hash_index.append(int(element))
        self.generic_hash.append('{}name{}'.format(self.last[-1] + 1, 0))
        return True

    def start_node(self):
        self.node_hash.append('start')
        self.node_else.append(None)
        self.node_if.append(None)
        self.last.append(0)
        self.start.append(0)
        self.column.append(0)
        self.block.append('Start')
        self.type.append('start-code')
        self.hash_index.append(0)
        self.provenance.node('start', label='Start')
        self.generic_hash.append('{}name{}'.format(0, 0))
        return True

    def arguments_selection(self, conn, start):
        sqlite = ExperimentDataCollector(self.trial, conn)
        return sqlite.selection_args(start)

    def getCallTryException(self):
        try:
            for i in range(0, len(self.node_hash) - 1):
                current = self.node_hash[i]
                if 'try' in current:
                    intervalo_final = self.last[i]
                    intervalo_start = i
                    line_exception = -1
                    while True:
                        if intervalo_final <= self.start[intervalo_start]:
                            self.node_else[i] = self.node_hash[intervalo_start + 1]
                            break
                        if 'exception' in self.node_hash[intervalo_start]:
                            self.node_if[intervalo_start] = current
                            line_exception = intervalo_start

                        intervalo_start = intervalo_start + 1

                    if line_exception != -1:
                        self.node_else[line_exception - 1] = self.node_else[i]
        except:
            print('Error in update 4!')

    def create_Condition_Node(self):
        """
        insert tag in Condition Elements [node_if, node_elif, node_else]
        dependencies: all, DefinitionProvenance Class
        return: None
        """
        for index, node in enumerate(self.node_hash):
            if 'if' in node:
                lastLoop = SyntaxWrite().getIndexArray(self.last[index], self.start)
                for key in range(index + 1, lastLoop):
                    checkColumn = self.column[index] == self.column[key]
                    checkPosition = self.start[key] < self.last[index]
                    if SyntaxWrite().compareCondition(self.node_hash[key]):
                        if checkColumn and checkPosition:
                            self.node_if[key] = node
                            self.node_else[index] = self.node_hash[key]
                            self.last[key] = self.last[index]

    def organize_Sequences_IF_ELSE(self):
        """
         This method rearranges all conditions by binding them to their
         respective blocks of code.
         return: None
        """
        for index, node in enumerate(self.node_hash):
            there_Element = self.node_else[index] is not None
            if there_Element and 'if' in node and 'else' in self.node_else[index]:
                this_item = self.node_hash.index(self.node_else[index]) - 1
                next_item = self.node_hash.index(self.node_else[index])
                while True:
                    if 'else' in self.node_hash[next_item]:
                        node_else = self.node_else[next_item]
                        next_item = self.node_hash.index(node_else)
                    else:
                        self.node_else[this_item] = self.node_hash[next_item]
                        break

    def format_Condition_Node(self):
        """
        return: None
        """
        """ This item checks whether a given IF has any ELSE related to it """
        for key, node in enumerate(self.node_hash):
            if SyntaxWrite().compareCondition(node):
                idx = key + 1
                while True:
                    if self.last[key] <= self.start[idx]:
                        self.node_else[key - 1] = self.node_hash[idx + 1]
                        self.node_else[key] = self.node_hash[idx + 1]
                        break
                    idx = idx + 1
        """ This item checks already connected nodes and formats incorrectly linked nodes """
        for key, node in enumerate(self.node_hash):
            if SyntaxWrite().compareCondition(node):
                lastElse = SyntaxWrite().getIndexArray(self.last[key], self.start)
                lastNode = self.node_hash[lastElse]
                value = lastElse
                if SyntaxWrite().compareCondition(lastNode):
                    while True:
                        if SyntaxWrite().compareCondition(lastNode):
                            lastElse = SyntaxWrite().getIndexArray(self.last[lastElse], self.start)
                            value = lastElse - 1
                            lastNode = self.node_hash[lastElse]
                            break
                        else:
                            else_ = SyntaxWrite().getIndexArray(self.last[value], self.start)
                            self.provenance.edge(self.node_hash[else_], lastNode)
                            self.visited_x.append(self.node_hash[else_])
                            self.visited_y.append(lastNode)
                            self.node_else[else_] = lastNode
                            break
                else:
                    self.node_else[value] = lastNode
                    else_ = SyntaxWrite().getIndexArray(self.last[value], self.start)
                    self.provenance.edge(self.node_hash[else_], lastNode)

    def get_Call_Ends(self):
        """
        Get the loop boundaries, ie the end nodes and return nodes.
        dependencies: all, DefinitionProvenance class
        return: None
        """
        visitedArray = []
        for index, currentNode in enumerate(self.node_hash):
            if SyntaxWrite().compareLoop(currentNode):
                nodeLoop = SyntaxWrite().getObjectArray(self.last[index], self.start)
                nodeBack = self.node_hash[nodeLoop]
                if nodeBack not in visitedArray:
                    visitedArray.append(nodeBack)
                    there_Element = self.node_for[nodeLoop] is not None
                    check_Element = self.node_for[nodeLoop] != currentNode
                    if there_Element and check_Element:
                        nodeNext = self.node_for[self.getReturnLoop(nodeLoop)]
                        self.provenance.edge(nodeBack, nodeNext, style='dashed')

    def get_Call_Back(self):
        """
        get the link back between the loop nodes
        dependencies: all, DefinitionProvenance class
        return: None
        """
        visitedArray = []
        for index in reversed(range(len(self.start))):
            currentNode = self.node_hash[index]
            if SyntaxWrite().compareLoop(currentNode):
                linkedBack = SyntaxWrite().getObjectArray(self.last[index], self.start)
                if linkedBack is not None and self.node_hash[linkedBack] not in visitedArray:
                    self.provenance.edge(self.node_hash[linkedBack], currentNode, style='dashed')
                    visitedArray.append(self.node_hash[linkedBack])
                else:
                    continue

    def edge_Back_in_Loops(self):
        def return_object(element):
            object: int = -1
            for index in range(len(self.start) - 1, -1, -1):
                if element == self.start[index]:
                    object = index
                    break
            return object

        for index, item in enumerate(self.node_hash):
            if SyntaxWrite().compareLoop(item):
                if self.last[index] in self.start:
                    index_loop = return_object(self.last[index])
                    for k in range(index, index_loop + 1):
                        self.node_for[k] = item

    def get_Last_Loop(self):
        for index, item in enumerate(self.node_hash):
            if SyntaxWrite().compareLoop(item):
                columnNode = self.column[index]
                check = False
                if self.last[index] in self.start:
                    lastNode = SyntaxWrite().getIndexArray(self.last[index], self.start)
                    if lastNode + 1 == len(self.node_hash):
                        lastNode -= 1
                    if columnNode == self.column[lastNode + 1]:
                        self.node_end_for[index] = self.node_hash[lastNode + 1]
                        self.provenance.edge(item, self.node_hash[lastNode + 1],
                                             label=" End Loop")
                        check = True
                        self.visited_x.append(self.node_hash[lastNode])
                        self.visited_y.append(self.node_hash[lastNode + 1])
                    else:
                        indexNode = lastNode
                        while True:
                            if indexNode == 0:
                                break
                            else:
                                if SyntaxWrite.compareLoop(self.node_hash[indexNode]):
                                    check_column = self.column[indexNode] < columnNode
                                    if check_column:
                                        self.provenance.edge(item, self.node_hash[indexNode],
                                                             label=" End Loop")
                                        check = True
                                        self.node_end_for[index] = self.node_hash[indexNode]
                                        break
                                indexNode = indexNode - 1

                   # print(check)

    def update_Sequences_IF_ELSE(self):
        """
        This method appends a string to nodes that will be
        ignored in the binding method.
        return: None
        """
        for key, node in enumerate(self.node_hash):
            if 'if' in node and self.node_else[key] is None:
                node_if = SyntaxWrite().getIndexArray(self.last[key], self.start)
                if 'else' in self.node_hash[node_if + 1]:
                    self.node_else[key] = '{}*'.format(self.node_else[node_if + 1])
                else:
                    self.node_else[key] = '{}*'.format(self.node_hash[node_if + 1])

    def edge_Definition_and_Calls(self):
        """
        This function is only enabled when there is a function in the script schema.
        Link function definition with their respective calls.
        return: None
        """
        for keyDef in self.defs:
           # self.provenance.node('start' + keyDef, 'Start', shape='Msquare')
           # self.provenance.edge('start' + keyDef, keyDef)
            for keyCall in self.call:
                nameDef = self.defs[keyDef][0]
                nameCall = self.call[keyCall][0]
                if nameCall.find(nameDef) != -1:
                    #self.provenance.edge(keyCall, 'start' + keyDef, style='dashed')
                    self.provenance.edge(keyCall, keyDef, style='dashed')

    def create_Elif_List(self):
        for index, node in enumerate(self.node_hash):
            if 'if' in node or 'elif' in node:
                id_node = index
                column = self.column[index]
                for k in range(index + 1, len(self.node_hash)):
                    if 'elif' in self.node_hash[k] and column == self.column[k]:
                        self.node_else[id_node] = self.node_hash[k]
                        if self.def_list[id_node] == None:
                            self.provenance.edge(node, self.node_hash[k], label=' False')
                        else:
                            if self.def_list[id_node] == self.def_list[k]:
                                self.provenance.edge(node, self.node_hash[k], label=' False')
                        break

    def create_Function_End_List(self):
        for i in range(0, len(self.node_hash)):
            if 'function_def' in self.node_hash[i]:
                end_index = SyntaxWrite().getIndexArray(self.last[i], self.start)
                self.def_function.append(self.node_hash[i])
                self.def_function_final.append(self.node_hash[end_index + 1])
                self.def_function_after.append(self.node_hash[end_index])

    def getPointCode(self):
        for index, node in enumerate(self.node_hash):
            if self.def_list[index] is None and 'start' not in node:
                self.provenance.edge('start', node)
                break

    def check_Try(self):
        for index, node in enumerate(self.node_hash):
            if 'try' in node:
                try_node = node
                try_column = self.column[index]
                try_final = self.last[index]
                for index2 in range(index + 1, len(self.node_hash)):
                    if try_final == self.start[index2]:
                        break
                    if 'exception' in self.node_hash[index2]:
                        if try_column == self.column[index2]:
                            self.try_except[try_node].append(self.node_hash[index2])
                    elif 'finally' in self.node_hash[index2]:
                        if try_column == self.column[index2]:
                            self.try_except[try_node].append(self.node_hash[index2])

        for key in self.try_except:
            count = len(self.try_except[key])
            check = False
            if count == 1:
                check = 'finally' in self.try_except[key][0]
            if count == 2:
                check = 'finally' in self.try_except[key][1]

            check_structure = False
            if check:
                element = self.node_hash.index(key)
                last = SyntaxWrite().getIndexArray(self.last[element], self.start)
                self.provenance.edge(key, self.try_except[key][1])

                if 'exception' in self.try_except[key][count - 2]:
                    check_structure = True
                    exception_node = self.try_except[key][count - 2]
                    element = self.node_hash.index(exception_node) - 1

                    self.provenance.edge(self.node_hash[element], self.try_except[key][1])
                    self.visited_x.append(self.node_hash[element])

            element = self.node_hash.index(key)
            last = SyntaxWrite().getIndexArray(self.last[element], self.start)
            self.provenance.edge(key, self.node_hash[last + 1], style='dashed')

            if check_structure:
                self.visited_y.append(self.node_hash[last + 1])

    def limited_Class(self):
        for index, node_class in enumerate(self.class_def_name):
            indexLast = SyntaxWrite().getIndexArray(self.last[index], self.start)

    def limited(self):
        for index, node in enumerate(self.node_hash):
            if 'function_def' in node:
                index_start = index
                index_final = SyntaxWrite().getIndexArray(self.last[index],
                                                          self.start)

                for j in range(index_start, index_final + 1):
                    self.def_list[j] = node

    def create_Hash_Code(self, x, y, z):
        return '{}{}{}'.format(x, y, z)

    def create_All_Nodes(self, rows, connecting):
        syntax = Nodes()
        map = HashingMapper()
        nodes = GraphDrawer(self.provenance)

        self.start_node()
        count_class = 0
        count_def = 0
        count_loop = 0
        count_if = 0
        count_try = 0

        for codes in rows:
            check = False
            startLine = codes[0]
            finalLine = codes[1]
            typesLine = codes[2]
            blockLine = codes[3]
            columLine = codes[4]
            nodesHash = self.create_Hash_Code(startLine,
                                              typesLine,
                                              finalLine)
            label = map.getElement('label',
                                   startLine,
                                   blockLine)
            if nodesHash not in self.node_hash:
                if typesLine in SyntaxWrite().getOthers():
                    check, self.provenance = nodes.assign(nodesHash, label)

                elif typesLine == 'class_def':
                    count_class = count_class + 1
                    self.class_def_name.append(blockLine)
                    self.class_def_start.append(startLine)
                    self.class_def_final.append(finalLine)

                elif SyntaxWrite().getCall(typesLine, blockLine):
                    self.call[nodesHash].append(blockLine)
                    check, self.provenance = nodes.calls(nodesHash, label)

                elif typesLine == 'import':
                    check, self.provenance = nodes.imports(nodesHash, label)

                elif typesLine == 'return':
                    check, self.provenance = nodes.calls(nodesHash, label)

                elif typesLine == 'function_def':
                    count_def = count_def + 1
                    self.defs[nodesHash].append(blockLine)
                    args = self.arguments_selection(connecting, startLine)
                    text = map.getElement('function', startLine, blockLine, args)
                    check, self.provenance = nodes.calls(nodesHash, text)

                elif typesLine in SyntaxWrite().getLoop():
                    count_loop = count_loop + 1
                    array = blockLine.split('\n')
                    condition = syntax.loops(typesLine, array[0])

                    text = map.getElement('label', startLine, typesLine)
                    check, self.provenance = nodes.loops(nodesHash, text, condition)

                elif typesLine == 'if':
                    count_if = count_if + 1
                    array = blockLine.split('\n')
                    if 'elif' in array[0]:
                        nodesHash = self.create_Hash_Code(startLine, 'elif', columLine)
                        text = map.getElement('label', startLine, 'elif')
                        check, self.provenance = nodes.condition(nodesHash, text,
                                                                 syntax.statementIf(array[0]))
                    else:
                        text = map.getElement('label', startLine, 'if')
                        check, self.provenance = nodes.condition(nodesHash, text,
                                                                 syntax.statementIf(array[0]))

                elif typesLine in SyntaxWrite().getTry() or blockLine == 'finally:':
                    count_try = count_try + 1
                    if typesLine == 'try':
                        text = map.getElement('label', startLine, 'try')
                        check, self.provenance = nodes.exceptions(nodesHash, text)

                    elif blockLine == 'finally:':
                        nodesHash = self.create_Hash_Code(startLine, 'finally', columLine)
                        text = map.getElement('label', startLine, 'finally')
                        check, self.provenance = nodes.calls(nodesHash, text)

                    elif typesLine == 'exception':
                        text = map.getElement('label', startLine, 'except')
                        check, self.provenance = nodes.exceptions(nodesHash, text)

                elif 'else:' == blockLine:
                    nodesHash = self.create_Hash_Code(startLine, 'else', columLine)
                    text = map.getElement('label', startLine, 'else')
                    check, self.provenance = nodes.calls(nodesHash, text)

                if check:
                    Dict = {str(columLine): nodesHash}
                    self.arrayHashing[startLine].append(Dict)
                    generic = '{}name{}'.format(startLine,
                                                columLine)
                    element = '{}{}'.format(startLine, columLine)
                    self.hash_index.append(int(element))
                    self.generic_hash.append(generic)
                    self.block.append(blockLine)
                    self.last.append(finalLine)
                    self.start.append(startLine)
                    self.column.append(columLine)
                    self.node_else.append(None)
                    self.node_if.append(None)
                    self.node_hash.append(nodesHash)
                    self.type.append(typesLine)

    def create_Function_List(self):
        self.def_list = [None for i in self.node_hash]
        self.limited()

    def create_Boxes_List(self):
        self.createBoxInClass()
        self.createBoxesInFunctions()

    def create_Array_List(self):
        self.class_list = ['Main' for i in self.node_hash]
        self.node_end_for = [None for i in self.node_hash]
        self.node_for = [None for i in self.node_hash]
        self.node_for_sup = [None for i in self.node_hash]
        self.singleIF = [None for i in self.node_hash]

    def create_Rules_List(self):
        self.syntaxRulesIF()
        self.syntaxRulesFOR()
        self.syntaxRulesTRY()

    def componentAnalyzer(self, sqlite, connecting, rows, data_set):
        self.create_All_Nodes(rows, connecting)
        self.create_Global_End_Node()
        self.format_column()

        self.create_Function_List()
        self.create_Boxes_List()
        self.create_Array_List()
        self.create_Rules_List()

        self.create_Function_End_List()
        self.edge_Definition_and_Calls()
        self.create_Elif_List()
        self.edge_Back_in_Loops()

        if data_set['activations_v'][0]:
            execution = ExecutionProvenance(self.trial,
                                            self.provenance,
                                            self.node_hash,
                                            self.start,
                                            data_set,
                                            sqlite,
                                            None,
                                            None,
                                            self.arrayHashing)

            execution.activations_provenance()

        if data_set['contents_v'][0]:
            execution = ExecutionProvenance(self.trial,
                                            self.provenance,
                                            self.node_hash,
                                            self.start,
                                            data_set,
                                            sqlite,
                                            self.column,
                                            self.generic_hash,
                                            self.arrayHashing)
            execution.contents_provenance()
        if data_set['checkpoints_v'][0]:
            execution = ExecutionProvenance(self.trial,
                                            self.provenance,
                                            self.node_hash,
                                            self.start,
                                            data_set,
                                            sqlite,
                                            self.column,
                                            self.generic_hash,
                                            self.arrayHashing)
            execution.runtime_provenance()

        self.getPointCode()
        if data_set['indented'][0]:
            self.indented_label()

        self.verify_function_check()
        self.show()
        self.linking_nodes_graph()
        self.provenance.view()
