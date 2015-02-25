#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""CSS-HTML-JS-Minify.

StandAlone Async single-file cross-platform no-dependencies
Unicode-ready Python3-ready Minifier for the Web.
"""


import logging as log
import os
import re
import sys
from argparse import ArgumentParser
from copy import copy
from ctypes import byref, cdll, create_string_buffer
from datetime import datetime
from multiprocessing import cpu_count, Pool
from tempfile import gettempdir
from doctest import testmod

try:
    from urllib import request
except ImportError:
    request = None
try:
    from StringIO import StringIO  # pure-Python StringIO supports unicode.
except ImportError:
    from io import StringIO  # lint:ok
try:
    import resource
except ImportError:
    resource = None  # windows dont have resource


__version__ = '1.0.0'
__license__ = 'GPLv3+ LGPLv3+'
__author__ = 'Juan Carlos'
__email__ = 'juancarlospaco@gmail.com'
__url__ = 'https://github.com/juancarlospaco/css-html-js-minify'
__source__ = ('https://raw.githubusercontent.com/juancarlospaco/'
              'css-html-js-minify/master/css-html-js-minify.py')


start_time = datetime.now()
# 'Color Name String': (R, G, B)
EXTENDED_NAMED_COLORS = {
    'azure': (240, 255, 255), 'beige': (245, 245, 220),
    'bisque': (255, 228, 196), 'blanchedalmond': (255, 235, 205),
    'brown': (165, 42, 42), 'burlywood': (222, 184, 135),
    'chartreuse': (127, 255, 0), 'chocolate': (210, 105, 30),
    'coral': (255, 127, 80), 'cornsilk': (255, 248, 220),
    'crimson': (220, 20, 60), 'cyan': (0, 255, 255),
    'darkcyan': (0, 139, 139), 'darkgoldenrod': (184, 134, 11),
    'darkgray': (169, 169, 169), 'darkgreen': (0, 100, 0),
    'darkgrey': (169, 169, 169), 'darkkhaki': (189, 183, 107),
    'darkmagenta': (139, 0, 139), 'darkolivegreen': (85, 107, 47),
    'darkorange': (255, 140, 0), 'darkorchid': (153, 50, 204),
    'darkred': (139, 0, 0), 'darksalmon': (233, 150, 122),
    'darkseagreen': (143, 188, 143), 'darkslategray': (47, 79, 79),
    'darkslategrey': (47, 79, 79), 'darkturquoise': (0, 206, 209),
    'darkviolet': (148, 0, 211), 'deeppink': (255, 20, 147),
    'dimgray': (105, 105, 105), 'dimgrey': (105, 105, 105),
    'firebrick': (178, 34, 34), 'forestgreen': (34, 139, 34),
    'gainsboro': (220, 220, 220), 'gold': (255, 215, 0),
    'goldenrod': (218, 165, 32), 'gray': (128, 128, 128),
    'green': (0, 128, 0), 'grey': (128, 128, 128),
    'honeydew': (240, 255, 240), 'hotpink': (255, 105, 180),
    'indianred': (205, 92, 92), 'indigo': (75, 0, 130),
    'ivory': (255, 255, 240), 'khaki': (240, 230, 140),
    'lavender': (230, 230, 250), 'lavenderblush': (255, 240, 245),
    'lawngreen': (124, 252, 0), 'lemonchiffon': (255, 250, 205),
    'lightcoral': (240, 128, 128), 'lightcyan': (224, 255, 255),
    'lightgray': (211, 211, 211), 'lightgreen': (144, 238, 144),
    'lightgrey': (211, 211, 211), 'lightpink': (255, 182, 193),
    'lightsalmon': (255, 160, 122), 'lightseagreen': (32, 178, 170),
    'lightslategray': (119, 136, 153), 'lightslategrey': (119, 136, 153),
    'lime': (0, 255, 0), 'limegreen': (50, 205, 50), 'linen': (250, 240, 230),
    'magenta': (255, 0, 255), 'maroon': (128, 0, 0),
    'mediumorchid': (186, 85, 211), 'mediumpurple': (147, 112, 219),
    'mediumseagreen': (60, 179, 113), 'mediumspringgreen': (0, 250, 154),
    'mediumturquoise': (72, 209, 204), 'mediumvioletred': (199, 21, 133),
    'mintcream': (245, 255, 250), 'mistyrose': (255, 228, 225),
    'moccasin': (255, 228, 181), 'navy': (0, 0, 128),
    'oldlace': (253, 245, 230), 'olive': (128, 128, 0),
    'olivedrab': (107, 142, 35), 'orange': (255, 165, 0),
    'orangered': (255, 69, 0), 'orchid': (218, 112, 214),
    'palegoldenrod': (238, 232, 170), 'palegreen': (152, 251, 152),
    'paleturquoise': (175, 238, 238), 'palevioletred': (219, 112, 147),
    'papayawhip': (255, 239, 213), 'peachpuff': (255, 218, 185),
    'peru': (205, 133, 63), 'pink': (255, 192, 203), 'plum': (221, 160, 221),
    'purple': (128, 0, 128), 'rosybrown': (188, 143, 143),
    'saddlebrown': (139, 69, 19), 'salmon': (250, 128, 114),
    'sandybrown': (244, 164, 96), 'seagreen': (46, 139, 87),
    'seashell': (255, 245, 238), 'sienna': (160, 82, 45),
    'silver': (192, 192, 192), 'slategray': (112, 128, 144),
    'slategrey': (112, 128, 144), 'snow': (255, 250, 250),
    'springgreen': (0, 255, 127), 'teal': (0, 128, 128),
    'thistle': (216, 191, 216), 'tomato': (255, 99, 71),
    'turquoise': (64, 224, 208), 'violet': (238, 130, 238),
    'wheat': (245, 222, 179)
}


###############################################################################
# CSS minify


def remove_comments(css):
    """Remove all CSS comment blocks."""
    log.debug("Removing all Comments.")
    iemac, preserve = False, False
    comment_start = css.find("/*")
    while comment_start >= 0:
        # Preserve comments that look like `/*!...*/`.
        # Slicing is used to make sure we dont get an IndexError.
        preserve = css[comment_start + 2:comment_start + 3] == "!"
        comment_end = css.find("*/", comment_start + 2)
        if comment_end < 0:
            if not preserve:
                css = css[:comment_start]
                break
        elif comment_end >= (comment_start + 2):
            if css[comment_end - 1] == "\\":
                # This is an IE Mac-specific comment; leave this one and the
                # following one alone.
                comment_start = comment_end + 2
                iemac = True
            elif iemac:
                comment_start = comment_end + 2
                iemac = False
            elif not preserve:
                css = css[:comment_start] + css[comment_end + 2:]
            else:
                comment_start = comment_end + 2
        comment_start = css.find("/*", comment_start)
    return css


def remove_unnecessary_whitespace(css):
    """Remove unnecessary whitespace characters."""
    log.debug("Removing all unnecessary whitespace.")

    def pseudoclasscolon(css):
        """Prevent 'p :link' from becoming 'p:link'.

        Translates 'p :link' into 'p ___PSEUDOCLASSCOLON___link'.
        This is translated back again later.
        """
        regex = re.compile(r"(^|\})(([^\{\:])+\:)+([^\{]*\{)")
        match = regex.search(css)
        while match:
            css = ''.join([
                css[:match.start()],
                match.group().replace(":", "___PSEUDOCLASSCOLON___"),
                css[match.end():]])
            match = regex.search(css)
        return css

    css = pseudoclasscolon(css)
    # Remove spaces from before things.
    css = re.sub(r"\s+([!{};:>+\(\)\],])", r"\1", css)
    # If there is a `@charset`, then only allow one, and move to beginning.
    css = re.sub(r"^(.*)(@charset \"[^\"]*\";)", r"\2\1", css)
    css = re.sub(r"^(\s*@charset [^;]+;\s*)+", r"\1", css)
    # Put the space back in for a few cases, such as `@media screen` and
    # `(-webkit-min-device-pixel-ratio:0)`.
    css = re.sub(r"\band\(", "and (", css)
    # Put the colons back.
    css = css.replace('___PSEUDOCLASSCOLON___', ':')
    # Remove spaces from after things.
    css = re.sub(r"([!{}:;>+\(\[,])\s+", r"\1", css)
    return css


def remove_unnecessary_semicolons(css):
    """Remove unnecessary semicolons."""
    log.debug("Removing all unnecessary semicolons.")
    return re.sub(r";+\}", "}", css)


def remove_empty_rules(css):
    """Remove empty rules."""
    log.debug("Removing all unnecessary empty rules.")
    return re.sub(r"[^\}\{]+\{\}", "", css)


def normalize_rgb_colors_to_hex(css):
    """Convert `rgb(51,102,153)` to `#336699`."""
    log.debug("Converting all rgba to hexadecimal color values.")
    regex = re.compile(r"rgb\s*\(\s*([0-9,\s]+)\s*\)")
    match = regex.search(css)
    while match:
        colors = map(lambda s: s.strip(), match.group(1).split(","))
        hexcolor = '#%.2x%.2x%.2x' % tuple(map(int, colors))
        css = css.replace(match.group(), hexcolor)
        match = regex.search(css)
    return css


def condense_zero_units(css):
    """Replace `0(px, em, %, etc)` with `0`."""
    log.debug("Condensing all zeroes on values.")
    return re.sub(r"([\s:])(0)(px|em|%|in|cm|mm|pc|pt|ex)", r"\1\2", css)


def condense_multidimensional_zeros(css):
    """Replace `:0 0 0 0;`, `:0 0 0;` etc. with `:0;`."""
    log.debug("Condensing all multidimensional zeroes on values.")
    css = css.replace(":0 0 0 0;", ":0;")
    css = css.replace(":0 0 0;", ":0;")
    css = css.replace(":0 0;", ":0;")
    # Revert `background-position:0;` to the valid `background-position:0 0;`.
    css = css.replace("background-position:0;", "background-position:0 0;")
    css = css.replace("transform-origin:0;", "transform-origin:0 0;")
    return css


def condense_floating_points(css):
    """Replace `0.6` with `.6` where possible."""
    log.debug("Condensing all floating point values.")
    return re.sub(r"(:|\s)0+\.(\d+)", r"\1.\2", css)


def condense_hex_colors(css):
    """Shorten colors from #AABBCC to #ABC where possible."""
    log.debug("Condensing all hexadecimal color values.")
    regex = re.compile(r"([^\"'=\s])(\s*)#([0-9a-fA-F])([0-9a-fA-F])"
                       "([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])")
    match = regex.search(css)
    while match:
        first = match.group(3) + match.group(5) + match.group(7)
        second = match.group(4) + match.group(6) + match.group(8)
        if first.lower() == second.lower():
            css = css.replace(
                match.group(), match.group(1) + match.group(2) + '#' + first)
            match = regex.search(css, match.end() - 3)
        else:
            match = regex.search(css, match.end())
    return css


