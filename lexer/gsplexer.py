# -*- coding: utf-8 -*-
"""
    Lexer for the Groovy Server Pages
    Mostly copy-paste from JspLexer
"""

from pygments.lexer import RegexLexer, DelegatingLexer, using
from pygments.lexers.web import XmlLexer
from pygments.token import Keyword, Other
from lexer.groovylexer import GroovyLexer

class GspRootLexer(RegexLexer):
    """
    Base for the `GspLexer`. Yields `Token.Other` for area outside of
    GSP tags.
    """

    tokens = {
        'root': [
            (r'<%\S?', Keyword, 'groovy1'),
            (r'\$\{', Keyword, 'groovy2'),
            # FIXME: I want to make these keywords but still parse attributes.
            (r'</?g:(actionSubmit|applyLayout|checkBox|collect|cookie|country).*?>', Keyword),
            (r'</?g:(countrySelect|createLink|createLinkTo|currencySelect).*?>', Keyword),
            (r'</?g:(datePicker|each|eachError|else|elseif|fieldValue|findAll).*?>', Keyword),
            (r'</?g:(form|formRemote|formatBoolean|formatDate|formatNumber|grep).*?>', Keyword),
            (r'</?g:(hasErrors|header|hiddenField|if|include|javascript|layoutBody).*?>', Keyword),
            (r'</?g:(layoutHead|layoutTitle|link|localeSelect|message|meta).*?>', Keyword),
            (r'</?g:(pageProperty|paginate|passwordField|radio|radioGroup).*?>', Keyword),
            (r'</?g:(remoteField|remoteFunction|remoteLink|render|renderErrors).*?>', Keyword),
            (r'</?g:(resource|select|set|sortableColumn|submitButton|submitToRemote).*?>', Keyword),
            (r'([^<$]|\$[^{])+', Other),
            (r'<', Other),
        ],
        'groovy1': [
            (r'%>', Keyword, '#pop'),
            # note: '\w\W' != '.' without DOTALL.
            (r'[\w\W]+?(?=%>|\Z)', using(GroovyLexer)),
        ],
        'groovy2': [
            (r'}', Keyword, '#pop'),
            # FIXME: ${ "${...}" } is not parsed correctly
            # note: '\w\W' != '.' without DOTALL.
            (r'[\w\W]+?(?=}|\Z)', using(GroovyLexer)),
        ],
    }


class GspLexer(DelegatingLexer):
    """
    Lexer for Groovy Server Pages.
    """

    name = 'Groovy Server Page'
    aliases = ['gsp']
    filenames = ['*.gsp']
    mimetypes = ['application/x-gsp']

    def __init__(self, **options):
        super(GspLexer, self).__init__(XmlLexer, GspRootLexer, **options)

    def analyse_text(text):
        rv = GroovyLexer.analyse_text(text) - 0.01
        if looks_like_xml(text):
            rv += 0.4
        if '<%' in text and '%>' in text:
            rv += 0.1
        if '${' in text and '}' in text:
            rv += 0.1
        return rv

