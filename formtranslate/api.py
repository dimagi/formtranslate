import subprocess
from formtranslate import config
from tempfile import NamedTemporaryFile
import os

def validate(input_data, version='1.0'):
    """Validates an xform into an xsd file"""
    # hack
    vals = form_translate(input_data, "schema", version=version)
    vals["outstring"] = ""
    return vals

def get_xsd_schema(input_data, version='1.0'):
    """Translates an xform into an xsd file"""
    return form_translate(input_data, "schema", version=version)

def readable_form(input_data, version='1.0'):
    """Gets a readable display of an xform"""
    return form_translate(input_data, "summary", version=version)


def csv_dump(input_data, version='1.0'):
    """Get the csv translation file from an xform"""
    return form_translate(input_data, "csvdump", version=version)

def form_translate(input_data, operation, version='1.0'):
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
            location = config.get_form_translate_jar_location(version)
            p = subprocess.Popen(["java","-jar",
                                  location,
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

        
        
    
    