def condense_whitespace(css):
    """Condense multiple adjacent whitespace characters into one."""
    log.debug("Condensing all unnecessary white spaces.")
    return re.sub(r"\s+", " ", css)


def condense_semicolons(css):
    """Condense multiple adjacent semicolon characters into one."""
    log.debug("Condensing all unnecessary multiple adjacent semicolons.")
    return re.sub(r";;+", ";", css)


def wrap_css_lines(css, line_length):
    """Wrap the lines of the given CSS to an approximate length."""
    log.debug("Wrapping lines to ~{} max line lenght.".format(line_length))
    lines, line_start = [], 0
    for i, char in enumerate(css):
        # Its safe to break after } characters.
        if char == '}' and (i - line_start >= line_length):
            lines.append(css[line_start:i + 1])
            line_start = i + 1
    if line_start < len(css):
        lines.append(css[line_start:])
    return '\n'.join(lines)


def condense_font_weight(css):
    """Condense multiple font weights into shorter integer equals."""
    log.debug("Condensing font weights on values.")
    return css.replace(':normal;', ':400;').replace(':bold;', ':700;')


def condense_std_named_colors(css):
    """Condense named color values to shorter replacement using HEX."""
    log.debug("Condensing standard named color values.")
    for k, v in iter(tuple({'aqua': '#0ff', 'blue': '#00f',
                            'fuchsia': '#f0f', 'yellow': '#ff0'}.items())):
        css = css.replace(k, v)
    return css


