import tkinter as tk
from enum import Enum
import re
import pandas
import pandastable as pt
from nltk.tree import *


class Token_type(Enum):  # listing all tokens type

    Implicit = 1
    End = 2
    DO = 3
    Else = 4
    COMMA = 5
    If = 6
    INTEGER = 7
    Dot = 8
    Semicolon = 9
    EqualOp = 10
    LessThanOp = 11
    GreaterThanOp = 12
    NotEqualOp = 13
    PlusOp = 14
    MinusOp = 15
    MultiplyOp = 16
    DivideOp = 17
    Identifier = 18
    Constant = 19
    Error = 20
    PROGRAM = 21
    NONE = 22
    REAL = 23
    COMPLEX = 24
    LOGICAL = 25
    CHARACTER = 26  # add brackets for length
    PARAMETER = 27
    SINGLECOLON = 28
    THEN = 29
    LEFTPARANTHESES = 30  # (
    LEN = 31
    RIGHTPARANTHESES = 32  # )
    DOUBLEQUOTATION = 33
    LESSTHANOREQUALOP = 34
    GREATERTHANOREQUAL = 35
    EQUALCOMP = 36
    SINGLEQUOTATION = 38
    READ = 39
    PRINT = 40
    TRUE = 41
    FALSE = 42
    COMMENTOP = 43
    NEWLINE = 44
    BLOCKNAME = 45
    LEFTBRACKET = 46  # [
    RIGHTBRACKET = 47  # ]
    # SPACE = 48  # ]
    COMMENTED = 49
    DOUBLECOLON = 50
    ENDIF = 51
    ENDDO = 52


# class token to hold string and token type
class token:
    def _init_(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type
        }


# Reserved word Dictionary
ReservedWords = {
    "PROGRAM": Token_type.PROGRAM,
    "IF": Token_type.If,
    "END": Token_type.End,
    "IMPLICIT": Token_type.Implicit,
    "NONE": Token_type.NONE,
    "DO": Token_type.DO,
    "ELSE": Token_type.Else,
    "INTEGER": Token_type.INTEGER,
    "REAL": Token_type.REAL,
    "PARAMETER": Token_type.PARAMETER,
    "COMPLEX": Token_type.COMPLEX,
    "THEN": Token_type.THEN,
    "CHARACTER": Token_type.CHARACTER,
    "READ": Token_type.READ,
    "PRINT": Token_type.PRINT,
    "LOGICAL": Token_type.LOGICAL,
    "TRUE": Token_type.TRUE,
    "FALSE": Token_type.FALSE,
    "\n": Token_type.NEWLINE,
    "ENDIF": Token_type.ENDIF,
    "ENDDO": Token_type.ENDDO
    # " ": Token_type.SPACE,
}
Operators = {".": Token_type.Dot,
             "=": Token_type.EqualOp,
             "+": Token_type.PlusOp,
             "-": Token_type.MinusOp,
             "*": Token_type.MultiplyOp,
             "/": Token_type.DivideOp,
             "<": Token_type.LessThanOp,
             ">": Token_type.GreaterThanOp,
             "(": Token_type.LEFTPARANTHESES,
             ")": Token_type.RIGHTPARANTHESES,
             "[": Token_type.LEFTBRACKET,
             "]": Token_type.RIGHTBRACKET,
             ",": Token_type.COMMA,
             "'": Token_type.SINGLEQUOTATION,
             "\"": Token_type.DOUBLEQUOTATION,
             ":": Token_type.SINGLECOLON,
             "==": Token_type.EQUALCOMP,
             "/=": Token_type.NotEqualOp,
             ">=": Token_type.GREATERTHANOREQUAL,
             "<=": Token_type.LESSTHANOREQUALOP,
             "::": Token_type.DOUBLECOLON
             }
Tokens = []
errors = []


