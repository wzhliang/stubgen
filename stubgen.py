from __future__ import print_function
import sys
from pycparser import c_parser, c_ast, parse_file

def build_type(arg):
    """ Recursively explains a type decl node
    """
    typ = type(arg)

    if typ == c_ast.TypeDecl:
        quals = ' '.join(arg.quals) + ' ' if arg.quals else ''
        return quals + build_type(arg.type)
    elif typ == c_ast.Typename or typ == c_ast.Decl:
        return build_type(arg.type)
    elif typ == c_ast.IdentifierType:
        return ' '.join(arg.names)
    elif typ == c_ast.PtrDecl:
        quals = ' '.join(arg.quals) + ' ' if arg.quals else ''
        return quals + build_type(arg.type) + "*"
    elif typ == c_ast.ArrayDecl:
        arr = 'array'
        if arg.dim: arr += '[%s]' % arg.dim.value

        return arr + " of " + build_type(arg.type)

def print_return(node):
	# FIMXE: this doesn't handle complex return types
	ret = " ".join(node.type.type.type.names)
	if '*' in ret:
		print("    return NULL;")
	elif ret == 'void':
		print("    return;")
	else:
		print("    return 0;")

def print_func(node):
	print("%s " % " ".join(node.type.type.type.names), end='')
	print("%s(" % node.name, end='')
	args = []
	for p in node.type.args.params:
		args.append("%s %s" % (build_type(p), p.name))
	print("%s" % ", ".join(args), end='')
	print(")")
	print("{\n")
	print_return(node)
	print ("}\n")

def _print_func(node):
	print("name: %s" % node.name)
	print("return: %s" % " ".join(node.type.type.type.names))

def show_func_defs(filename):
	ast = parse_file(filename, use_cpp=True)
	for node in ast.ext:
		if type(node) is c_ast.Decl:
			print_func(node)


if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename  = sys.argv[1]
	else:
		print("Need a header file to work on.")

	show_func_defs(filename)