def condense_xtra_named_colors(css):
    """Condense named color values to shorter replacement using HEX."""
    log.debug("Condensing extended named color values.")
    for k, v in iter(tuple(EXTENDED_NAMED_COLORS.items())):
        same_color_but_rgb = 'rgb({},{},{})'.format(v[0], v[1], v[2])
        if len(k) > len(same_color_but_rgb):
            css = css.replace(k, same_color_but_rgb)
    return css


def remove_url_quotes(css):
    """Fix for url() does not need quotes."""
    log.debug("Removing quotes from url.")
    return re.sub(r'url\((["\'])([^)]*)\1\)', r'url(\2)', css)


def condense_border_none(css):
    """Condense border:none; to border:0;."""
    log.debug("Condense borders values.")
    return css.replace("border:none;", "border:0;")


def add_encoding(css):
    """Add @charset 'UTF-8'; if missing."""
    log.debug("Adding encoding declaration if needed.")
    return "@charset utf-8;" + css if "@charset" not in css.lower() else css


def restore_needed_space(css):
    """Fix CSS for some specific cases where a white space is needed."""
    return css.replace("!important", " !important"
                       ).replace("@media(", "@media (")


def unquote_selectors(css):
    """Fix CSS for some specific selectors where Quotes is not needed."""
    log.debug("Removing unnecessary Quotes on selectors of CSS classes.")
    return re.compile('([a-zA-Z]+)="([a-zA-Z0-9-_\.]+)"]').sub(r'\1=\2]', css)


def cssmin(css, wrap=None):
    """Minify CSS main function."""
    log.info("Compressing CSS...")
    css = remove_comments(css)
    css = unquote_selectors(css)
    css = condense_whitespace(css)
    css = remove_url_quotes(css)
    css = condense_xtra_named_colors(css)
    css = condense_std_named_colors(css)
    css = condense_font_weight(css)
    css = remove_unnecessary_whitespace(css)
    css = remove_unnecessary_semicolons(css)
    css = condense_zero_units(css)
    css = condense_multidimensional_zeros(css)
    css = condense_floating_points(css)
    css = normalize_rgb_colors_to_hex(css)
    css = condense_hex_colors(css)
    css = condense_border_none(css)
    css = wrap_css_lines(css, wrap) if wrap is not None else css
    css = condense_semicolons(css)
    css = add_encoding(css)
    css = restore_needed_space(css)
    log.info("Finished compressing CSS !.")
    return css.strip()


