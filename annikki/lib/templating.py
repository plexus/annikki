"""
Extensions/adaptations of pylons.templating
"""

from pylons.templating import pylons_globals, cached_template
from webhelpers.html import literal
from genshi.filters import HTMLFormFiller

from annikki.lib.filters import HTMLFormErrors

def render_genshi(template_name, extra_vars=None, cache_key=None, 
                  cache_type=None, cache_expire=None, method='xhtml', 
                  form_data=None, form_errors=None):
    """Render a template with Genshi
   
    Taken from Pylons, augmented with the HTMLFormFiller functionality,
    use ``form_data'' option.

    Accepts the cache options ``cache_key``, ``cache_type``, and
    ``cache_expire`` in addition to method which are passed to Genshi's
    render function.    
    """
    # Create a render callable for the cache function
    def render_template():
        # Pull in extra vars if needed
        globs = extra_vars or {}
        
        # Second, get the globals
        globs.update(pylons_globals())

        # Grab a template reference
        template = globs['app_globals'].genshi_loader.load(template_name)

        stream = template.generate(**globs)

        if form_data:
            stream = stream | HTMLFormFiller(data=form_data)

        if form_errors:
            stream = stream | HTMLFormErrors(errors=form_errors)
 
        return literal(stream.render(method=method, encoding=None))

    # if there's form data we don't cache
    if form_data or form_errors:
        return render_template()

    return cached_template(template_name, render_template, cache_key=cache_key,
                           cache_type=cache_type, cache_expire=cache_expire,
                           ns_options=('method'), method=method)

