# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-21 16:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("flows", "0154_populate_flowstart_counts")]

    operations = [migrations.RemoveField(model_name="flowrun", name="message_ids")]