##############################################################################
# HTML Minify


def condense_html_whitespace(html):
    """Condense HTML, but be safe first if it have textareas or pre tags.

    >>> condense_html_whitespace('<i>  <b>    <a> test </a>    </b> </i><br>')
    '<i><b><a> test </a></b></i><br>'
    """  # first space between tags, then empty new lines and in-between.
    log.debug("Removing unnecessary HTML White Spaces and Empty New Lines.")
    is_ok = "<textarea" not in html.lower() and "<pre" not in html.lower()
    html = re.sub(r'>\s+<', '><', html) if is_ok else html
    return re.sub(r'\s{2,}|[\r\n]', ' ', html) if is_ok else html.strip()


def condense_style(html):
    """Condense style html tags.

    >>> condense_style('<style type="text/css">*{border:0}</style><p>a b c')
    '<style>*{border:0}</style><p>a b c'
    """  # May look silly but Emmet does this and is wrong.
    log.debug("Condensing HTML Style CSS tags.")
    html = html.replace('<style type="text/css">', '<style>')
    html = html.replace("<style type='text/css'>", '<style>')
    html = html.replace("<style type=text/css>", '<style>')
    return html


def condense_script(html):
    """Condense script html tags.

    >>> condense_script('<script type="text/javascript"> </script><p>a b c')
    '<script> </script><p>a b c'
    """  # May look silly but Emmet does this and is wrong.
    log.debug("Condensing HTML Script JS tags.")
    html = html.replace('<script type="text/javascript">', '<script>')
    html = html.replace("<style type='text/javascript'>", '<script>')
    html = html.replace("<style type=text/javascript>", '<script>')
    return html


def clean_unneeded_html_tags(html):
    """Clean unneeded optional html tags.

    >>> clean_unneeded_html_tags('a<body></img></td>b</th></tr></hr></br>c')
    'abc'
    """
    log.debug("Removing unnecessary optional HTML tags.")
    for tag_to_remove in (  # May look silly but Emmet does this and is wrong.
        '</area>', '</base>', '<body>', '</body>', '</br>', '</col>',
        '</colgroup>', '</dd>', '</dt>', '<head>', '</head>', '</hr>',
        '<html>', '</html>', '</img>', '</input>', '</li>', '</link>',
        '</meta>', '</option>', '</p>', '</param>', '<tbody>', '</tbody>',
        '</td>', '</tfoot>', '</th>', '</thead>', '</tr>', '</basefont>',
            '</isindex>', '</param>'):
            html = html.replace(tag_to_remove, '')
    return html


def remove_html_comments(html):
    """Remove all HTML comments, Keep all for Grunt, Grymt and IE.

    >>> _="<!-- build:dev -->a<!-- endbuild -->b<!--[if IE 7]>c<![endif]--> "
    >>> _+= "<!-- kill me please -->keep" ; remove_html_comments(_)
    '<!-- build:dev -->a<!-- endbuild -->b<!--[if IE 7]>c<![endif]--> keep'
    """  # Grunt uses comments to as build arguments, bad practice but still.
    log.debug("""Removing all unnecessary HTML comments; Keep all containing:
    'build:', 'endbuild', '<!--[if]>', '<![endif]-->' for Grunt/Grymt, IE.""")
    return re.compile('<!-- [^(build|endbuild)].*? -->', re.I).sub('', html)


def unquote_html_attributes(html):
    """Remove all HTML quotes on attibutes if possible.

    >>> unquote_html_attributes('<img   width="9" height="5" data-foo="0"  >')
    '<img width=9 height=5 data-foo=0 >'
    """  # data-foo=0> might cause errors on IE, we leave 1 space data-foo=0 >
    log.debug("Removing unnecessary Quotes on attributes of HTML tags.")
    # cache all regular expressions on variables before we enter the for loop.
    any_tag = re.compile(r"<\w.*?>", re.I | re.MULTILINE | re.DOTALL)
    space = re.compile(r' \s+|\s +', re.MULTILINE)
    space1 = re.compile(r'\w\s+\w', re.MULTILINE)
    space2 = re.compile(r'"\s+>', re.MULTILINE)
    space3 = re.compile(r"'\s+>", re.MULTILINE)
    space4 = re.compile('"\s\s+\w+="|\'\s\s+\w+=\'|"\s\s+\w+=|\'\s\s+\w+=',
                        re.MULTILINE)
    space6 = re.compile(r"\d\s+>", re.MULTILINE)
    quotes_in_tag = re.compile('([a-zA-Z]+)="([a-zA-Z0-9-_\.]+)"')
    # iterate on a for loop cleaning stuff up on the html markup.
    for tag in iter(any_tag.findall(html)):
        # exceptions of comments and closing tags
        if tag.startswith('<!') or tag.find('</') > -1:
            continue
        original = tag
        # remove white space inside the tag itself
        tag = space2.sub('" >', tag)  # preserve 1 white space is safer
        tag = space3.sub("' >", tag)
        for each in space1.findall(tag) + space6.findall(tag):
            tag = tag.replace(each, space.sub(' ', each))
        for each in space4.findall(tag):
            tag = tag.replace(each, each[0] + ' ' + each[1:].lstrip())
        # remove quotes on some attributes
        tag = quotes_in_tag.sub(r'\1=\2', tag)
        if original != tag:  # has the tag been improved ?
            html = html.replace(original, tag)
    return html.strip()


