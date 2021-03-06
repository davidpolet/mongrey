# -*- coding: utf-8 -*-

import datetime
import json
from wtforms import fields

from flask import abort, redirect, url_for, request, session, current_app

from flask_admin import Admin, AdminIndexView as BaseAdminIndexView, expose
from flask_admin.model import filters
from flask_admin.contrib.peewee.view import ModelView as BaseModelView
from flask_admin.contrib.peewee.form import CustomModelConverter
from flask_admin.contrib.peewee.filters import FilterConverter 

from playhouse import shortcuts

import arrow

from ...ext.flask_login import current_user, logout_user
from ... import constants
from ...web.extensions import gettext, lazy_gettext

from ...web.admin import (moment_format,
                             key_format,
                             SecureView)
from . import models

class CustomFilterConverter(FilterConverter):

    @filters.convert('DateTimeFieldExtend')
    def conv_datetime(self, column, name):
        return [f(column, name) for f in self.datetime_filters]

    #@filters.convert('ListCharField')
    #def conv_datetime(self, column, name):
    #    return [f(column, name) for f in self.datetime_filters]

class ModelConverter(CustomModelConverter):

    def handle_list(self, model, field, **kwargs):
        return field.name, fields.FieldList(**kwargs)
    
    def __init__(self, view, additional=None):
        CustomModelConverter.__init__(self, view, additional=additional)
        self.converters[models.DateTimeFieldExtend] = self.handle_datetime        
        self.converters[models.ListCharField] = self.handle_list       

def json_convert(obj):
    
    if isinstance(obj, datetime.datetime):
        return arrow.get(obj).for_json()
    
    return obj

def jsonify(obj):
    content = json.dumps(obj, default=json_convert)
    return current_app.response_class(content, mimetype='application/json')


class ModelView(SecureView, BaseModelView):
    
    model_form_converter = ModelConverter
    
    filter_converter = CustomFilterConverter()

class UserView(ModelView):
    
    column_list = ('username',)

    column_searchable_list = ('username',)

class DomainView(ModelView):
    
    column_list = ('name',)

    column_searchable_list = ('name',)

class MailboxView(ModelView):
    
    column_list = ('name',)

    column_searchable_list = ('name',)

class MynetworkView(ModelView):
    
    column_list = ('value', 'comments')

    column_searchable_list = ('value', 'comments')

class WhiteListView(ModelView):
    
    column_list = ('value', 'field_name', 'comments')

    column_formatters = {
        #"field_name": lambda v, c, m, n: m.get_field_name_display(),
    }

    column_searchable_list = ('value', 'comments')

class BlackListView(ModelView):
    
    column_list = ('value', 'field_name', 'comments')

    column_formatters = {
        #"field_name": lambda v, c, m, n: m.get_field_name_display(),
    }

    column_searchable_list = ('value', 'comments')

class PolicyView(ModelView):
    
    column_list = ('name', 'value', 'field_name', 'greylist_key', 'greylist_remaining', 'greylist_expire', 'comments')
    
    column_formatters = {
        #"field_name": lambda v, c, m, n: m.get_field_name_display(),
    }
    
    
class GreylistMetricView(ModelView):
    
    can_edit = False

    can_create = False
    
    column_list = ('timestamp', 'count', 'accepted', 'rejected', 'requests', 'abandoned', 'delay')
    
    column_formatters = {
        "timestamp": lambda v, c, m, n: moment_format(m.timestamp),
    }


class GreylistEntryView(ModelView):
    """
    TODO: Actions
        add whitelist ip
        add whitelist sender email
        add whitelist sender domain
        add whitelist recipient email
        add whitelist recipient domain
    """

    list_template = "mongrey/greylistentry_list.html"

    column_list = ('key', 'timestamp', 'delay', 'expire_time', 'rejects', 'accepts', 'policy')

    can_edit = False
    can_create = False

    column_formatters = {
        "key": lambda v, c, m, n: key_format(m.id, m.key),
        "timestamp": lambda v, c, m, n: moment_format(m.timestamp),
        "expire_time": lambda v, c, m, n: moment_format(m.expire_time),
    }

    column_filters = ['key', 'timestamp', 'expire_time']

    column_searchable_list = ['key']

    @expose('/show')
    def show(self):
        _id = request.args.get('id')
        model = self.get_one(_id)
        if not model:
            abort(404)

        kwargs = shortcuts.model_to_dict(model, exclude=['protocol'])#, recurse, backrefs, only, exclude, seen)
        kwargs['protocol'] = json.loads(model.protocol)

        return self.render('mongrey/greylistentry_show.html', **kwargs)


class AdminIndexView(SecureView, BaseAdminIndexView):

    @expose()
    def index(self):
        return redirect(url_for('greylistentry.index_view'))
    
    @expose('/logout')
    def logout(self):
        logout_user()
        return redirect(url_for('admin.index'))
    
    @expose('/change-lang', methods=('GET',))
    def change_lang(self):
        """
        {{ url_for('user_menu.change_lang') }}?locale=fr
        """
        
        from flask_babelex import refresh
        locale = request.args.get("locale", None)
        current_lang = session.get(constants.SESSION_LANG_KEY, None)

        if locale and current_lang and locale != current_lang and locale in dict(current_app.config.get('ACCEPT_LANGUAGES_CHOICES')).keys():
            session[constants.SESSION_LANG_KEY] = locale
            refresh()

        _next = request.args.get("next") or request.referrer or request.url
        return redirect(_next)


def init_admin(app, 
               admin_app=None, 
               url='/admin',
               name=u"Greylist",               
               base_template='mongrey/layout.html',
               index_template=None,
               index_view=None,
               ):
    
    index_view = index_view or AdminIndexView(template=index_template,                                               
                                              url=url,
                                              name="home")
    
    admin = admin_app or Admin(app,
                               url=url,
                               name=name,
                               index_view=index_view, 
                               base_template=base_template, 
                               template_mode='bootstrap3'
                               )
    
    admin.add_view(UserView(models.User, 
                                 name=gettext(u"Users")))

    admin.add_view(DomainView(models.Domain, 
                                 name=gettext(u"Domains")))

    admin.add_view(MailboxView(models.Mailbox, 
                                 name=gettext(u"Mailboxs")))
    
    admin.add_view(MynetworkView(models.Mynetwork, 
                                 name=gettext(u"Mynetworks")))

    admin.add_view(PolicyView(models.Policy, 
                                      name=gettext(u"Policies")))
    
    admin.add_view(GreylistEntryView(models.GreylistEntry, 
                                     name=gettext(u"Greylists")))

    admin.add_view(WhiteListView(models.WhiteList, 
                                 name=gettext(u"Whitelists")))
    
    admin.add_view(BlackListView(models.BlackList, 
                                 name=gettext(u"Blacklists")))
        
    admin.add_view(GreylistMetricView(models.GreylistMetric, 
                                      name=gettext(u"Metrics")))
