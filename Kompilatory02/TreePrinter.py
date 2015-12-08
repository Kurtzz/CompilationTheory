
import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Const)
    def printTree(self, depth):
        return depth + str(self.value) + "\n"

    @addToClass(AST.Variable)
    def printTree(self, depth):
        return depth + str(self.id) + "\n"

    @addToClass(AST.Blocks)
    def printTree(self, depth):
        res = ""
        for block in self.blocks:
            res += block.printTree(depth)
        return res

    @addToClass(AST.Declarations)
    def printTree(self, depth):
        res = ""
        for decl in self.declarations:
            res += decl.printTree(depth + "| ")
        return res

    @addToClass(AST.Declaration)
    def printTree(self, depth):
        return depth + "DECL\n" + self.inits.printTree(depth + "| ")

    @addToClass(AST.Inits)
    def printTree(self, depth):
        res = ""
        for init in self.inits:
            res += init.printTree(depth)
        return res

    @addToClass(AST.Init)
    def printTree(self, depth):
        res = depth + "=\n"
        res += depth + "| " + str(self.id) + "\n"
        res += self.expression.printTree(depth + "| ")
        return res

    @addToClass(AST.FunDef)
    def printTree(self, depth):
        res = depth + "FUNDEF\n"
        depth += "| "
        res += depth + str(self.id) + "\n"
        res += depth + "RET " + str(self.type) + "\n"
        res += self.args.printTree(depth)
        res += self.body.printTree(depth)
        return res

    @addToClass(AST.ArgList)
    def printTree(self, depth):
        res = ""
        for arg in self.arglist:
            res += arg.printTree(depth)
        return res

    @addToClass(AST.Arg)
    def printTree(self, depth):
        return depth + "ARG " + str(self.type) + " " + str(self.id) + "\n"

    @addToClass(AST.Assignment)
    def printTree(self, depth):
        res = depth + "=\n"
        res += depth + "| " + str(self.id) + "\n"
        res += self.expression.printTree(depth + "| ")
        return res

    @addToClass(AST.Instructions)
    def printTree(self, depth):
        res = ""
        for instr in self.instructions:
            res += instr.printTree(depth)
        return res

    @addToClass(AST.InstructionPrint)
    def printTree(self, depth):
        res = depth + "PRINT\n"
        res += self.expression.printTree(depth + "| ")
        return res

    @addToClass(AST.InstructionIf)
    def printTree(self, depth):
        res = depth + "IF\n"
        res += self.condition.printTree(depth + "| ")
        res += self.instructionIf.printTree(depth + "| ")
        if self.instructionElse is not None:
            res += depth + "ELSE\n"
            res += self.instructionElse.printTree(depth + "| ")
        return res

    @addToClass(AST.InstructionWhile)
    def printTree(self, depth):
        res = depth + "WHILE\n"
        res += self.condition.printTree(depth + "| ")
        res += self.instruction.printTree(depth + "| ")
        return res

    @addToClass(AST.Repeat)
    def printTree(self, depth):
        res = depth + "REPEAT\n"
        res += self.instructions.printTree(depth + "| ")
        res += depth + "UNTIL\n"
        res += self.condition.printTree(depth + "| ")
        return res

    @addToClass(AST.Return)
    def printTree(self, depth):
        res = depth + "RETURN\n"
        res += self.expression.printTree(depth + "| ")
        return res

    @addToClass(AST.Continue)
    def printTree(self, depth):
        return depth + "CONTINUE\n"

    @addToClass(AST.Break)
    def printTree(self, depth):
        return depth + "BREAK\n"

    @addToClass(AST.CompoundInstruction)
    def printTree(self, depth):
        res = ""
        if self.declarations is not None:
            res += self.declarations.printTree(depth + "| ")
        res += self.instructions.printTree(depth + "| ")
        return res

    @addToClass(AST.BinExpr)
    def printTree(self, depth):
        res = depth + str(self.op) + "\n"
        res += self.left.printTree(depth + "| ")
        res += self.right.printTree(depth + "| ")
        return res

    @addToClass(AST.ExpressionList)
    def printTree(self, depth):
        res = ""
        for expr in self.expressionList:
            res += expr.printTree(depth)
        return res

    @addToClass(AST.FunCall)
    def printTree(self, depth):
        res = depth + "FUNCALL\n"
        res += depth + "| " + str(self.id) + "\n"
        res += self.arglist.printTree(depth + "| ")
        return res