def find_token(text):
    tokens = re.findall(r'\w+|[\=\+\-\*\/\<\>\(\)\{\}\'\"\n\:\[\]\,\!\." "]', text)
    print(tokens)
    i = 0
    """while i<len(tokens):
        if(tokens[i]=="="and tokens[i+1]=="="):
            Tokens.append(token(i, Token_type.EQUALCOMP))
            i+=1
        i+=1"""
    while i < len(tokens):
        if tokens[i] == " ":
            i = i + 1
            continue
        elif tokens[i] == "!":
            t = token()
            t.lex = str(tokens[i])
            t.token_type = Token_type.COMMENTOP
            Tokens.append(t)
            j = i + 1
            comments = ""
            while j < len(tokens):
                if tokens[j] != "\n":
                    comments += tokens[j]
                    j += 1
                else:
                    break
            i = j
            s = token()
            s.lex = comments
            s.token_type = Token_type.COMMENTED
            Tokens.append(s)

        elif str(tokens[i]).upper() in ReservedWords:
            if str(tokens[i]).upper() == "END" and i + 2 < len(tokens):
                if str(tokens[i + 2]).upper() == "IF":
                    t = token()
                    t.lex = "ENDIF"
                    t.token_type = Token_type.ENDIF
                    Tokens.append(t)
                    i = i + 2
                elif str(tokens[i + 2]).upper() == "DO":
                    t = token()
                    t.lex = "ENDDO"
                    t.token_type = Token_type.ENDDO
                    Tokens.append(t)
                    i = i + 2
                else:
                    t = token()
                    t.lex = str(tokens[i]).upper()
                    t.token_type = Token_type.End
                    Tokens.append(t)
            else:
                t = token()
                t.lex = str(tokens[i]).upper()
                t.token_type = ReservedWords[str(tokens[i]).upper()]
                Tokens.append(t)
        elif (re.match("^[a-zA-Z][a-zA-z0-9]*$", tokens[i])):
            t = token()
            t.lex = str(tokens[i]).upper()
            t.token_type = Token_type.Identifier
            Tokens.append(t)
        elif tokens[i] in Operators:
            if tokens[i] == "=" and i + 1 < len(tokens):
                if tokens[i + 1] == "=":
                    t = token()
                    t.lex = "=="
                    t.token_type = Operators["=="]
                    Tokens.append(t)
                    i = i + 1
                else:
                    t = token()
                    t.lex = "="
                    t.token_type = Operators["="]
                    Tokens.append(t)
            elif tokens[i] == "/" and i + 1 < len(tokens):
                if tokens[i + 1] == "=":
                    t = token()
                    t.lex = "/="
                    t.token_type = Operators["/="]
                    Tokens.append(t)
                    i = i + 1
                else:
                    t = token()
                    t.lex = "="
                    t.token_type = Operators["="]
                    Tokens.append(t)

            elif tokens[i] == "<" and i + 1 < len(tokens):
                if tokens[i + 1] == "=":
                    t = token()
                    t.lex = "<="
                    t.token_type = Operators["<="]
                    Tokens.append(t)
                    i = i + 1
                else:
                    t = token()
                    t.lex = "<"
                    t.token_type = Operators["<"]
                    Tokens.append(t)
            elif tokens[i] == ">" and i + 1 < len(tokens):
                if tokens[i + 1] == "=":
                    t = token()
                    t.lex = ">="
                    t.token_type = Operators[">="]
                    Tokens.append(t)
                    i = i + 1
                else:
                    t = token()
                    t.lex = ">"
                    t.token_type = Operators[">"]
                    Tokens.append(t)
            elif tokens[i] == ":" and i + 1 < len(tokens):
                if tokens[i + 1] == ":":
                    t = token()
                    t.lex = "::"
                    t.token_type = Operators["::"]
                    Tokens.append(t)
                    i = i + 1
                else:
                    t = token()
                    t.lex = ":"
                    t.token_type = Operators[":"]
                    Tokens.append(t)
            else:
                t = token()
                t.lex = str(tokens[i]).upper()
                t.token_type = Operators[tokens[i]]
                Tokens.append(t)
        elif re.match("([0-9]+)+(.[0-9]*)?", tokens[i]):
            t = token()
            t.lex = str(tokens[i]).upper()
            t.token_type = Token_type.Constant
            Tokens.append(t)
        else:
            t = token()
            t.lex = str(tokens[i]).upper()
            t.token_type = Token_type.Error
            Tokens.append(t)
            break
        i += 1


def Parse():
    j = 0
    Children = []
    Header_dict = Header(j)
    Children.append(Header_dict["node"])
    declsec_dict = DeclSec(Header_dict["index"])
    Children.append(declsec_dict["node"])
    Block_dict = Statements(declsec_dict["index"])
    Children.append(Block_dict["node"])

    # dic_output = Match(Token_type.Dot, Block_dict["index"])
    # # print(dic_output)
    end_dict = End(Block_dict["index"])
    Children.append(end_dict["node"])
    # Children.append(dic_output["node"])
    Node = Tree('Program', Children)

    return Node


def Header(j):
    children = []

    program_dict = Match(Token_type.PROGRAM, j)
    children.append(program_dict["node"])
    identify_dect = Match(Token_type.Identifier, program_dict["index"])
    children.append(identify_dect["node"])
    endline_dect = Endlines(identify_dect["index"])
    if not (endline_dect["node"] == ""):
        children.append(endline_dect["node"])
    Node = Tree('Header', children)
    out = dict()
    out["node"] = Node
    out["index"] = endline_dect['index']
    return out


def End(j):
    children = []
    end_dict = Match(Token_type.End, j)
    children.append(end_dict["node"])
    program_dict = Match(Token_type.PROGRAM, end_dict["index"])
    children.append(program_dict["node"])
    identifier_dict = Match(Token_type.Identifier, program_dict["index"])
    children.append(identifier_dict["node"])
    elines_dict = Elines(identifier_dict["index"])
    children.append(elines_dict["node"])
    Node = Tree('End', children)
    out = dict()
    out["node"] = Node
    out["index"] = elines_dict['index']
    return out


def Endlines(j):
    children = []
    endLineDash_dict = EndlineDash(j)
    children.append(endLineDash_dict["node"])
    elines_dict = Elines(endLineDash_dict["index"])
    if not (elines_dict["node"] == ""):
        children.append(elines_dict["node"])
    Node = Tree('newLine1', children)
    out = dict()
    out["node"] = Node
    out["index"] = elines_dict['index']
    return out


def Elines(j):
    children = []
    temp = Tokens[j].to_dict()
    if temp['token_type'] == Token_type.NEWLINE:
        endLineDash_dict = EndlineDash(j)
        children.append(endLineDash_dict["node"])
        elines_dict = Elines(endLineDash_dict["index"])
        if not (elines_dict["node"] == ""):
            children.append(elines_dict["node"])
        # children.append(elines_dict["node"])
        Node = Tree('newLine2', children)
        out = dict()
        out["node"] = Node
        out["index"] = elines_dict['index']
        return out
    else:
        out = dict()
        out["node"] = ""
        out["index"] = j
        return out


