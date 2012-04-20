# coding=utf-8
from zope.component import createObject
from zope.pagetemplate.pagetemplatefile import PageTemplateFile
import zope.interface, zope.component, zope.publisher.interfaces
import zope.viewlet.interfaces, zope.contentprovider.interfaces 
from gs.profile.base.contentprovider import ContentProvider
from interfaces import IGSVerifyingJavaScriptContentProvider

class GSVerifyingJavaScriptContentProvider(ContentProvider):
    """Content provider for the JavaScript to verify email addresses."""
    zope.interface.implements( IGSVerifyingJavaScriptContentProvider )
    zope.component.adapts(zope.interface.Interface,
        zope.publisher.interfaces.browser.IDefaultBrowserLayer,
        zope.interface.Interface)

    def __init__(self, context, request, view):
        ContentProvider.__init__(self, context, request, view)
        self.__updated = False
        
    def update(self):
        self.__updated = True
        self.siteName = self.siteInfo.name.replace("'", r"\'")
        
    def render(self):
        if not self.__updated:
            raise interfaces.UpdateNotCalled

        pageTemplate = PageTemplateFile(self.pageTemplateFileName)
        return pageTemplate(view=self)

zope.component.provideAdapter(GSVerifyingJavaScriptContentProvider,
    provides=zope.contentprovider.interfaces.IContentProvider,
    name="groupserver.VerifyEmailJavaScript")

