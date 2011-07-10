import subprocess
from formtranslate import config
from tempfile import NamedTemporaryFile
import os

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
    with NamedTemporaryFile("w", suffix=".txt", delete=False) as stdout_file:
        with NamedTemporaryFile("w", suffix=".txt", delete=False) as stderr_file:
            p = subprocess.Popen(["java","-jar",
                                  config.FORM_TRANSLATE_JAR_LOCATION,
                                  operation], 
                                  shell=False, 
                                  stdin=subprocess.PIPE,
                                  stdout=stdout_file,
                                  stderr=stderr_file)
            
            p.stdin.write(input_data)
            p.stdin.flush()
            p.stdin.close()
            p.wait()
            
            with open(stdout_file.name, "r") as f:
                output = f.read()    
            with open(stderr_file.name, "r") as f:
                error = f.read()
            
            try:
                os.unlink(stdout_file.name)
                os.unlink(stderr_file.name)
            except Exception:
                pass
            
            # todo: this is horrible.
            has_error = "exception" in error.lower() 
            return {"success": not has_error,
                    "errstring": error,
                    "outstring": output}

        
        
    
    