def EndlineDash(j):
    children = []

    newline = Match(Token_type.NEWLINE, j)
    children.append(newline["node"])
    Node = Tree('EndlineDash', children)
    out = dict()
    out["node"] = Node
    out["index"] = newline['index']
    return out


#
def DeclSec(j):
    Children = []
    implicit_dect = Match(Token_type.Implicit, j)
    Children.append(implicit_dect["node"])
    none_dect = Match(Token_type.NONE, implicit_dect["index"])
    Children.append(none_dect["node"])
    endline_dict = Endlines(none_dect["index"])
    Children.append(endline_dict["node"])
    Paramdecls_dict = ParamDecls(endline_dict["index"])
    if not (Paramdecls_dict["node"] == ""):
        Children.append(Paramdecls_dict["node"])
    Node = Tree('DeclSec', Children)
    out = dict()
    out["node"] = Node
    out["index"] = Paramdecls_dict['index']
    return out


def ParamDecls(j):
    children = []
    paramDecl_dict = ParamDecl(j)
    children.append(paramDecl_dict["node"])
    parDecls_dict = ParDecls(paramDecl_dict["index"])
    children.append(parDecls_dict["node"])
    Node = Tree('ParamDecls', children)
    out = dict()
    out["node"] = Node
    out["index"] = parDecls_dict['index']
    return out


def ParDecls(j):
    children = []
    temp = Tokens[j].to_dict()
    if temp['token_type'] == Token_type.NEWLINE:
        endlines_dict = Endlines(j)
        children.append(endlines_dict["node"])
        paramDecl_dict = ParamDecl(endlines_dict["index"])
        children.append(paramDecl_dict["node"])
        parDecls_dict = ParDecls(paramDecl_dict["index"])
        if not (parDecls_dict["node"] == ""):
            children.append(parDecls_dict["node"])
        Node = Tree('ParDecls', children)
        out = dict()
        out["node"] = Node
        out["index"] = parDecls_dict['index']
        return out
    else:
        out = dict()
        out["node"] = ""
        out["index"] = j
        return out


def ParamDecl(j):
    children = []
    dataType_dict = DataType(j)
    if not (dataType_dict["node"] == ""):
        children.append(dataType_dict["node"])
        children.append(dataType_dict["node"])
        parameter_dict = Parameter(dataType_dict["index"])
        children.append(parameter_dict["node"])
        doubleColon_dict = Match(Token_type.DOUBLECOLON, parameter_dict["index"])
        children.append(doubleColon_dict["node"])
        identify_dict = Match(Token_type.Identifier, doubleColon_dict["index"])
        children.append(identify_dict["node"])
        Node = Tree('ParamDecl', children)
        out = dict()
        out["node"] = Node
        out["index"] = identify_dict['index']
        return out
    else:
        out = dict()
        out["node"] = ""
        out["index"] = j
        return out



def Parameter(j):
    children = []

    temp = Tokens[j].to_dict()

    if temp['token_type'] == Token_type.COMMA:
        comma_dict = Match(Token_type.COMMA, j)
        children.append(comma_dict["node"])
        parameter_dict = Match(Token_type.PARAMETER, comma_dict["index"])
        children.append(parameter_dict["node"])
        equal_dict = Match(Token_type.EqualOp, parameter_dict["index"])
        children.append(equal_dict["node"])
        constant_dict = Match(Token_type.Constant, equal_dict["index"])
        children.append(constant_dict["node"])
        Node = Tree('Parameter', children)
        out = dict()
        out["node"] = Node
        out["index"] = constant_dict['index']
        return out
    else:
        out = dict()
        out["node"] = ""
        out["index"] = j
        return out


def DataType(j):
    children = []
    temp = Tokens[j].to_dict()

    if temp['token_type'] == Token_type.INTEGER:
        integer_dict = Match(Token_type.INTEGER, j)
        children.append(integer_dict["node"])
        Node = Tree('DataType', children)
        out = dict()
        out["node"] = Node
        out["index"] = integer_dict['index']
        return out

    elif temp['token_type'] == Token_type.COMPLEX:
        complex_dict = Match(Token_type.COMPLEX, j)
        children.append(complex_dict["node"])
        Node = Tree('DataType', children)
        out = dict()
        out["node"] = Node
        out["index"] = complex_dict['index']
        return out

    elif temp['token_type'] == Token_type.REAL:
        real_dict = Match(Token_type.REAL, j)
        children.append(real_dict["node"])
        Node = Tree('DataType', children)
        out = dict()
        out["node"] = Node
        out["index"] = real_dict['index']
        return out

    elif temp['token_type'] == Token_type.LOGICAL:
        logical_dict = Match(Token_type.LOGICAL, j)
        children.append(logical_dict["node"])
        Node = Tree('DataType', children)
        out = dict()
        out["node"] = Node
        out["index"] = logical_dict['index']
        return out

    elif temp['token_type'] == Token_type.CHARACTER:
        character_dict = CharacterFun(j)
        children.append(character_dict["node"])
        Node = Tree('DataType', children)
        out = dict()
        out["node"] = Node
        out["index"] = character_dict['index']
        return out
    else:
        out = dict()
        out["node"] = ""
        out["index"] = j
        return out


