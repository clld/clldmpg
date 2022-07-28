clldmpg
=======

Python library providing common functionality for CLLD apps maintained in affiliation
with the MPG.

Provides an MPG specific pyramid app scaffold and a pyramid package to be included by
a clld app.

Note: The `templates` directory provided by this package must be specified in an app's `appconf.ini`
in the correct position to make template lookup work, e.g.
```ini
[mako]
directories_list = concepticon:templates clldmpg:templates clld:web/templates
```