def htmlmin(html):
    """Minify HTML main function.

    >>> htmlmin(' <p  width="9" height="5"  > <!-- a --> b </p> c <br> ')
    '<p width=9 height=5 > b c <br>'
    """
    log.info("Compressing HTML...")
    html = remove_html_comments(html)
    html = condense_style(html)
    html = condense_script(html)
    html = clean_unneeded_html_tags(html)
    html = condense_html_whitespace(html)
    html = unquote_html_attributes(html)
    log.info("Finished compressing HTML !.")
    return html.strip()


##############################################################################
# JS Minify


def jsmin(js):
    """Return a minified version of the Javascript string."""
    log.info("Compressing Javascript...")
    ins, outs = StringIO(js), StringIO()
    JavascriptMinify(ins, outs).minify()
    return condense_semicolons(force_single_line_js(outs.getvalue()))


def force_single_line_js(js):
    """Force Javascript to a single line, even if need to add semicolon."""
    log.debug("Forcing JS from {} to 1 Line.".format(len(js.split("\n"))))
    return ";".join(js.split("\n")) if len(js.split("\n")) > 1 else js.strip()


# regular expressions to find and work with Javascript functions and variables
function_start_regex = re.compile('(function[ \w+\s*]\(([^\)]*)\)\s*{)')
function_start_regex = re.compile('(function(\s+\w+|)\s*\(([^\)]*)\)\s*{)')


def _findFunctions(whole):
    """Find function() on Javascript code."""
    for res in function_start_regex.findall(whole):
        function_start, function_name, params = res
        params_split = [x.strip() for x in params.split(',')]
        stack, code, core_code = 1, function_start, ''
        start = whole.find(function_start) + len(code)
        while stack > 0:
            try:
                next_char = whole[start]
            except IndexError:  # dont worry we will obfuscte the one we found
                return  # sometimes fails to find all functions on big files
            core_code += next_char
            if next_char == '{':
                stack += 1
            elif next_char == '}':
                stack -= 1
            start += 1
        yield (params, params_split, core_code[:-1], function_start)


def slim_params(code):
    """Compress params on Javascript code functions.

    >>> slim_params('function f(large_name,is_large){large_name*is_large}')
    'function f(_0,_1){_0*_1}'
    """
    old_functions, new_code = {}, code
    for params, params_split, core, function_start in _findFunctions(code):
        params_split_use = [x for x in params_split if len(x) > 1]
        _param_regex = '|'.join([r'\b%s\b' % x for x in params_split_use])
        param_regex, new_params = re.compile(_param_regex), {}
        for i in range(len(params_split_use)):
            new_params[params_split[i]] = '_{}'.format(i)
        replacer_1 = lambda __match: new_params.get(__match.group())
        new_core, _params = param_regex.sub(replacer_1, core), []
        for p in params_split:
            _params.append(new_params.get(p, p))
        new_function = function_start.replace(
            params, ','.join(_params)) + new_core + '}'
        old_function = function_start + core + '}'
        old_functions[old_function] = new_function
    regex = '|'.join([re.escape(x) for x in old_functions.keys()])
    replacer_2 = lambda __match: old_functions.get(__match.group())
    return re.sub(regex, replacer_2, new_code)


class NamesGenerator:

    """Class to generate names for Javascript code function variables."""

    def __init__(self):
        """Init class, setup basic variables."""
        self.i, self.pool = 0, list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def next(self):
        """Work with next items.

        >>> _=NamesGenerator();(_.next(),_.next(),_.next(),_.next(),_.next())
        ('_A', '_B', '_C', '_D', '_E')
        """
        try:
            e = self.pool[self.i]
            self.i = self.i + 1
        except IndexError:
            if not hasattr(self, 'j'):
                self.j = 0
                self.pool.extend([x.lower() for x in self.pool])
            try:
                e = self.pool[self.i % len(self.pool)] + self.pool[self.j]
                self.j = self.j + 1
            except IndexError:
                self.i += 1
                self.j = 0
                return self.next()
        return '_{}'.format(e)


