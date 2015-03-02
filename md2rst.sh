#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#    sudo apt-get install pandoc

chrt --verbose --idle 0 pandoc --from=markdown_github --to=rst --smart --output=README.rst README.md
