class OperatorType(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __str__(self):
        return self.name


class OperatorExpression(object):
    def __init__(self, operand):
        self._operand = operand

    def operand(self):
        return self._operand


class Literal(object):
    def __init__(self, value, literal_type):
        self.value = value
        self.type = literal_type
