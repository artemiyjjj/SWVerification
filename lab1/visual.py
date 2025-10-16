import ast
import pprint
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

def add_node(dot, node: ast.AST, parent=None, edge_name=""):
    global stack_of_scopes
    current_scope = stack_of_scopes[-1]
    node_name = str(node.__class__.__name__)
    parent_name = str(parent.__class__.__name__)
    node_attrs = []
    match node_name:
        case "Name":
            node_attrs.append("id: " + str(node.id))
        case "arg":
            node_attrs.append("arg: " + str(node.arg))
        case "Constant":
            node_attrs.append("value: " + str(node.value))
        case "FunctionDef":
            stack_of_scopes.append([])
            node_attrs.append("name: " + str(node.name))
            node_attrs.append("returns: " + str(node.returns))
        case "Assign" | "Expr" | "Break" | "Continue" | "Raise" | "Return" | "Yield" | "If" | "Try" | "ExceptHandler" | "For" | "While":
            if current_scope:
                dot.edge(str(id(current_scope[-1])), str(id(node)), color="red")
                current_scope.pop()
            current_scope.append(node)
        case _:
            pass
    dot.node(str(id(node)), node_name + "\n" + '\n'.join(node_attrs))
    if parent:
        dot.edge(str(id(parent)), str(id(node)), label=edge_name)
        if (parent_name == "If" or parent_name == "While") and edge_name == "orelse":
            dot.edge(str(id(parent)), str(id(node)), color="red")
    for name, item in ast.iter_fields(node):
        if isinstance(item, ast.AST):
            add_node(dot, item, node, name)
        elif isinstance(item, list):
            for child in item:
                if isinstance(child, ast.AST):
                    add_node(dot=dot, node=child, parent=node, edge_name=name)
    if node_name == "If":
        current_scope.append(node)
    elif node_name == "FunctionDef":
        stack_of_scopes.pop()

def read_programm(file: str) -> str:
    with open(file, "r") as f:
        return f.read()
    
def get_ast(text: str) -> ast.AST:
    return ast.parse(text, type_comments=True)

def visualise_ast(tree: ast.AST, outfilename: str):
    global stack_of_scopes
    dot = Digraph()
    stack_of_scopes = []
    stack_of_scopes.append([])
    add_node(dot, tree)
    dot.format="png"
    dot.render(outfilename, cleanup=True)

for file in files:
    print("===Making file " + file + "===")
    text = read_programm(file + ".py")
    tree = get_ast(text)
    # pprint.pprint(ast.dump(tree))
    visualise_ast(tree, "images/" + file)