#
def CharacterFun(j):
    children = []
    character_dict = Match(Token_type.CHARACTER, j)
    children.append(character_dict["node"])
    leftpara_dict = Match(Token_type.LEFTPARANTHESES, character_dict["index"])
    children.append(leftpara_dict["node"])
    len_dict = Match(Token_type.LEN, leftpara_dict["index"])
    children.append(len_dict["node"])
    equal_dict = Match(Token_type.EqualOp, len_dict["index"])
    children.append(equal_dict["node"])
    constant_dict = Match(Token_type.Constant, equal_dict["index"])
    children.append(constant_dict["node"])
    rightPara_dict = Match(Token_type.RIGHTPARANTHESES, constant_dict["index"])
    children.append(rightPara_dict["node"])
    Node = Tree('Character', children)
    out = dict()
    out["node"] = Node
    out["index"] = rightPara_dict['index']
    return out


def Block(j):
    children = []
    temp = Tokens[j].to_dict()
    if temp['token_type'] == Token_type.NEWLINE:
        statements_dict = Statements(j)
        children.append(statements_dict["node"])
        if not (statements_dict["node"] == ""):
            children.append(statements_dict["node"])
        Node = Tree('Block', children)
        out = dict()
        out["node"] = Node
        out["index"] = statements_dict['index']
        return out
    else:
        out = dict()
        out["node"] = ""
        out["index"] = j
        return out


#
def Statements(j):
    children = []
    statement_dict = Statement(j)
    children.append(statement_dict["node"])
    state_dict = State(statement_dict["index"])
    children.append(state_dict["node"])
    Node = Tree('Statements', children)
    out = dict()
    out["node"] = Node
    out["index"] = state_dict['index']
    return out


def State(j):
    children = []
    temp = Tokens[j].to_dict()
    if temp['token_type'] == Token_type.NEWLINE:
        endlines_dict = Endlines(j)
        children.append(endlines_dict["node"])
        statement_dict = Statement(endlines_dict["index"])
        children.append(statement_dict["node"])
        state_dict = State(statement_dict["index"])
        if not (state_dict["node"] == ""):
            children.append(state_dict["node"])
        Node = Tree('State', children)
        out = dict()
        out["node"] = Node
        out["index"] = state_dict['index']
        return out
    else:
        out = dict()
        out["node"] = ""
        out["index"] = j
        return out


def Statement(j):
    children = []
    temp = Tokens[j].to_dict()

    if temp['token_type'] == Token_type.Identifier:
        assignment_dict = Assignment(j)
        children.append(assignment_dict["node"])
        Node = Tree('DataType', children)
        out = dict()
        out["node"] = Node
        out["index"] = assignment_dict['index']
        return out  #
    elif temp['token_type'] == Token_type.READ:
        read_dict = Read(j)
        children.append(read_dict["node"])
        Node = Tree('Statement', children)
        out = dict()
        out["node"] = Node
        out["index"] = read_dict['index']
        return out

    elif temp['token_type'] == Token_type.PRINT:
        print_dict = Print(j)
        children.append(print_dict["node"])
        Node = Tree('Statement', children)
        out = dict()
        out["node"] = Node
        out["index"] = print_dict['index']
        return out

    elif temp['token_type'] == Token_type.If:
        if_dict = ifStatement(j)
        children.append(if_dict["node"])
        Node = Tree('Statement', children)
        out = dict()
        out["node"] = Node
        out["index"] = if_dict['index']
        return out
    elif temp['token_type'] == Token_type.DO:
        do_dict = doStatement(j)
        children.append(do_dict["node"])
        Node = Tree('DataType', children)
        out = dict()
        out["node"] = Node
        out["index"] = do_dict['index']
        return out
    else:
        out = dict()
        out["node"] = ""
        out["index"] = j
        return out


def doStatement(j):
    children = []
    do_dict = Match(Token_type.DO, j)
    children.append(do_dict["node"])
    identifer_dict = Match(Token_type.Identifier, do_dict["index"])
    children.append(identifer_dict["node"])
    equal_dict = Match(Token_type.EqualOp, identifer_dict["index"])
    children.append(equal_dict["node"])
    factor1_dict = Factor(equal_dict["index"])
    children.append(factor1_dict["node"])
    comma_dict = Match(Token_type.COMMA, factor1_dict["index"])
    children.append(comma_dict["node"])
    factor2_dict = Factor(comma_dict["index"])
    children.append(factor2_dict["node"])
    step_dict = Step(factor2_dict["index"])
    children.append(step_dict["node"])

    endlines_dict = Endlines(step_dict["index"])
    children.append(endlines_dict["node"])

    statement_dict = Statement(endlines_dict["index"])
    children.append(statement_dict["node"])

    endlines1_dict = Elines(statement_dict["index"])
    children.append(endlines1_dict["node"])
    enddo_dict = Match(Token_type.ENDDO, endlines1_dict["index"])
    children.append(enddo_dict["node"])
    Node = Tree('Do Statement', children)
    out = dict()
    out["node"] = Node
    out["index"] = enddo_dict['index']
    return out


def Step(j):
    children = []
    temp = Tokens[j].to_dict()
    if temp['token_type'] == Token_type.COMMA:
        comma_dict = Match(Token_type.COMMA, j)
        children.append(comma_dict["node"])
        factor_dict = Factor(comma_dict["index"])
        children.append(factor_dict["node"])
        Node = Tree('Step', children)
        out = dict()
        out["node"] = Node
        out["index"] = factor_dict['index']
        return out
    else:
        out = dict()
        out["node"] = ""
        out["index"] = j
        return out


