#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:wd

from tasks import app


@app.task
def show_name(name: str):
    print(name)