def slim_func_names(js):
    """Compress Javascript variable names inside functions.

    >>> slim_func_names('function longName(p1,p2){return p1*p2}longName(2,4)')
    'function _A(p1,p2){return p1*p2}_A(2,4);var longName=_A;'
    """
    renamed_func, functions = [], re.compile('(function (\w+)\()').findall(js)
    new_names_generator = NamesGenerator()
    for whole_func, func_name in functions:
        count = js.count(func_name)  # more than 1 mention of the function
        if len(func_name) > 3 and count > 1:  # function name larger than 3
            new_name = new_names_generator.next()
            if re.findall(r'\b%s\b' % re.escape(new_name), js):
                continue
            js = re.sub(r'\b%s\b' % re.escape(func_name), new_name, js)
            renamed_func.append((func_name, new_name))
    list_of_replacements = ['{}={}'.format(x, y) for (x, y) in renamed_func]
    js_function_name_replacements = ';var {};'.format(  # ;var a=b,c=d; or ''
        ','.join(list_of_replacements)) if len(list_of_replacements) else ""
    return js + js_function_name_replacements


def slim(js):
    """Compress variables and functions names.

    >>> slim('function foo( long_variable_name, bar ) { console.log(bar); };')
    'function foo(_0,_1) { console.log(_1); };'
    """
    log.debug("Obfuscating Javascript variables names inside functions.")
    # if eval() or with{} is used on JS is not too Safe to Obfuscate stuff.
    is_ok = "eval(" not in js and "with{" not in js and "with {" not in js
    return slim_func_names(slim_params(js)) if is_ok else js.strip()


class JavascriptMinify(object):

    """Minify an input stream of Javascript, writing to an output stream."""

    def __init__(self, instream=None, outstream=None):
        """Init class."""
        self.ins, self.outs = instream, outstream

    def minify(self, instream=None, outstream=None):
        """Minify Javascript using StringIO."""
        if instream and outstream:
            self.ins, self.outs = instream, outstream
        write, read = self.outs.write, self.ins.read
        space_strings = ("abcdefghijklmnopqrstuvwxyz"
                         "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$\\")
        starters, enders = '{[(+-', '}])+-"\''
        newlinestart_strings = starters + space_strings
        newlineend_strings = enders + space_strings
        do_newline, do_space = False, False
        doing_single_comment, doing_multi_comment = False, False
        previous_before_comment, in_quote = '', ''
        in_re, quote_buf = False, []
        previous = read(1)
        next1 = read(1)
        if previous == '/':
            if next1 == '/':
                doing_single_comment = True
            elif next1 == '*':
                doing_multi_comment = True
            else:
                write(previous)
        elif not previous:
            return
        elif previous >= '!':
            if previous in "'\"":
                in_quote = previous
            write(previous)
            previous_non_space = previous
        else:
            previous_non_space = ' '
        if not next1:
            return
        while True:
            next2 = read(1)
            if not next2:
                last = next1.strip()
                conditional_1 = (doing_single_comment or doing_multi_comment)
                if not conditional_1 and last not in ('', '/'):
                    write(last)
                break
            if doing_multi_comment:
                if next1 == '*' and next2 == '/':
                    doing_multi_comment = False
                    next2 = read(1)
            elif doing_single_comment:
                if next1 in '\r\n':
                    doing_single_comment = False
                    while next2 in '\r\n':
                        next2 = read(1)
                        if not next2:
                            break
                    if previous_before_comment in ')}]':
                        do_newline = True
                    elif previous_before_comment in space_strings:
                        write('\n')
            elif in_quote:
                quote_buf.append(next1)

                if next1 == in_quote:
                    numslashes = 0
                    for c in reversed(quote_buf[:-1]):
                        if c != '\\':
                            break
                        else:
                            numslashes += 1
                    if numslashes % 2 == 0:
                        in_quote = ''
                        write(''.join(quote_buf))
            elif next1 in '\r\n':
                conditional_2 = previous_non_space in newlineend_strings
                if conditional_2 or previous_non_space > '~':
                    while 1:
                        if next2 < '!':
                            next2 = read(1)
                            if not next2:
                                break
                        else:
                            conditional_3 = next2 in newlinestart_strings
                            if conditional_3 or next2 > '~' or next2 == '/':
                                do_newline = True
                            break
            elif next1 < '!' and not in_re:
                conditional_4 = next2 in space_strings or next2 > '~'
                conditional_5 = previous_non_space in space_strings
                conditional_6 = previous_non_space > '~'
                if (conditional_5 or conditional_6) and (conditional_4):
                    do_space = True
            elif next1 == '/':
                if in_re:
                    if previous != '\\':
                        in_re = False
                    write('/')
                elif next2 == '/':
                    doing_single_comment = True
                    previous_before_comment = previous_non_space
                elif next2 == '*':
                    doing_multi_comment = True
                else:
                    in_re = previous_non_space in '(,=:[?!&|'
                    write('/')
            else:
                if do_space:
                    do_space = False
                    write(' ')
                if do_newline:
                    write('\n')
                    do_newline = False
                write(next1)
                if not in_re and next1 in "'\"":
                    in_quote = next1
                    quote_buf = []
            previous = next1
            next1 = next2
            if previous >= '!':
                previous_non_space = previous