def Assignment(j):
    children = []

    identifer_dict = Match(Token_type.Identifier, j)
    children.append(identifer_dict["node"])
    equal_dict = Match(Token_type.EqualOp, identifer_dict["index"])
    children.append(equal_dict["node"])
    expression_dict = BooleanExpression(equal_dict["index"])
    children.append(expression_dict["node"])
    Node = Tree('Assignment', children)
    out = dict()
    out["node"] = Node
    out["index"] = expression_dict['index']
    return out


def Read(j):
    children = []

    read_dict = Match(Token_type.READ, j)
    children.append(read_dict["node"])
    star_dict = Match(Token_type.MultiplyOp, read_dict["index"])
    children.append(star_dict["node"])
    varDecls_dict = VarDecls(star_dict["index"])
    children.append(varDecls_dict["node"])
    Node = Tree('Read', children)
    out = dict()
    out["node"] = Node
    out["index"] = varDecls_dict['index']
    return out


def VarDecls(j):
    children = []
    varDecl_dict = VarDecl(j)
    children.append(varDecl_dict["node"])
    vdecls_dict = VDecls(varDecl_dict["index"])
    children.append(vdecls_dict["node"])
    Node = Tree('VarDecls', children)
    out = dict()
    out["node"] = Node
    out["index"] = vdecls_dict['index']
    return out


def VDecls(j):
    children = []
    temp = Tokens[j].to_dict()
    if temp['token_type'] == Token_type.COMMA:
        VarDecl_dict = VarDecl(j)
        children.append(VarDecl_dict["node"])
        VDecls_dict = VDecls(VarDecl_dict["index"])
        if not (VDecls_dict["node"] == ""):
            children.append(VDecls_dict["node"])
        Node = Tree('Vdecls', children)
        out = dict()
        out["node"] = Node
        out["index"] = VDecls_dict['index']
        return out
    else:
        out = dict()
        out["node"] = ""
        out["index"] = j
        return out


def VarDecl(j):
    children = []

    comma_dict = Match(Token_type.COMMA, j)
    children.append(comma_dict["node"])
    identify_dict = Match(Token_type.Identifier, comma_dict["index"])
    children.append(identify_dict["node"])
    Node = Tree('VarDecl', children)
    out = dict()
    out["node"] = Node
    out["index"] = identify_dict['index']
    return out


def Print(j):
    children = []

    print_dict = Match(Token_type.PRINT, j)
    children.append(print_dict["node"])
    star_dict = Match(Token_type.MultiplyOp, print_dict["index"])
    children.append(star_dict["node"])
    printDecls_dict = PrintDecls(star_dict["index"])
    children.append(printDecls_dict["node"])
    Node = Tree('Print', children)
    out = dict()
    out["node"] = Node
    out["index"] = printDecls_dict['index']
    return out


def PrintDecls(j):
    children = []
    printDecl_dict = PrintDecl(j)
    children.append(printDecl_dict["node"])
    pdecls_dict = PDecls(printDecl_dict["index"])
    children.append(pdecls_dict["node"])
    Node = Tree('PrintDecls', children)
    out = dict()
    out["node"] = Node
    out["index"] = pdecls_dict['index']
    return out


def PDecls(j):
    children = []
    temp = Tokens[j].to_dict()
    if temp['token_type'] == Token_type.COMMA:
        PrintDecl_dict = PrintDecl(j)
        children.append(PrintDecl_dict["node"])
        PDecls_dict = PDecls(PrintDecl_dict["index"])
        if not (PDecls_dict["node"] == ""):
            children.append(PDecls_dict["node"])
        Node = Tree('PDecls', children)
        out = dict()
        out["node"] = Node
        out["index"] = PDecls_dict['index']
        return out
    else:
        out = dict()
        out["node"] = ""
        out["index"] = j
        return out


def PrintDecl(j):
    children = []

    comma_dict = Match(Token_type.COMMA, j)
    children.append(comma_dict["node"])
    printable_dict = Printable(comma_dict["index"])
    children.append(printable_dict["node"])
    # identify_dict = Match(Token_type.Identifier, comma_dict["index"])
    # children.append(identify_dict["node"])
    Node = Tree('PrintDecl', children)
    out = dict()
    out["node"] = Node
    out["index"] = printable_dict['index']
    return out


def Printable(j):
    children = []
    temp = Tokens[j].to_dict()
    if temp['token_type'] == Token_type.Identifier:
        Identifier_dict = Match(Token_type.Identifier, j)
        if not (Identifier_dict["node"] == ""):
            children.append(Identifier_dict["node"])
        Node = Tree('Printable', children)
        out = dict()
        out["node"] = Node
        out["index"] = Identifier_dict['index']
        return out
    elif temp['token_type'] == Token_type.SINGLEQUOTATION:
        single_dict = Match(Token_type.SINGLEQUOTATION, j)
        if not (single_dict["node"] == ""):
            children.append(single_dict["node"])
        Node = Tree('Printable', children)
        out = dict()
        out["node"] = Node
        out["index"] = single_dict['index']
        return out
    else:
        out = dict()
        out["node"] = ""
        out["index"] = j
        return out


def ifStatement(j):
    children = []

    if_dict = Match(Token_type.If, j)
    children.append(if_dict["node"])
    condition_dict = Condition(if_dict["index"])
    children.append(condition_dict["node"])
    then_dict = Match(Token_type.THEN, condition_dict["index"])
    children.append(then_dict["node"])
    endlines_dict = Endlines(then_dict["index"])
    children.append(endlines_dict["node"])
    statements_dict = Statements(endlines_dict["index"])
    children.append(statements_dict["node"])
    endlines1_dict = Endlines(statements_dict["index"])
    children.append(endlines1_dict["node"])
    elseClause_dict = ElseClause(endlines1_dict["index"])
    children.append(elseClause_dict["node"])
    Node = Tree('ifStatement', children)
    out = dict()
    out["node"] = Node
    out["index"] = elseClause_dict['index']
    return out


