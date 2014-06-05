# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from flask import current_app, request, render_template
from ggrc.app import app
from ggrc.login import login_required
from ggrc.models import all_models
from ggrc.notification import EmailNotification, EmailDigestNotification
from datetime import datetime


@app.route("/prepare_email", methods=["GET", "POST"])
@login_required
def prepare_email_ggrc_users():
  """ prepare email digest
  """
  model = request.args.get('model')
  id = request.args.get('id')
  cls = getattr(all_models, model)
  obj = cls.query.filter(cls.id == int(id)).first()
  if obj is not None:
    target_objs=[]
    recipients=[obj.contact]
    email_notification = EmailNotification()
    if obj is not None:
      subject = obj.type + " " + obj.title + " created"
      content = obj.type + ": " + obj.title + " : " + request.url_root + obj._inflector.table_plural + \
       "/" + str(obj.id) + " created on " + str(obj.created_at)
      email_notification.prepare(target_objs, obj.contact, recipients, subject, content)
  return render_template("dashboard/index.haml")


@app.route("/prepare_emaildigest", methods=["GET", "POST"])
@login_required
def prepare_email_digest_ggrc_users():
  """ prepare email digest
  """
  model = request.args.get('model')
  id = request.args.get('id')
  import ggrc.models
  cls = getattr(all_models, model)
  obj = cls.query.filter(cls.id == int(id)).first()
  if obj is not None:
    target_objs=[]
    recipients=[obj.contact]
    email_digest_notification = EmailDigestNotification()
    if obj is not None:
      subject = obj.type + " " + "Email Digest for " + datetime.now().strftime('%Y/%m/%d')
      content = obj.type + ": " + obj.title + " : " + request.url_root + obj._inflector.table_plural+ \
       "/" + str(obj.id) + " created on " + str(obj.created_at)
      email_digest_notification.prepare(target_objs, obj.contact, recipients, subject, content)
  return render_template("dashboard/index.haml")


@app.route("/notify_email", methods=["GET", "POST"])
@login_required
def notify_email_ggrc_users():
  """ notify email for a program object
  """
  email_notification = EmailNotification()
  email_notification.notify()
  return render_template("dashboard/index.haml")


@app.route("/notify_emaildigest", methods=["GET", "POST"])
@login_required
def notify_email_digest_ggrc_users():
  """ notify email digest 
  """
  email_digest_notification = EmailDigestNotification()
  email_digest_notification.notify()
  return render_template("dashboard/index.haml")
