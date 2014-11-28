# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Workout'
        db.create_table(u'logs_workout', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_of_workout', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('reps', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'logs', ['Workout'])

        # Adding model 'Log'
        db.create_table(u'logs_log', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'logs', ['Log'])

        # Adding M2M table for field workouts on 'Log'
        m2m_table_name = db.shorten_name(u'logs_log_workouts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('log', models.ForeignKey(orm[u'logs.log'], null=False)),
            ('workout', models.ForeignKey(orm[u'logs.workout'], null=False))
        ))
        db.create_unique(m2m_table_name, ['log_id', 'workout_id'])


    def backwards(self, orm):
        # Deleting model 'Workout'
        db.delete_table(u'logs_workout')

        # Deleting model 'Log'
        db.delete_table(u'logs_log')

        # Removing M2M table for field workouts on 'Log'
        db.delete_table(db.shorten_name(u'logs_log_workouts'))


    models = {
        u'logs.log': {
            'Meta': {'object_name': 'Log'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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