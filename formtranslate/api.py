import subprocess
from formtranslate import config

def validate(input_data):
    '''Validates an xform into an xsd file'''
    # hack
    vals = form_translate(input_data, "schema")
    vals["outstring"] = ""
    return vals

def get_xsd_schema(input_data):
    '''Translates an xform into an xsd file'''
    return form_translate(input_data, "schema")

def readable_form(input_data):
    '''Gets a readable display of an xform'''
    return form_translate(input_data, "summary")


def csv_dump(input_data):
    '''Get the csv translation file from an xform'''
    return form_translate(input_data, "csvdump")

def form_translate(input_data, operation):
    """Utility for interacting with the form_translate jar, which provides 
       functionality for a number of different useful form tools including 
       converting a form to an xsd file, turning a form into a more readable
       format, and generating a list of translations as an exportable .csv
       file."""
    
    # In case you're trying to produce this behavior on the command line for
    # rapid testing, the command that eventually gets called is: 
    # java -jar form_translate.jar <operation> < form.xml > output
    #
    # You can pass in a filename or a full string/stream of xml data
    p = subprocess.Popen(["java","-jar",
                          config.FORM_TRANSLATE_JAR_LOCATION,
                          operation], 
                          shell=False, 
                          stdout=subprocess.PIPE,
                          stdin=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    p.stdin.write(input_data)
    p.stdin.flush()
    p.stdin.close()
    
    output = p.stdout.read()    
    error = p.stderr.read()
    
    # todo: this is horrible.
    has_error = "exception" in error.lower() 
    
    return {"success": not has_error,
            "errstring": error,
            "outstring": output}
