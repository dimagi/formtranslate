A small django web-api wrapper for JavaRosa's XForm Jar tools

The tools are form_translate.jar and javarosa-xform-validator.jar.

This is used to interact with the java-based XForm tool that lets you
validate XForms and get readable XForms. 

This app provides a basic API to the form translate jar utility file.

The API is:

POST
{"xform": <XFORM_BODY_GOES_HERE>}


RESPONSE
A json response with the following structure:
{
 "success": <our best guess as to whether it succeeded>
 "outstring": <the jar's output to stdout, if any>
 "errstring": <the jar's output to stderr, if any> 
}

The following services are available endpoints:

/formtranslate/validate - validate an xform (errors will be in errstring)
/formtranslate/readable - get a readable copy of the xform (will be in outstring)
/formtranslate/csv      - get the csv translation file for the form (will be in outstring)
/formtranslate/xsd      - get the xsd file for the form (will be in outstring)

There's also a reference implementation of the UI available at

/formtranslate/


The latest form_translate.jar is available at 

http://build.dimagi.com:250/

KNOWN ISSUES:

Certain malformed forms crash it.