
class Node(object):
    def __str__(self):
        return self.printTree("")


class Const(Node):
    def __init__(self, value):
        self.value = value


class Integer(Const):
    pass


class Float(Const):
    pass


class String(Const):
    pass


class Variable(Node):
    def __init__(self, id):
        self.id = id


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Blocks(Node):
    def __init__(self):
        self.blocks = []


class Declarations(Node):
    def __init__(self):
        self.declarations = []


class Declaration(Node):
    def __init__(self, type, inits):
        self.type = type
        self.inits = inits


class Inits(Node):
    def __init__(self):
        self.inits = []


class Init(Node):
    def __init__(self, id, expression):
        self.id = id
        self.expression = expression


class FunDef(Node):
    def __init__(self, type, id, args, body):
        self.type = type
        self.id = id
        self.args = args
        self.body = body


class ArgList(Node):
    def __init__(self):
        self.arglist = []


class Arg(Node):
    def __init__(self, type, id):
        self.type = type
        self.id = id

class Assignment(Node):
    def __init__(self, id, expression):
        self.id = id
        self.expression = expression

class Instructions(Node):
    def __init__(self):
        self.instructions = []


class InstructionPrint(Node):
    def __init__(self, expression):
        self.expression = expression


class InstructionIf(Node):
    def __init__(self, condition, instructionIf, instructionElse=None):
        self.condition = condition
        self.instructionIf = instructionIf
        self.instructionElse = instructionElse


class InstructionWhile(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class Repeat(Node):
    def __init__(self, instructions, condition):
        self.condition = condition
        self.instructions = instructions


class Return(Node):
    def __init__(self, expression):
        self.expression = expression


class Continue(Node):
    pass


class Break(Node):
    pass


class CompoundInstruction(Node):
    def __init__(self, declarations, instructions):
        self.declarations = declarations
        self.instructions = instructions


class ExpressionList(Node):
    def __init__(self):
        self.expressionList = []

class FunCall(Node):
    def __init__(self, id, arglist):
        self.id = id
        self.arglist = arglist

