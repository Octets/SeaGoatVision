#! /usr/bin/env python

#    Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
#
#    This file is part of SeaGoatVision.
#
#    SeaGoatVision is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import inspect
import logging
import time
import os

# date formater with day, use : "%Y-%m-%d %H:%M:%S"

last_print_duplicate = ""
last_time_print = time.time()
spam_delay_sec = 5
formatter = logging.Formatter(
    "[%(asctime)s.%(msecs)d-%(levelname)s-%(name)s] %(message)s",
    "%H:%M:%S")
dct_file_handler = {}
dct_logger = {}


def add_handler(file_path):
    global own_logger
    global formatter
    global dct_file_handler
    global dct_logger

    if not isinstance(file_path, str):
        own_logger.error(
            "The path %s is not type of string, type is %s" %
            (file_path, type(file_path)))
        return

    if file_path in dct_file_handler.values():
        own_logger.error("The path %s is already handled on log." % file_path)
        return

    if os.path.isfile(file_path):
        os.remove(file_path)

    hdlr = logging.FileHandler(filename=file_path)
    hdlr.setFormatter(formatter)

    for logger in dct_logger.values():
        logger.addHandler(hdlr)

    dct_file_handler[file_path] = hdlr


def remove_handler(file_path):
    global own_logger
    global dct_file_handler
    global dct_logger

    if not isinstance(file_path, str):
        own_logger.error(
            "The path %s is not type of string, type is %s" %
            (file_path, type(file_path)))
        return

    hdlr = dct_file_handler.get(file_path, None)
    if not hdlr:
        own_logger.warning("The path %s is not handled on log." % file_path)
        return

    for logger in dct_logger.values():
        logger.removeHandler(hdlr)

    del dct_file_handler[file_path]


def get_logger(name):
    global dct_logger
    global formatter
    global dct_file_handler

    key = "SeaGoatVision."
    if name.startswith(key):
        name = name[len(key):]

    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    if name not in dct_logger:
        dct_logger[name] = logger

    for handler in dct_file_handler.values():
        logger.addHandler(handler)

    return logger


def printerror_stacktrace(logger, message, check_duplicate=False):
    global last_print_duplicate
    global last_time_print
    global spam_delay_sec

    func = inspect.currentframe().f_back.f_code
    origin_to_print = to_print = "%s: %s() in %s:%i" % (
        message,
        func.co_name,
        func.co_filename,
        func.co_firstlineno
    )
    if check_duplicate:
        if to_print == last_print_duplicate:
            to_print = "(spam delay %d sec) %s" % (
                spam_delay_sec, origin_to_print)
            # each 3 seconds, print the message
            if not(time.time() - last_time_print > spam_delay_sec):
                return
        last_time_print = time.time()
        last_print_duplicate = origin_to_print
    logger.error(to_print)


def print_function(logger_call, message, last_stack=False):
    if last_stack:
        func = inspect.currentframe().f_back.f_back.f_code
    else:
        func = inspect.currentframe().f_back.f_code
    to_print = "%s() %s" % (
        func.co_name,
        message
    )
    logger_call(to_print)


# create own_logger to log info from himself!!
own_logger = get_logger(__name__)