##############################################################################


def walkdir_to_filelist(where, target, omit):
    """Perform full walk of where, gather full path of all files."""
    log.debug("""Recursively Scanning {}, searching for {}, and ignoring {}.
    """.format(where, target, omit))
    return tuple([os.path.join(root, f) for root, d, files in os.walk(where)
                  for f in files if not f.startswith('.')  # ignore hidden
                  and not f.endswith(omit)  # not process processed file
                  and f.endswith(target)])  # only compress target files


def process_multiple_files(file_path):
    """Process multiple CSS, JS, HTML files with multiprocessing."""
    log.debug("Process {} is Compressing {}.".format(os.getpid(), file_path))
    if file_path.endswith(".css"):
        process_single_css_file(file_path)
    elif file_path.endswith(".js"):
        process_single_js_file(file_path)
    else:
        process_single_html_file(file_path)


def prefixer_extensioner(file_path, old, new):
    """Take a file path and safely prepend a prefix and change extension.

    This is needed because filepath.replace('.foo', '.bar') sometimes may
    replace '/folder.foo/file.foo' into '/folder.bar/file.bar' wrong!.
    >>> prefixer_extensioner('/tmp/test.js', '.js', '.min.js')
    '/tmp/test.min.js'
    """
    log.debug("Prepending Prefix to {}.".format(file_path))
    global args
    extension = os.path.splitext(file_path)[1].lower().replace(old, new)
    filenames = os.path.splitext(os.path.basename(file_path))[0]
    filenames = args.prefix + filenames if args.prefix else filenames
    dir_names = os.path.dirname(file_path)
    file_path = os.path.join(dir_names, filenames + extension)
    return file_path


