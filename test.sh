#!/usr/bin/env bash
# -*- coding: utf-8 -*-
wget https://code.jquery.com/jquery-git2.js
python2 ./css-html-js-minify.py --prefix temp_ --timestamp --checkupdates --wrap ./jquery-git2.js
python3 ./css-html-js-minify.py --prefix temp_ --timestamp --checkupdates --wrap ./jquery-git2.js
wget https://maxcdn.bootstrapcdn.com/bootstrap/latest/css/bootstrap.css
python2 ./css-html-js-minify.py --prefix temp_ --timestamp --checkupdates --wrap ./bootstrap.css
python3 ./css-html-js-minify.py --prefix temp_ --timestamp --checkupdates --wrap ./bootstrap.css