#
#
#
def Condition(j):
    children = []

    left_par_dict = Match(Token_type.LEFTPARANTHESES, j)
    children.append(left_par_dict["node"])
    expression1 = BooleanTerm(left_par_dict["index"])
    children.append(expression1["node"])
    relational_dict = RelationalOp(expression1["index"])
    children.append(relational_dict["node"])
    expression2 = BooleanTerm(relational_dict["index"])
    children.append(expression2["node"])
    right_part_dict = Match(Token_type.RIGHTPARANTHESES, expression2["index"])
    children.append(right_part_dict["node"])
    Node = Tree('condition', children)
    out = dict()
    out["node"] = Node
    out["index"] = right_part_dict['index']
    return out


def ElseClause(j):
    children = []
    temp = Tokens[j].to_dict()
    if temp['token_type'] == Token_type.Else:
        else_dict = Match(Token_type.Else, j)
        children.append(else_dict["node"])
        statements_Dict = Statements(else_dict["index"])
        children.append(statements_Dict["node"])
        end_dict = Match(Token_type.ENDIF, statements_Dict["index"])
        if not (end_dict["node"] == ""):
            children.append(end_dict["node"])
        Node = Tree('ELSEClause', children)
        out = dict()
        out["node"] = Node
        out["index"] = end_dict['index']
        return out

    elif temp['token_type'] == Token_type.ENDIF:
        end_dict = Match(Token_type.ENDIF, j)
        if not (end_dict["node"] == ""):
            children.append(end_dict["node"])
        Node = Tree('ENDIF', children)
        out = dict()
        out["node"] = Node
        out["index"] = end_dict['index']
        return out
    else:
        out = dict()
        out["node"] = ""
        out["index"] = j
        return out


def ArthimeticOp(j):
    children = []
    temp = Tokens[j].to_dict()

    if temp['token_type'] == Token_type.MultiplyOp or temp['token_type'] == Token_type.DivideOp:
        mult_dict = MultOp(j)
        children.append(mult_dict["node"])
        Node = Tree('ArthimeticOp', children)
        out = dict()
        out["node"] = Node
        out["index"] = mult_dict['index']
        return out

    elif temp['token_type'] == Token_type.PlusOp or temp['token_type'] == Token_type.MinusOp:
        AddOp_dict = AddOp(j)
        children.append(AddOp_dict["node"])
        Node = Tree('ArthimeticOp', children)
        out = dict()
        out["node"] = Node
        out["index"] = AddOp_dict['index']
        return out


def RelationalOp(j):
    children = []
    temp = Tokens[j].to_dict()

    if temp['token_type'] == Token_type.GreaterThanOp or temp['token_type'] == Token_type.LessThanOp or temp[
        'token_type'] == Token_type.GREATERTHANOREQUAL or temp['token_type'] == Token_type.LESSTHANOREQUALOP:
        relOpdict = RelOp(j)
        children.append(relOpdict["node"])
        Node = Tree('RelationalOp', children)
        out = dict()
        out["node"] = Node
        out["index"] = relOpdict['index']
        return out

    elif temp['token_type'] == Token_type.EQUALCOMP or temp['token_type'] == Token_type.NotEqualOp:
        AddOp_dict = EquOp(j)
        children.append(AddOp_dict["node"])
        Node = Tree('RelationalOp', children)
        out = dict()
        out["node"] = Node
        out["index"] = AddOp_dict['index']
        return out


def Factor(j):
    children = []
    temp = Tokens[j].to_dict()

    if temp['token_type'] == Token_type.Identifier:
        Identifier_dict = Match(Token_type.Identifier, j)
        children.append(Identifier_dict["node"])
        Node = Tree('Identifier Factor', children)
        out = dict()
        out["node"] = Node
        out["index"] = Identifier_dict['index']
        return out
    elif temp['token_type'] == Token_type.Constant:
        Constant_dict = Match(Token_type.Constant, j)
        children.append(Constant_dict["node"])
        Node = Tree('Constant Factor', children)
        out = dict()
        out["node"] = Node
        out["index"] = Constant_dict['index']
        return out

    elif temp['token_type'] == Token_type.Dot:
        boolean_dict = Boolean(j)
        children.append(boolean_dict["node"])
        Node = Tree('Boolean Factor', children)
        out = dict()
        out["node"] = Node
        out["index"] = boolean_dict['index']
        return out
    elif temp['token_type'] == Token_type.LEFTPARANTHESES:
        left_dict = Match(Token_type.LEFTPARANTHESES, j)
        children.append(left_dict["node"])
        boolean_dict = BooleanExpression(left_dict["index"])
        children.append(boolean_dict["node"])
        right_dict = Match(Token_type.RIGHTPARANTHESES, boolean_dict["index"])
        children.append(right_dict["node"])
        Node = Tree('Boolean Factor', children)
        out = dict()
        out["node"] = Node
        out["index"] = right_dict['index']
        return out


##### EXPRESSION ######

def BooleanExpression(j):
    children = []
    booleanTerm_dict = BooleanTerm(j)
    children.append(booleanTerm_dict["node"])
    boolExp_dict = BoolExp(booleanTerm_dict["index"])
    children.append(boolExp_dict["node"])
    Node = Tree('BooleanExpression', children)
    out = dict()
    out["node"] = Node
    out["index"] = boolExp_dict['index']
    return out


