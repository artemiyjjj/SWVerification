import ast
import copy
# import pprint
from graphviz import Digraph

files = {
    "comment",
    "for",
    "func",
    "if",
    "strings",
    "structs",
    "switch",
    "try",
    "while"
}

# files = {"try"}

def add_node(dot, node: ast.AST, parent=None, edge_name="", parent_attrs_func=None):
    global stack_of_scopes
    current_scope = stack_of_scopes[-1]
    node_name = str(node.__class__.__name__)
    parent_name = str(parent.__class__.__name__)
    node_attrs = []
    elsebranch = None
    finalbranch = None

    try:
        elsebranch = getattr(node, "orelse")
    except AttributeError:
        pass
    try:
        finalbranch = getattr(node, "finalbody")
    except AttributeError:
        pass

    def get_node_attrs():
        nonlocal node_attrs
        return node_attrs

    print("IN " + node_name + " " + ast.unparse(node))
    match node_name:
        # Add node's info to their parent node
        case "Name":
            parent_attrs_func().append(edge_name + ": " + str(node.id))
            return
        case "And" | "Eq" | "NotEq" |  "Or" | "Not" | "Lt" | "LtE" | "Gt" | "GtE" | \
             "Add" | "Div" | "Sub" | "Mult" | "FloorDiv" | "Mod" | "Pow" | "LShift" | "RShift" | \
             "BitOr" | "BitXor" | "BitAnd" | "MatMult" | "Is" | "IsNot" | "In" | "NotIn":
            parent_attrs_func().append(edge_name + ": " + str(node.__class__.__name__))
            return
        # Add node attributes
        case "arg":
            node_attrs.append("arg: " + str(node.arg))
        case "Constant":
            node_attrs.append("value: " + str(node.value))
        # Add function context to make it independent from main execution and other functions
        case "FunctionDef":
            stack_of_scopes.append([node])
            node_attrs.append("name: " + str(node.name))
            node_attrs.append("returns: " + str(node.returns))
        case "Assign" | "Call" | "Expr" | "Break" | "Pass" | "Continue" | "Raise" | "Return" | "Yield" | "If" | "Try" | "ExceptHandler" | "For" | "While" | \
             "BinOp" | "UnaryOp" | "BoolOp" | "IfExp":
            if ((node_name == "If" and parent_name != "If") or node_name == "Try") and len(current_scope) >= 1:
                for elem in current_scope:
                    dot.edge(str(id(elem)), str(id(node)), color="red")
                current_scope.clear()
            if node_name == "If" or node_name == "ExceptHandler" or edge_name == "orelse":
                stack_of_scopes.append(copy.copy(current_scope))
                current_scope = stack_of_scopes[-1]
            elif node_name == "Try":
                # Create second scope for handlers
                stack_of_scopes.append(copy.copy(current_scope))
                stack_of_scopes.append(copy.copy(current_scope))
                current_scope = stack_of_scopes[-1]
            # elif node_name == "ExceptHandler":
                # current_scope = stack_of_scopes[-2]
            if (parent_name == "If" and edge_name == "orelse"):
                # Remove connection with expression from previous if node or handlers edge
                current_scope.pop()
                current_scope.append(parent)
            # elif  parent_name == "Try" and (edge_name == "handlers" or edge_name == "orelse") and len(current_scope) > 1:
            #     # Remove connection with previous handlers edge
            #     current_scope.pop()
            if len(current_scope) >= 1:
                # !!! сюда же try, except
                for elem in current_scope:
                    dot.edge(str(id(elem)), str(id(node)), color="red")
                current_scope.clear()
            current_scope.append(node)
        # Remove excessive node types
        case "Load" | "Store":
            return
        case _:
            pass
    
    if parent:
        dot.edge(str(id(parent)), str(id(node)), label=edge_name)
    # Then moving to children
    for name, item in ast.iter_fields(node):
        if isinstance(item, ast.AST):
            add_node(dot, item, node, name, get_node_attrs)
        elif isinstance(item, list):
            for child in item:
                if isinstance(child, ast.AST):
                    add_node(dot=dot, node=child, parent=node, edge_name=name, parent_attrs_func=get_node_attrs)
    # Then returning to parent, moving to siblings
    if node_name == "FunctionDef":
        stack_of_scopes.pop()
    # Works or try.orelse too
    elif node_name == "If" or node_name == "Try" or edge_name == "orelse":
        forward_list = stack_of_scopes.pop()
        # Add connection from if node to siblings if it has no orelse attr
        if (node_name == "If") and edge_name != "orelse" and not elsebranch:
                forward_list.append(node)
        try:
            stack_of_scopes[-1].extend(forward_list)
        except IndexError:
            stack_of_scopes.append(forward_list)
    elif node_name == "ExceptHandler":
        forward_list = stack_of_scopes.pop()
        # Choose scope for handlers
        stack_of_scopes[-2].extend(forward_list)
    elif parent_name == "If" and edge_name == "test":
        current_scope.pop()
        current_scope.append(parent)
    if parent_name == "Try" and edge_name == "orelse":
        # handlers_scope = stack_of_scopes.pop()
        body_scope = stack_of_scopes.pop()
        # stack_of_scopes[-1].extend(handlers_scope)
        stack_of_scopes[-1].extend(body_scope)
    dot.node(str(id(node)), node_name + "\n" + '\n'.join(node_attrs))

def read_programm(file: str) -> str:
    with open(file, "r") as f:
        return f.read()
    
def get_ast(text: str) -> ast.AST:
    return ast.parse(text, type_comments=True)

def visualise_ast(tree: ast.AST, outfilename: str):
    global stack_of_scopes
    dot = Digraph()
    stack_of_scopes = [[]]
    # stack_of_scopes.append([])
    add_node(dot, tree)
    dot.format="png"
    dot.render(outfilename, cleanup=True)

for file in files:
    print("===Making file " + file + "===")
    text = read_programm(file + ".py")
    tree = get_ast(text)
    # pprint.pprint(ast.dump(tree))
    visualise_ast(tree, "images/" + file)
