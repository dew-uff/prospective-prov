class HashingMapper(object):
    def __init__(self):
        """
        :rtype: object
        """
        pass

    def getElement(self, *args):
        """
        :param args: args[1]: line, line start of code block
                     args[2]: type, type of code block
                     args[3]: arguments, arguments in function
        :return: return Object
        """
        if args[0] == 'hashing':
            return self.getHashing(args[1], args[2], args[3])
        if args[0] == 'label':
            return self.getLabel(args[1], args[2])
        if args[0] == 'function':
            return self.getLabelFunction(args[1], args[2], args[3])

    @staticmethod
    def getHashing(line: int, types: str, block: str) -> object:
        """
        :param line: start line of this block code
        :param types: node classification (loop, condition, variable, ...)
        :param block: block of code on a specific line
        :return:
        """
        return '{}{}{}'.format(line, types, block)

    @staticmethod
    def getLabelFunction(line: int, block: str, arguments: str) -> object:
        """
        :param line: start line of this block code
        :param block: block of code on a specific line
        :param arguments: arguments of a function
        :return:
        """
        return '{}: def {}({})'.format(line, block, arguments)

    @staticmethod
    def getLabel(line: int, block: str) -> object:
        """
        :param line: start line of this block code
        :param block: block of code on a specific line
        :return:
        """
        return '{}: {}'.format(line, block)
