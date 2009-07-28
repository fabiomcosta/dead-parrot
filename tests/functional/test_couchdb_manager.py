# -*- coding: utf-8; -*-
#
# Copyright (C) 2009 Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
import os
from nose.tools import assert_equals
from deadparrot import models
from utils import ignore_it
from couchdb import Server

def setup():
    try:
        global svr
        svr  = Server('http://localhost:5984/')
        del svr['dead_parrot']
    except: pass

#@ignore_it('changing to use couch api')
def test_couchdb_file_manager_create():
    
    class FooBarSerial(models.Model):
        name = models.CharField(max_length=100)
        age = models.IntegerField()
        objects = models.CouchDBModelManager(base_uri='http://localhost:5984/')
        def __unicode__(self):
            return u'<FooBarSerial(name=%r)>' % self.name

    expected = FooBarSerial(name='foo bar', age=7)
    got = FooBarSerial.objects.create(name='foo bar', age=7)

    assert expected == got, 'Expected %r, got %r' % (expected, got)

def test_model_file_manager_create_many():
    class WeeWooSerial(models.Model):
        name = models.CharField(max_length=100)
        age = models.IntegerField()
        objects = models.CouchDBModelManager(base_uri='http://localhost:5984/')
        def __unicode__(self):
            return u'<WeeWooSerial(name=%r)>' % self.name

    f1 = WeeWooSerial.objects.create(name='foo one', age=40)
    f2 = WeeWooSerial.objects.create(name='foo two', age=41)
    f3 = WeeWooSerial.objects.create(name='foo three', age=42)

    assert len(svr['dead_parrot']) == 3

test_model_file_manager_create_many.setup = setup

