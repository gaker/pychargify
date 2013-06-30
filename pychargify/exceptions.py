# -*- coding: utf-8 -*-
'''
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


Created on 30 June 2013
Author: Paul Trippett (paul@pyhub.com)
        Greg Aker (me@gregaker.net)
'''

class ChargifyError(Exception):
    """
    A Chargify Releated error
    @license    GNU General Public License
    """
    pass


class ChargifyUnAuthorized(ChargifyError):
    """
    Returned when API authentication has failed.
    @license    GNU General Public License
    """
    pass


class ChargifyForbidden(ChargifyError):
    """
    Returned by valid endpoints in our application that have not been
    enabled for API use.
    @license    GNU General Public License
    """
    pass


class ChargifyNotFound(ChargifyError):
    """
    The requested resource was not found.
    @license    GNU General Public License
    """
    pass


class ChargifyUnProcessableEntity(ChargifyError):
    """
    Sent in response to a POST (create) or PUT (update) request
    that is invalid.
    @license    GNU General Public License
    """
    pass


class ChargifyServerError(ChargifyError):
    """
    Signals some other error
    @license    GNU General Public License
    """
    pass
