# -*- coding: utf-8 -*- 
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import datetime
import logging
helper = local_import('Helper')


def index():
    response.title = 'hext.me | links for the real world'
    searchform = FORM('',
                    INPUT(_name='searchtext',
                          _id='searchtext',
                          _autocomplete='off',
                          requires=IS_NOT_EMPTY()),
                    INPUT(_name='searchtextgrey',
                          _disabled='disabled',
                          _id='searchtextgrey',
                          _autocomplete='off'),
                    INPUT(_type='submit',_id='searchformsubmit'),
                    _id='searchform')
    
    createform = FORM(DIV("Hext Text",_class="inputheader"),
                      INPUT(_name='hext',
                              _autocomplete='off',
                              requires=IS_NOT_EMPTY(),
                              _class="createhextinput"),
                      DIV("Web Address",_class="inputheader"),
                      INPUT(_name='url',
                              _autocomplete='off',
                              requires=IS_NOT_EMPTY(),
                              _class="createhextinput"),
                      INPUT(_type='submit'))

    if searchform.accepts(request.vars, session, formname='searchform'):
        search = searchform.vars.searchtext.lower().strip()
        results = db(db.hexts.hextstring==search).select()
        found = False
        for result in results:
            db.tracker.insert(hext=result.id,
                              timestamp=datetime.datetime.now())
            found = True
            db(db.hexts.id == result.id).update(totalHits=result.totalHits + 1)
            redirect(result.url)
        if not found:
            response.flash = "Sorry, that hext link doesn't exist. Please try again."
    elif searchform.errors:
        response.flash = 'Sorry, please see errors below.'
    else:
        if createform.accepts(request.vars, session, formname='createform'):
            if auth.user is None:
                tempuser = None
            else:
                tempuser = auth.user.id
                
            session.hext = createform.vars.hext.lower().strip()
            session.solicitcreate = True
            session.url = createform.vars.url

            #Test existance before adding (display error if duplicate)
            results = db(db.hexts.hextstring==createform.vars.hext).select()
            found = False
            for result in results:
                found = True

            if not found:
                db.hexts.insert(hextstring=session.hext,
                                url=createform.vars.url,
                                createdBy=tempuser,
                                dateCreated=datetime.datetime.now(),
                                totalHits=0)
                response.flash = '##' + session.hext + '## successfuly created'
            else:
                response.flash = '## Sorry, hext link already exists with that name ##'
            
        elif createform.errors:
            response.flash = '## Sorry, please see errors below. ##'
        else:
            response.flash = '## Welcome to hext.me - links for the real world ##'

    return dict(message=T(''),
                searchform=searchform,
                createform=createform)

#end def Index()

def dashboard():
    #redirect if not authed
    if auth.user is None:
        redirect(URL(r=request,f='index'))
    hextStringList = []
    allTimeHits = []
    results = db(db.hexts.createdBy==auth.user.id).select()
    for result in results:
        hextStringList.append("#" + result.hextstring)
        allTimeHits.append(db(db.tracker.hext==result.id).count())
        
    return dict(message=T(''),
                hexts=hextStringList,
                hits=allTimeHits)
    

def livesearch():
    srch = request.vars.partialsearch.lower()
    beginning = srch
    ending = srch + u'\ufffd'
    #MyModel.all().filter('prop >=', prefix).filter('prop <', prefix + u'\ufffd')
    results = db((db.hexts.hextstring>=beginning) &
                 (db.hexts.hextstring<ending)).select()
    tempList = []
    #tempList.append(request.vars.partialsearch)
    for item in results:
        tempList.append(item.hextstring)
    return response.json(tempList)


def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
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