def BoolExp(j):
    children = []
    temp = Tokens[j].to_dict()
    if temp['token_type'] == Token_type.Identifier or temp['token_type'] == Token_type.Constant or temp['token_type'] == Token_type.EQUALCOMP or temp['token_type'] == Token_type.NotEqualOp:
        equOp_dict = EquOp(j)
        children.append(equOp_dict["node"])
        booleanterm_dict = BooleanTerm(equOp_dict["index"])
        children.append(booleanterm_dict["node"])
        boolExp_dict = BoolExp(booleanterm_dict["index"])
        if not (boolExp_dict["node"] == ""):
            children.append(boolExp_dict["node"])
        Node = Tree('BoolExp', children)
        out = dict()
        out["node"] = Node
        out["index"] = boolExp_dict['index']
        return out
    else:
        out = dict()
        out["node"] = ""
        out["index"] = j
        return out


def BooleanTerm(j):
    children = []
    ArthimeticExpression_dict = ArthimeticExpression(j)
    children.append(ArthimeticExpression_dict["node"])
    BoolTer_dict = BoolTer(ArthimeticExpression_dict["index"])
    children.append(BoolTer_dict["node"])
    Node = Tree('BooleanTerm', children)
    out = dict()
    out["node"] = Node
    out["index"] = BoolTer_dict['index']
    return out


def BoolTer(j):
    children = []
    temp = Tokens[j].to_dict()
    if temp['token_type'] == Token_type.GreaterThanOp or temp['token_type'] == Token_type.LessThanOp or temp['token_type'] == Token_type.GREATERTHANOREQUAL or temp['token_type'] == Token_type.LESSTHANOREQUALOP:
        RelOp_dict = RelOp(j)
        children.append(RelOp_dict["node"])
        ArthimeticExpression_dict = ArthimeticExpression(RelOp_dict["index"])
        children.append(ArthimeticExpression_dict["node"])
        BoolTer_dict = BoolTer(ArthimeticExpression_dict["index"])
        if not (BoolTer_dict["node"] == ""):
            children.append(BoolTer_dict["node"])
        Node = Tree('BooleanTerm', children)
        out = dict()
        out["node"] = Node
        out["index"] = BoolTer_dict['index']
        return out
    else:
        out = dict()
        out["node"] = ""
        out["index"] = j
        return out


def ArthimeticExpression(j):
    children = []
    term_dict = Term(j)
    children.append(term_dict["node"])
    exp_dict = Exp(term_dict["index"])
    children.append(exp_dict["node"])
    Node = Tree('ArthimeticExpression', children)
    out = dict()
    out["node"] = Node
    out["index"] = exp_dict['index']
    return out

def Boolean(j):
    children = []
    dot1_dict = Match(Token_type.Dot, j)
    children.append(dot1_dict["node"])
    bool_dict = Bool(dot1_dict["index"])
    children.append(bool_dict["node"])
    dot2_dict = Match(Token_type.Dot, bool_dict["index"])
    children.append(dot2_dict["node"])
    Node = Tree('Boolean', children)
    out = dict()
    out["node"] = Node
    out["index"] = dot2_dict['index']
    return out

def Bool(j):
    children = []
    temp = Tokens[j].to_dict()
    if temp['token_type'] == Token_type.TRUE:
        true_dict = Match(Token_type.TRUE, j)
        children.append(true_dict["node"])
        Node = Tree('true_dict', children)
        out = dict()
        out["node"] = Node
        out["index"] = true_dict['index']
        return out
    elif temp['token_type'] == Token_type.FALSE:
        FALSE_dict = Match(Token_type.TRUE, j)
        children.append(FALSE_dict["node"])
        Node = Tree('FALSE_dict', children)
        out = dict()
        out["node"] = Node
        out["index"] = FALSE_dict['index']
        return out

def Exp(j):
    children = []
    temp = Tokens[j].to_dict()
    if temp['token_type'] == Token_type.PlusOp or temp['token_type'] == Token_type.MinusOp:
        addOp_dict = AddOp(j)
        children.append(addOp_dict["node"])
        term_dict = Term(addOp_dict["index"])
        children.append(term_dict["node"])
        exp_dict = Exp(term_dict["index"])
        if not (exp_dict["node"] == ""):
            children.append(exp_dict["node"])
        Node = Tree('ArthimeticExpression', children)
        out = dict()
        out["node"] = Node
        out["index"] = exp_dict['index']
        return out
    else:
        out = dict()
        out["node"] = ""
        out["index"] = j
        return out


def Term(j):
    children = []
    factor_dict = Factor(j)
    children.append(factor_dict["node"])
    ter_dict = Ter(factor_dict["index"])
    children.append(ter_dict["node"])
    Node = Tree('Term', children)
    out = dict()
    out["node"] = Node
    out["index"] = ter_dict['index']
    return out


def Ter(j):
    children = []
    temp = Tokens[j].to_dict()
    if temp['token_type'] == Token_type.MultiplyOp or temp['token_type'] == Token_type.MinusOp:
        MultOp_dict = MultOp(j)
        children.append(MultOp_dict["node"])
        factor_dict = Factor(MultOp_dict["index"])
        children.append(factor_dict["node"])
        ter_dict = Ter(factor_dict["index"])
        if not (ter_dict["node"] == ""):
            children.append(ter_dict["node"])
        Node = Tree('Ter', children)
        out = dict()
        out["node"] = Node
        out["index"] = ter_dict['index']
        return out
    else:
        out = dict()
        out["node"] = ""
        out["index"] = j
        return out


