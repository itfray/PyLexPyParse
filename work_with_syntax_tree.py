from sparser.isparser import Node
from lexer.ilexer import ILexer
from sparser.sparser import SParser


def print_tokens_syntax_tree(parser: SParser, lexer: ILexer, root: Node, cnt_spcs=4):
    if root is None:
        return
    curr_cnt_spcs = 0
    nodes = []
    nodes.append((root, curr_cnt_spcs))
    while len(nodes) > 0:
        curr_node, curr_cnt_spcs = nodes.pop(0)
        childs = []
        for child in curr_node.childs:
            childs.append((child, curr_cnt_spcs + cnt_spcs))
        nodes = childs + nodes
        if not curr_node.value is None:
            token = curr_node.value
            spcs = f'{" ":^{curr_cnt_spcs}}'
            token_text = lexer.lexemes[token.kind][token.value]
            print(spcs + token_text)
        else:
            print(f'{" ":^{curr_cnt_spcs}}node : {parser.symbol(curr_node.kind)}')