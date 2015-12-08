#!/usr/bin/python

import AST
from SymbolTable import *
from collections import defaultdict

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
for op in ['+', '-', '*', '/', '%', '<', '>', '<<', '>>', '|', '&', '^', '<=', '>=', '==', '!=']:
    ttype[op]['int']['int'] = 'int'

for op in ['+', '-', '*', '/']:
    ttype[op]['int']['float'] = 'float'
    ttype[op]['float']['int'] = 'float'
    ttype[op]['float']['float'] = 'float'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['int']['float'] = 'int'
    ttype[op]['float']['int'] = 'int'
    ttype[op]['float']['float'] = 'int'

ttype['+']['string']['string'] = 'string'
ttype['*']['string']['int'] = 'string'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['string']['string'] = 'int'


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.table = SymbolTable(None, "root")
        self.currentType = ""
        self.currentFun = None
        self.isInLoop = False

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Variable(self, node):
        definition = self.table.getGlobal(node.id)
        if definition is None:
            raise MyException("Error: Usage of undeclared variable '{}': line {}".format(node.id, node.line))
        else:
            return definition.type

    def visit_Declaration(self, node):
        self.currentType = node.type
        self.visit(node.inits)
        self.currentType = ""

    def visit_Init(self, node):
        exprType = self.visit(node.expression)
        if (self.currentType == exprType) or (self.currentType == "int" and exprType == "float") or (self.currentType == "float" and exprType == "int"):
            if self.table.get(node.id) is not None:
                raise MyException("Error: Variable '{}' already declared: line {}".format(node.id, node.line))
            else:
                self.table.put(node.id, VariableSymbol(node.id, self.currentType))
        else:
            raise MyException("Error: Assignment of '{}' to '{}': line {}".format(exprType, self.currentType, node.line))


    def visit_FunDef(self, node):
        if self.table.get(node.id) is not None:
            raise MyException("Error: Redefinition of function '{}': line {}".format(node.id, node.line))
        else:
            function = FunctionSymbol(node.type, node.id, SymbolTable(self.table, node.id))
            self.table.put(node.id, function)
            self.table = function.symbolTable
            self.currentFun = function
            if node.args is not None:
                self.visit(node.args)
            function.extractParams()
            self.visit(node.body)
            self.table = self.table.getParentScope()
            self.currentFun = None

    def visit_Arg(self, node):
        if self.table.get(node.id) is not None:
            raise MyException("Error: Variable '{}' already declared: line {}".format(node.id, node.line))
        else:
            self.table.put(node.id, VariableSymbol(node.id, node.type))

    def visit_Assignment(self, node):
        declaration = self.table.getGlobal(node.id)
        exprType = self.visit(node.expression)
        if declaration is None:
            raise MyException("Error: Variable '{}' undefined in current scope: line {}".format(node.id, node.line))
        elif declaration.type == "int" and exprType == "float":
            print "Warning: Assignment of '{}' to '{}' may cause loss of precision: line {}".format(exprType, declaration.type, node.line)
        elif declaration.type == "float" and exprType == "int":
            pass
        elif exprType != declaration.type:
            raise MyException("Error: Assignment of '{}' to '{}': line {}". format(exprType, declaration.type, node.line))

    def visit_InstructionPrint(self, node):
        self.visit(node.expression)

    def visit_InstructionIf(self, node):
        self.visit(node.condition)
        self.visit(node.instructionIf)
        if node.instructionElse is not None:
            self.visit(node.instructionElse)

    def visit_InstructionWhile(self, node):
        innerLoop = False
        if self.isInLoop:
            innerLoop = True
        self.visit(node.condition)
        self.isInLoop = True
        self.visit(node.instruction)
        if not innerLoop:
            self.isInLoop = False

    def visit_Repeat(self, node):
        innerLoop = False
        if self.isInLoop:
            innerLoop = True
        self.isInLoop = True
        self.visit(node.instructions)
        self.visit(node.condition)
        if not innerLoop:
            self.isInLoop = False

    def visit_Return(self, node):
        if self.currentFun is None:
            raise MyException("Error: return instruction outside a function: line {}".format(node.line))
        else:
            retType = self.visit(node.expression)
            if retType != self.currentFun.type and (self.currentFun.type != "float" or retType != "int"):
                raise MyException("Error: Improper returned type, expected {}, got {}: line {}".format(self.currentFun.type, retType, node.line))

    def visit_Continue(self, node):
        if not self.isInLoop:
            raise MyException("Error: continue instruction outside a loop: line {}".format(node.line))

    def visit_Break(self, node):
        if not self.isInLoop:
            raise MyException("Error: break instruction outside a loop: line {}".format(node.line))

    def visit_CompoundInstruction(self, node):
        innerScope = SymbolTable(self.table, "innerScope")
        self.table = innerScope
        if node.declarations is not None:
            self.visit(node.declarations)
        self.visit(node.instructions)
        self.table = self.table.getParentScope()

    def visit_Expression(self):
        pass

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        result = ttype[op][type1][type2]
        if result is None:
            raise MyException("Error: Illegal operation, '{} {} {}': line {}".format(type1, op, type2, node.line))
        return result


    def visit_FunCall(self, node):
        funDef = self.table.getGlobal(node.id)
        if funDef is None or not isinstance(funDef, FunctionSymbol):
            raise MyException("Error: Call of undefined fun: '{}': line {}".format(node.id, node.line))
        else:
            if len(node.arglist.children) != len(funDef.params):
                raise MyException("Error: Improper number of args in '{}' call: line {}".format(funDef.id, node.line))
            else:
                types = [self.visit(x) for x in node.arglist.children]
                expectedTypes = funDef.params
                for actual, expected in zip(types, expectedTypes):
                    if actual != expected and not (actual == "int" and expected == "float"):
                        raise MyException("Error: Improper type of args in {} call: line {}".format(node.id, node.line))
            return funDef.type


class MyException(Exception):
    def __init__(self, error):
        self.error = error