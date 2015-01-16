from django.conf.urls import *

urlpatterns = patterns('formtranslate.views',
    url(r'^$', 'home', name='formtranslate_home'),
    url(r'^validate/$', 'validate', name='formtranslate_validate'),
    url(r'^readable/$', 'readable', name='formtranslate_readable'),
    url(r'^csv/$', 'csv', name='formtranslate_csv'),
    url(r'^xsd/$', 'xsd', name='formtranslate_xsd'),
    
)