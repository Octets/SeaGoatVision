#! /usr/bin/env python

#    Copyright (C) 2012  Octets - octets.etsmtl.ca
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

import logging
import inspect
import logging
import time

# date formater with day, use : "%Y-%m-%d %H:%M:%S"

last_print_duplicate = ""
last_time_print = time.time()
spam_delay_sec = 5

def get_logger(name):
    key = "SeaGoatVision."
    if name.startswith(key):
        name = name[len(key):]

    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter("[%(asctime)s-%(levelname)s-%(name)s] %(message)s",
                                  "%H:%M:%S")

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
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
            to_print = "(spam delay %d sec) %s" % (spam_delay_sec, origin_to_print)
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