def process_single_css_file(css_file_path):
    """Process a single CSS file."""
    log.info("Processing CSS file: {}".format(css_file_path))
    global args
    try:  # Python3
        with open(css_file_path, encoding="utf-8-sig") as css_file:
            minified_css = cssmin(css_file.read(), wrap=80)
    except:  # Python2
        with open(css_file_path) as css_file:
            minified_css = cssmin(css_file.read(), wrap=80)
    if args.timestamp:
        taim = "/* {} */ ".format(datetime.now().isoformat()[:-7].lower())
        minified_css = taim + minified_css
    css_file_path = prefixer_extensioner(css_file_path, ".css", ".min.css")
    try:
        with open(css_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(minified_css)
    except:
        with open(css_file_path, "w") as output_file:
            output_file.write(minified_css)


def process_single_html_file(html_file_path):
    """Process a single HTML file."""
    log.info("Processing HTML file: {}".format(html_file_path))
    try:  # Python3
        with open(html_file_path, encoding="utf-8-sig") as html_file:
            minified_html = htmlmin(html_file.read())
    except:  # Python2
        with open(html_file_path) as html_file:
            minified_html = htmlmin(html_file.read())
    html_file_path = prefixer_extensioner(html_file_path, ".htm", ".html")
    try:  # Python3
        with open(html_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(minified_html)
    except:  # Python2
        with open(html_file_path, "w") as output_file:
            output_file.write(minified_html)


def process_single_js_file(js_file_path):
    """Process a single JS file."""
    log.info("Processing JS file: {}".format(js_file_path))
    try:  # Python3
        with open(js_file_path, encoding="utf-8-sig") as js_file:
            minified_js = jsmin(slim(js_file.read()))
    except:  # Python2
        with open(js_file_path) as js_file:
            minified_js = jsmin(slim(js_file.read()))
    if args.timestamp:
        taim = "/* {} */ ".format(datetime.now().isoformat()[:-7].lower())
        minified_js = taim + minified_js
    js_file_path = prefixer_extensioner(js_file_path, ".js", ".min.js")
    try:  # Python3
        with open(js_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(minified_js)
    except:  # Python2
        with open(js_file_path, "w") as output_file:
            output_file.write(minified_js)


def check_for_updates():
    """Method to check for updates from Git repo versus this version."""
    if not request:
        log.critical("Feature only available on Python 3.x, command ignored.")
        return
    this_version = str(open(__file__).read())
    last_version = str(request.urlopen(__source__).read().decode("utf8"))
    if this_version != last_version:
        log.warning("Theres new Version available!,Update from " + __source__)
    else:
        log.info("No new updates!,You have the lastest version of this app.")


def main():
    """Main Loop."""
    if not sys.platform.startswith("win") and sys.stderr.isatty():
        def add_color_emit_ansi(fn):
            """Add methods we need to the class."""
            def new(*args):
                """Method overload."""
                if len(args) == 2:
                    new_args = (args[0], copy(args[1]))
                else:
                    new_args = (args[0], copy(args[1]), args[2:])
                if hasattr(args[0], 'baseFilename'):
                    return fn(*args)
                levelno = new_args[1].levelno
                if levelno >= 50:
                    color = '\x1b[31;5;7m\n '  # blinking red with black
                elif levelno >= 40:
                    color = '\x1b[31m'  # red
                elif levelno >= 30:
                    color = '\x1b[33m'  # yellow
                elif levelno >= 20:
                    color = '\x1b[32m'  # green
                elif levelno >= 10:
                    color = '\x1b[35m'  # pink
                else:
                    color = '\x1b[0m'  # normal
                try:
                    new_args[1].msg = color + str(new_args[1].msg) + ' \x1b[0m'
                except Exception as reason:
                    print(reason)  # Do not use log here.
                return fn(*new_args)
            return new
        # all non-Windows platforms support ANSI Colors so we use them
        log.StreamHandler.emit = add_color_emit_ansi(log.StreamHandler.emit)
    log.basicConfig(
        level=-1, format="%(levelname)s:%(asctime)s %(message)s", filemode="w",
        filename=os.path.join(gettempdir(), "css-html-js-minify.log"))
    log.getLogger().addHandler(log.StreamHandler(sys.stderr))
    try:
        os.nice(19)  # smooth cpu priority
        libc = cdll.LoadLibrary('libc.so.6')  # set process name
        buff = create_string_buffer(len("css-html-js-minify") + 1)
        buff.value = bytes("css-html-js-minify".encode("utf-8"))
        libc.prctl(15, byref(buff), 0, 0, 0)
    except Exception as reason:
        pass  # this may fail on windows and its normal, so be silent.
    # Parse command line arguments.
    parser = ArgumentParser(description=__doc__, epilog="""CSS-HTML-JS-Minify:
    Takes a file or folder full path string and process all CSS/HTML/JS found.
    If argument is not file/folder will fail. Check Updates works on Python3.
    StdIn to StdOut is deprecated since may fail with unicode characters.""")
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('fullpath', metavar='fullpath', type=str,
                        help='Full path to local file or folder.')
    parser.add_argument('--wrap', action='store_true',
                        help="Wrap Output to ~80 chars per line, CSS Only.")
    parser.add_argument('--prefix', type=str,
                        help="Prefix string to prepend on output filenames.")
    parser.add_argument('--timestamp', action='store_true',
                        help="Add a Time Stamp on all CSS/JS output files.")
    parser.add_argument('--quiet', action='store_true',
                        help="Quiet, force disable all Logging.")
    parser.add_argument('--checkupdates', action='store_true',
                        help="Check for Updates from Internet while running.")
    parser.add_argument('--tests', action='store_true',
                        help="Run all built-in Unit Tests, report and exit.")
    global args
    args = parser.parse_args()
    if args.checkupdates:
        check_for_updates()
    if args.tests:
        testmod(verbose=True, report=True, exclude_empty=True)
        sys.exit(0)
    if args.quiet:
        log.disable(log.CRITICAL)
    log.info(__doc__ + __version__)
    # Work based on if argument is file or folder, folder is slower.
    if os.path.isfile(args.fullpath) and args.fullpath.endswith(".css"):
        log.info("Target is a CSS File.")
        list_of_files = str(args.fullpath)
        process_single_css_file(args.fullpath)
    elif os.path.isfile(args.fullpath) and args.fullpath.endswith(".htm"):
        log.info("Target is a HTML File.")
        list_of_files = str(args.fullpath)
        process_single_html_file(args.fullpath)
    elif os.path.isfile(args.fullpath) and args.fullpath.endswith(".js"):
        log.info("Target is a JS File.")
        list_of_files = str(args.fullpath)
        process_single_js_file(args.fullpath)
    elif os.path.isdir(args.fullpath):
        log.info("Target is a Folder with CSS, HTML, JS.")
        log.warning("Processing a whole Folder may take some time...")
        list_of_files = walkdir_to_filelist(args.fullpath,
                                            (".css", ".js", ".htm"),
                                            (".min.css", ".min.js", ".html"))
        pool = Pool(cpu_count())  # Multiprocessing Async
        pool.map_async(process_multiple_files, list_of_files)
        pool.close()
        pool.join()
    else:
        log.critical("File or folder not found,or cant be read,or I/O Error.")
        sys.exit(1)
    log.info('-' * 80)
    log.info('Files Processed: {}.'.format(list_of_files))
    log.info('Number of Files Processed: {}'.format(
        len(list_of_files) if isinstance(list_of_files, tuple) else 1))
    log.info('Total Maximum RAM Memory used: ~{} MegaBytes.'.format(int(
        resource.getrusage(resource.RUSAGE_SELF).ru_maxrss *
        resource.getpagesize() / 1024 / 1024 if resource else 0)))
    log.info('Total Processing Time: {}.'.format(datetime.now() - start_time))


if __name__ in '__main__':
    main()
