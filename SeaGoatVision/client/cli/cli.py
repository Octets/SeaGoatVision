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

"""
Description : Run the command line interface to communicate with the \
SeaGoatVision Server
"""
import fileinput


def run(ctr, subscriber, local=False,
        host="localhost", port=8090, quiet=False):
    # TODO implement using subscriber
    from vCmd import VCmd
    VCmd(
        ctr,
        stdin=fileinput.input(),
        local=local,
        host=host,
        port=port,
        quiet=quiet).cmdloop()
    return 0
