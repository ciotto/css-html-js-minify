# css-html-js-minify

- **StandAlone Async single-file cross-platform no-dependencies Unicode-ready Python3-ready Minifier for the Web.**


```bash
css-html-js-minify.py --help

usage: css-html-js-minify.py [-h] [--version] [-w WRAP] [--quiet] fullpath

CSS-HTML-JS-Minify - StandAlone Async single-file cross-platform 
no-dependencies Unicode-ready Python3-ready Minifier for the Web.

positional arguments:
  fullpath              Full path to local file or folder.

optional arguments:
  -h, --help            show this help message and exit
  --version             show programs version number and exit
  -w WRAP, --wrap WRAP  Wrap Output to N chars per line, CSS Only.
  --quiet               Quiet, force disable all Logging.

CSS-HTML-JS-Minify: 
Takes a file or folder full path string and process all CSS/HTML/JS found. 
If argument is not a file or folder it will fail and raise errors. 
StdIn to StdOut is deprecated since may fail with unicode characters.
```

- Takes a full path to anything, a file or a folder, then parse, optimize and compress for Production.
- If full path is a folder with multiple files it will use Async Multiprocessing.
- Pretty-Printed colored Logging to Standard Output and Log File on OS Temporary Folder.
- No Dependencies at all, just needs Python Standard Built-in Libs.
- Set its own Process name and show up on Process lists.
- Full Unicode/UTF-8 support.
- Smooth CPU usage.
- `*.css` files are saved as `*.min.css`, `*.js` are saved as `*.min.js`, `*.htm` are saved as `*.html`
- Do NOT obfuscates code.


# Usage:

```bash
css-html-js-minify.py file.htm

css-html-js-minify.py file.css

css-html-js-minify.py file.js

css-html-js-minify.py /project/static/
```


# Try it !:

```
wget -O - https://raw.githubusercontent.com/juancarlospaco/css-html-js-minify/master/css-html-js-minify.py | python3
```

# Install permanently on the system:

```
sudo wget -O /usr/bin/css-html-js-minify https://raw.githubusercontent.com/juancarlospaco/css-html-js-minify/master/css-html-js-minify.py
sudo chmod +x /usr/bin/css-html-js-minify
css-html-js-minify
```


# Requisites:

- [Python 3.x](https://www.python.org "Python Homepage") *(or Python 2.x)*


Donate, Charityware :
---------------------

- [Charityware](https://en.wikipedia.org/wiki/Donationware) is a licensing model that supplies fully operational unrestricted software to the user and requests an optional donation be paid to a third-party beneficiary non-profit. The amount of donation may be left to the discretion of the user. Its GPL-compatible and Enterprise ready.
- If you want to Donate please [click here](http://www.icrc.org/eng/donations/index.jsp) or [click here](http://www.atheistalliance.org/support-aai/donate) or [click here](http://www.msf.org/donate) or [click here](http://richarddawkins.net/) or [click here](http://www.supportunicef.org/) or [click here](http://www.amnesty.org/en/donate)
