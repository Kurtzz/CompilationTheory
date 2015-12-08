
class Node(object):
    def __str__(self):
        return self.printTree("")

    def accept(self, visitor):
        return visitor.visit(self)

    def __init__(self):
        self.children = ()


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
    def __init__(self, id, line):
        self.id = id
        self.line = line


class Blocks(Node):
    def __init__(self):
        self.children = []


class Declarations(Node):
    def __init__(self):
        self.children = []


class Declaration(Node):
    def __init__(self, type, inits):
        self.type = type
        self.inits = inits


class Inits(Node):
    def __init__(self):
        self.children = []


class Init(Node):
    def __init__(self, id, expression, line):
        self.id = id
        self.expression = expression
        self.line = line


class FunDef(Node):
    def __init__(self, type, id, args, body, line):
        self.type = type
        self.id = id
        self.args = args
        self.body = body
        self.line = line


class ArgList(Node):
    def __init__(self):
        self.children = []


class Arg(Node):
    def __init__(self, type, id, line):
        self.type = type
        self.id = id
        self.line = line


class Instructions(Node):
    def __init__(self):
        self.children = []


class Assignment(Node):
    def __init__(self, id, expression, line):
        self.id = id
        self.expression = expression
        self.line = line


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
        self.instructions = instructions
        self.condition = condition


class Return(Node):
    def __init__(self, expression, line):
        self.expression = expression
        self.line = line


class Continue(Node):
    def __init__(self, line):
        self.line = line


class Break(Node):
    def __init__(self, line):
        self.line = line


class CompoundInstruction(Node):
    def __init__(self, declarations, instructions):
        self.declarations = declarations
        self.instructions = instructions


class ExpressionList(Node):
    def __init__(self):
        self.children = []


class BinExpr(Node):
    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line


class FunCall(Node):
    def __init__(self, id, arglist, line):
        self.id = id
        self.arglist = arglist
        self.line = line
