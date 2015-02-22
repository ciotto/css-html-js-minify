# css-html-js-minify

- **StandAlone Async single-file cross-platform no-dependencies Unicode-ready Python3-ready Minifier for the Web.**


```bash
css-html-js-minify.py --help

usage: css-html-js-minify.py [-h] [--version] [--wrap] [--prefix PREFIX]
[--timestamp] [--quiet] [--checkupdates]
[--autocommit]
fullpath

CSS-HTML-JS-Minify. StandAlone Async single-file cross-platform no-
dependencies Unicode-ready Python3-ready Minifier for the Web.

positional arguments:
    fullpath         Full path to local file or folder.

optional arguments:
    -h, --help       show this help message and exit
    --version        show program's version number and exit
    --wrap           Wrap Output to ~80 chars per line, CSS Only.
    --prefix PREFIX  Prefix string to prepend on output filenames.
    --timestamp      Add a Time Stamp on all CSS/JS output files.
    --quiet          Quiet, force disable all Logging.
    --checkupdates   Check for Updates from Internet while running.
    --autocommit     Automatically commit all changed files to Git, ask for a
    commit message to be typed by the user.

    CSS-HTML-JS-Minify: Takes a file or folder full path string and process all
    CSS/HTML/JS found. If argument is not file/folder will fail. Check Updates
    works on Python3. Git Auto-Commit only works on Linux/OsX and asks for commit
    Message. StdIn to StdOut is deprecated since may fail with unicode characters.

```

- Takes a full path to anything, a file or a folder, then parse, optimize and compress for Production.
- If full path is a folder with multiple files it will use Async Multiprocessing.
- Pretty-Printed colored Logging to Standard Output and Log File on OS Temporary Folder.
- No Dependencies at all, just needs Python Standard Built-in Libs.
- Set its own Process name and show up on Process lists.
- Can check for updates for itself.
- Full Unicode/UTF-8 support.
- Smooth CPU usage.
- `*.css` files are saved as `*.min.css`, `*.js` are saved as `*.min.js`, `*.htm` are saved as `*.html`


# Usage:

```bash
css-html-js-minify.py file.htm

css-html-js-minify.py file.css

css-html-js-minify.py file.js

css-html-js-minify.py /project/static/
```


# Install permanently on the system:

```
sudo wget -O /usr/bin/css-html-js-minify https://raw.githubusercontent.com/juancarlospaco/css-html-js-minify/master/css-html-js-minify.py
sudo chmod +x /usr/bin/css-html-js-minify
css-html-js-minify
```


# Why?:

- **Why another Compressor ?**, theres lots of Compressor for Web files outthere!; *Or maybe not ?*.
- Lots work inside DJango/Flask only, or Frameworks of PHP/Java/Ruby, or can Not process whole folders.

| Name | Reason |
| ---- | ------ |
| [YUI-Compressor](www.yuiblog.com/blog/2012/10/16/state-of-yui-compressor) | Deprecated, Needs Java, Dead since ~2012, No HTML Minification, Complex to Install |
| [UglifyJS](https://github.com/mishoo/UglifyJS2) | Needs NodeJS, No HTML/CSS Minification, Cant process whole folders, Slow |
| [Slimmer](https://pypi.python.org/pypi/slimmer) | Python2 Only, No Unicode/UTF-8 Support, Dead since ~2009 |
| [CSSMin](https://pypi.python.org/pypi/cssmin) | No Unicode/UTF-8 Support, Dead since ~2013, No HTML/JS Minification, Cant process whole folders |
| [django-cssmin](https://github.com/zacharyvoase/django-cssmin) | Uses CSSMin which is Dead, DJango only, No HTML/JS Minification |
| [SlimIt](https://pypi.python.org/pypi/slimit) | JS Only, to use as RunTime Module, Dead sincec ~2013, Cant process whole folders |
| [JSMin](https://pypi.python.org/pypi/jsmin) | JS Only, Cant process whole folders |
| All On-Line Minifiers | Cant process whole folders, Slow, No Unicode/UTF-8 Support usually |


# Requisites:

- [Python 3.x](https://www.python.org "Python Homepage") *(or Python 2.x)*


# Licence:

- GNU GPL Latest Version *AND* GNU LGPL Latest Version *AND* any Licence YOU Request via Bug Report.


Donate, Charityware :
---------------------

- [Charityware](https://en.wikipedia.org/wiki/Donationware) is a licensing model that supplies fully operational unrestricted software to the user and requests an optional donation be paid to a third-party beneficiary non-profit. The amount of donation may be left to the discretion of the user. Its GPL-compatible and Enterprise ready.
- If you want to Donate please [click here](http://www.icrc.org/eng/donations/index.jsp) or [click here](http://www.atheistalliance.org/support-aai/donate) or [click here](http://www.msf.org/donate) or [click here](http://richarddawkins.net/) or [click here](http://www.supportunicef.org/) or [click here](http://www.amnesty.org/en/donate)
