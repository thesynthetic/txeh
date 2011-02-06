# -*- coding: utf-8 -*- 
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
from gluon.tools import Auth


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """

    searchform = FORM('#:',
                    INPUT(_name='searchtext',requires=IS_NOT_EMPTY()),
                    INPUT(_type='submit'))
    
    if searchform.accepts(request.vars, session, formname='searchform'):
        response.flash = 'form accepted'
    elif searchform.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'


    createform = FORM('hext:',
                        INPUT(_name='hext',requires=IS_NOT_EMPTY()),
                        INPUT(_name='url',requires=IS_NOT_EMPTY()),
                        INPUT(_type='submit'))
    
    if createform.accepts(request.vars, session, formname='createform'):
        session.solicitcreate = True
        session.hext = createform.vars.hext
        session.url = createform.vars.url
        redirect(URL('create'))
        #response.flash = 'form accepted'
    elif createform.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'

    return dict(message=T(''),
                searchform=searchform,
                createform=createform)
#end def Index()

def user():
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()


