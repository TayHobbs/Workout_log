# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Log.name'
        db.add_column(u'logs_log', 'name',
                      self.gf('django.db.models.fields.CharField')(default='Workout', max_length=30),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Log.name'
        db.delete_column(u'logs_log', 'name')


    models = {
        u'logs.log': {
            'Meta': {'object_name': 'Log'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'workouts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['logs.Workout']", 'symmetrical': 'False'})
        },
        u'logs.workout': {
            'Meta': {'object_name': 'Workout'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_of_workout': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'reps': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['logs']