def AddOp(j):
    children = []
    temp = Tokens[j].to_dict()

    if temp['token_type'] == Token_type.PlusOp:
        plusop_dict = Match(Token_type.PlusOp, j)
        children.append(plusop_dict["node"])
        Node = Tree('AddOp', children)
        out = dict()
        out["node"] = Node
        out["index"] = plusop_dict['index']
        return out
    elif temp['token_type'] == Token_type.MinusOp:
        MinusOp_dict = Match(Token_type.MinusOp, j)
        children.append(MinusOp_dict["node"])
        Node = Tree('AddOp', children)
        out = dict()
        out["node"] = Node
        out["index"] = MinusOp_dict['index']
        return out



def MultOp(j):
    children = []
    temp = Tokens[j].to_dict()

    if temp['token_type'] == Token_type.MultiplyOp:
        MultiplyOp_dict = Match(Token_type.MultiplyOp, j)
        children.append(MultiplyOp_dict["node"])
        Node = Tree('MultOp', children)
        out = dict()
        out["node"] = Node
        out["index"] = MultiplyOp_dict['index']
        return out
    elif temp['token_type'] == Token_type.DivideOp:
        DivideOp_dict = Match(Token_type.DivideOp, j)
        children.append(DivideOp_dict["node"])
        Node = Tree('DivideOp', children)
        out = dict()
        out["node"] = Node
        out["index"] = DivideOp_dict['index']
        return out


def RelOp(j):
    children = []
    temp = Tokens[j].to_dict()

    if temp['token_type'] == Token_type.GreaterThanOp:
        GreaterThanOp_dict = Match(Token_type.GreaterThanOp, j)
        children.append(GreaterThanOp_dict["node"])
        Node = Tree('GreaterThanOp', children)
        out = dict()
        out["node"] = Node
        out["index"] = GreaterThanOp_dict['index']
        return out
    elif temp['token_type'] == Token_type.LessThanOp:
        LessThanOp_dict = Match(Token_type.LessThanOp, j)
        children.append(LessThanOp_dict["node"])
        Node = Tree('LessThanOp', children)
        out = dict()
        out["node"] = Node
        out["index"] = LessThanOp_dict['index']
        return out

    elif temp['token_type'] == Token_type.GREATERTHANOREQUAL:
        GREATERTHANOREQUALOp_dict = Match(Token_type.GREATERTHANOREQUAL, j)
        children.append(GREATERTHANOREQUALOp_dict["node"])
        Node = Tree('GREATERTHANOREQUAL', children)
        out = dict()
        out["node"] = Node
        out["index"] = GREATERTHANOREQUALOp_dict['index']
        return out
    elif temp['token_type'] == Token_type.LESSTHANOREQUALOP:
        LESSTHANOREQUALOP_dict = Match(Token_type.LESSTHANOREQUALOP, j)
        children.append(LESSTHANOREQUALOP_dict["node"])
        Node = Tree('LESSTHANOREQUALOP', children)
        out = dict()
        out["node"] = Node
        out["index"] = LESSTHANOREQUALOP_dict['index']
        return out


def EquOp(j):
    children = []
    temp = Tokens[j].to_dict()

    if temp['token_type'] == Token_type.EQUALCOMP:
        EqualCompt_dict = Match(Token_type.EQUALCOMP, j)
        children.append(EqualCompt_dict["node"])
        Node = Tree('EquOp', children)
        out = dict()
        out["node"] = Node
        out["index"] = EqualCompt_dict['index']
        return out
    elif temp['token_type'] == Token_type.NotEqualOp:
        NotEqualOp_dict = Match(Token_type.NotEqualOp, j)
        children.append(NotEqualOp_dict["node"])
        Node = Tree('NotEquoOp', children)
        out = dict()
        out["node"] = Node
        out["index"] = NotEqualOp_dict['index']
        return out


def Match(a, j):
    output = dict()
    if j < len(Tokens):
        Temp = Tokens[j].to_dict()
        if Temp['token_type'] == a:
            j += 1
            output["node"] = [Temp['Lex']]
            output["index"] = j
            return output
        else:
            output["node"] = ["error"]
            output["index"] = j
            errors.append("Syntax error : " + Temp['Lex'] + " invalid token")
            return output
    else:
        output["node"] = ["j out of range error"]
        output["index"] = j
        return output


# GUI
root = tk.Tk()

canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Scanner Phase')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Source code:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)


def Scan():
    filename = 'file.txt'  # replace with your input file name
    with open(filename, 'r') as f:
        x1 = f.read()
        find_token(x1)
        df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
    # print(df)

    # to display token stream as table
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()
    # start Parsing
    Node = Parse()

    # to display errorlist
    df1 = pandas.DataFrame(errors)
    dTDa2 = tk.Toplevel()
    dTDa2.title('Error List')
    dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    dTDaPT2.show()
    Node.draw()
    # clear your list

    # label3 = tk.Label(root, text='Lexem ' + x1 + ' is:', font=('helvetica', 10))
    # canvas1.create_window(200, 210, window=label3)

    # label4 = tk.Label(root, text="Token_type"+x1, font=('helvetica', 10, 'bold'))
    # canvas1.create_window(200, 230, window=label4)


button1 = tk.Button(text='Scan', command=Scan, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)
root.mainloop()
