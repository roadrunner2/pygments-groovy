# -*- coding: utf-8 -*-
"""
    Lexer for the Groovy programming language
    http://groovy.codehaus.org
"""

import re
from pygments.lexer import RegexLexer, bygroups, using, this
from pygments.token import \
     Text, Comment, Operator, Keyword, Name, String, Number

class GroovyLexer(RegexLexer):
    """
    For `Groovy <http://groovy.codehaus.org/>`_ source code.
    """

    name = 'Groovy'
    aliases = ['groovy']
    filenames = ['*.groovy']
    mimetypes = ['text/x-groovy']

    flags = re.MULTILINE | re.DOTALL

    #: optional Comment or Whitespace
    _ws = r'(?:\s|//.*?\n|/[*].*?[*]/)+'

    tokens = {
        'root': [
            # method names
            (r'^(\s*(?:[a-zA-Z_][a-zA-Z0-9_\.\[\]]*\s+)+?)' # return arguments
             r'([a-zA-Z_][a-zA-Z0-9_]*)'                    # method name
             r'(\s*)(\()',                                  # signature start
             bygroups(using(this), Name.Function, Text, Operator)),
            (r'[^\S\n]+', Text),
            (r'//.*?\n', Comment),
            (r'/\*.*?\*/', Comment),
            (r'@[a-zA-Z_][a-zA-Z0-9_\.]*', Name.Decorator),
            (r'(assert|break|case|catch|continue|default|else|finally|for|'
             r'if|instanceof|new|return|switch|this|throw|try|while)\b',
             Keyword),      # 'in' is not included because of its limited scope
            (r'(abstract|enum|extends|final|implements|native|private|'
             r'protected|public|static|super|synchronized|threadsafe|throws|'
             r'transient|volatile)\b', Keyword.Declaration),
            (r'(const|do|goto|strictfp)\b', Keyword.Reserved),
            (r'(def|boolean|byte|char|double|float|int|long|short|void)\b',
             Keyword.Type),
            (r'(package)(\s+)', bygroups(Keyword.Namespace, Text)),
            (r'(true|false|null)\b', Keyword.Constant),
            (r'(class|interface)(\s+)', bygroups(Keyword.Declaration, Text), 'class'),
            (r'(import)(\s+)', bygroups(Keyword.Namespace, Text), 'import'),
            (r'"(\\\\|\\"|[^"])*"', String),
            (r"'\\.'|'[^\\]'|'\\u[0-9a-f]{4}'", String.Char),
            (r'(\.)([a-zA-Z_][a-zA-Z0-9_]*)', bygroups(Operator, Name.Attribute)),
            (r'[a-zA-Z_][a-zA-Z0-9_]*:', Name.Label),
            (r'[a-zA-Z_\$][a-zA-Z0-9_]*', Name),
            (r'[~\^\*!%&\[\]\(\)\{\}<>\|+=:;,./?-]', Operator),
            (r'[0-9][0-9]*\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
            (r'0x[0-9a-f]+', Number.Hex),
            (r'[0-9]+[lL]', Number.Integer.Long),
            (r'[0-9]+', Number.Integer),
            (r'\\[0-3]?[0-7]{1,2}', Number.Oct),
            (r'\n', Text)
        ],
        'class': [
            (r'[a-zA-Z_][a-zA-Z0-9_]*', Name.Class, '#pop')
        ],
        'import': [
            (r'([a-zA-Z0-9_.]+\*?)(?:(\s+)(as)(\s+)([a-zA-Z0-9_.]+\*?))?',
             bygroups(Name.Namespace, Text, Keyword.Namespace, Text, Name.Namespace), '#pop')
        ],
    }
