#-----------------------------------------------------------------------------
# Name:        DjangoUtils
# Purpose:     To create websites using meta scripting of django
# Author:      Aric Sanders
# Created:     3/20/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" DjangoUtils contains helper functions and classes to create django websites
 using meta-scripting tools


 Help
---------------
<a href="./index.html">`pyMez.Code.Utils`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>"""
#-----------------------------------------------------------------------------
# Standard Imports
import os
#-----------------------------------------------------------------------------
# Third Party Imports

#-----------------------------------------------------------------------------
# Module Constants
TEMPLATE_BEGIN_STRING="{% extends 'index.html' %}\n{% load i18n %}\n"
#-----------------------------------------------------------------------------
# Module Functions
def build_index():
    """Builds index.html given a set of inputs"""
    pass


def create_nav_bar_string(**options):
    """Creates a django templated nav bar string for insertion into the {% block nav %} {% endblock %} template
    tags"""
    defaults = {"nav_class": "navbar navbar-inverse",
                "site_name": "Calnet",
                "apps": ["Home", "Help"],
                "registration": """
              {% if user.is_authenticated %}
                </ul>
                  <ul class="nav navbar-nav navbar-right">
                  <li><a href="/accounts/user_info/">
                  <span class="glyphicon glyphicon-user"></span>
                  {% trans "Logged in" %}: {{ user.username }}</a></li>
                  <li><a href="{% url 'auth_logout' %}"><span class="glyphicon glyphicon-log-out"></span> Logout</a></li>
                 </ul>
              {% else %}
                  </ul>
                  <ul class="nav navbar-nav navbar-right">
                  <li><a href="/accounts/register/"><span class="glyphicon glyphicon-user"></span> Sign Up</a></li>
                  <li><a href="{% url 'auth_login' %}"><span class="glyphicon glyphicon-log-in"></span> Login</a></li>
                </ul>
              {% endif %}""",
                "search": """<form class="navbar-form navbar-right" role="search">
                              <div class="form-group">
                              <input type="text" class="form-control" placeholder="Search">
                              </div>
                             <button type="submit" class="btn btn-default">
                             <span class="glyphicon glyphicon-search"></span></button>
                            </form>"""}
    nav_bar_options = {}
    for key, value in defaults.items():
        nav_bar_options[key] = value
    for key, value in options.items():
        nav_bar_options[key] = value
    output_string = ""
    string_template = """
    <nav class="{nav_class}" id="navbar">
        <div class="container-fluid">
            <div class="navbar-header">
              <a class="navbar-brand" href="/"><span class="badge">{site_name}</span></a>
            </div>
        <ul class="nav navbar-nav">
            {app_link_string}
            {registration}
        {search}
        </div>
    </nav>
    """
    app_link_string = ""
    for app in nav_bar_options["apps"]:
        app_link_string = app_link_string + '<li><a href="/{0}">{0}</a> </li>'.format(app)
    nav_bar_options["app_link_string"] = app_link_string
    if not nav_bar_options["registration"]:
        nav_bar_options = "</ol>"
    if not nav_bar_options["search"]:
        nav_bar_options["search"] = ""

    return string_template.format(**nav_bar_options)

def write_home_templates():
    """Writes several basic templates to the current directory includes index.html
    and a series of templates required for registrations"""
    # the index.html requires enough information
    template_names=["index.html","activate.html","login.html",
                    "logout.html","password_change_done.html","password_change_form.html",
                    "password_reset_complete.html","password_reset_confirm.html",
                    "password_reset_done.html","password_reset_email.html",
                    "password_reset_form.html","registration_complete.html",
                    "registration_form.html"]
    pass

def write_project_urls(app_names):
    """Writes a basic urls.py for a django-project
    given the app names"""
    urls_imports=['from django.conf.urls import include, url\n',
                 'from django.contrib import admin\n']

    url_pattern_lines=['urlpatterns= [\n',
                       "  url(r'^admin/', admin.site.urls),\n"
                      ]
    for app_name in app_names:
        url_pattern="  url(r'^%s/',include('%s.urls')),\n"%(app_name,app_name)
        url_pattern_lines.append(url_pattern)
    url_pattern_lines.append('  ]')

    out_file=open('urls.py','w')
    for line in urls_imports:
        out_file.write(line)
    for line in url_pattern_lines:
        out_file.write(line)
    out_file.close()

def write_app_urls(app_name):
    """Writes a basic urls.py for a django-app"""
    # Write the import string
    urls_imports=['from django.conf.urls import url\n',
                 'from . import views\n']
    # write the app_name = line, allows for namespacing the url template tags
    app_name_line="app_name= '%s'\n"%app_name
    # write the url patterns
    url_pattern_lines=['urlpatterns= [\n',
                       "  url(r'^$',views.index,name='index'),\n",
                      '  ]\n']
    # open the file and do the work
    out_file=open('urls.py','w')
    for line in urls_imports:
        out_file.write(line)
    out_file.write(app_name_line)
    for line in url_pattern_lines:
        out_file.write(line)
    out_file.close()
def write_admin_file(directory=None):
    """Writes an admin file in specified directory, defaults to the current directory"""
    if directory is not None:
        os.chdir(directory)
    admin_file_template=['# class functions from the standard library\n', 
                     'import pyclbr\n', 'import re\n',
                     'import os\n', 'from django.contrib import admin\n', '\n',
                     'def register_all_models(module=None,path=None):\n',
                     '    """ This function registers all modules in with the django admin. \n',
                     "    The module name should be a string, and defaults to 'models' and the path can be a string, list or tuple\n",
                     '    If you include the admin.ModelAdmin in the models.py module with the same name + Admin\n',
                     '    then it will register them too. Example if the model class is Pizza, then the admin model\n',
                     '    class would be PizzaAdmin """\n', '    if module is None:\n', "        module='models'\n",
                     '    if path is None:\n', '        path=os.path.dirname(os.path.abspath(__file__))\n',
                     '        classes = pyclbr.readmodule(module,[path])\n', '    elif type(path) is str:\n',
                     '        classes = pyclbr.readmodule(module,[path])\n', '    else:\n',
                     '        classes = pyclbr.readmodule(module,path)\n', '    # first make a list of string only parents\n',
                     '    for model in classes:\n', '        if classes[model].super[0] in classes.values():\n',
                     '            classes[model].super=classes[model].super[0].super\n', '\n',
                     '    # make a list of admin classes\n', '    admin_classes=[]\n', '    for model in classes:\n',
                     '        for superclass in classes[model].super:\n', '            try:\n',
                     "                if re.search('admin.ModelAdmin',superclass):\n",
                     '                    admin_classes.append(model)\n',
                     '            except:pass\n', '    for model in classes:\n',
                     '        # now the dirty part, check that the models are classes that inherit from models.Model\n',
                     '        # if this inhertance is not explicit in the class call it will not be registered\n',
                     '        for superclass in classes[model].super:\n', '            try:\n',
                     "                if re.search('models.Model',superclass):\n",
                     '                    try:\n',
                     '                        # Check to see if the modelNameAdmin is in the list of admin classes\n',
                     "                        test_name=model+'Admin'\n",
                     '                        if test_name in admin_classes:\n',
                     "                            exec('from %s import %s,%s'%(module,model,test_name))\n",
                     "                            exec('admin.site.register(%s,%s)'%(model,test_name))\n",
                     '                        else:\n',
                     '                        # this could be a from module import * above this loop\n',
                     "                            exec('from %s import %s'%(module,model))\n",
                     "                            exec('admin.site.register(%s)'%model)\n",
                     '                    except:raise\n',
                     '            except:pass\n', 'register_all_models()']
    out_file=open('admin.py','w')
    for line in admin_file_template:
        out_file.write(line)
    out_file.close()
#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts
def build_calnet_script():
    """Builds a django app called calnet with apps defined by app_names"""
    try:
        # set the top most directory
        current_directory=os.getcwd() # Should change this if it needs to be
        # name the project
        project_name='Calnet'
        #name the apps, use a general naming scheme. Here I have used CamelCase and Nouns
        # Always include the home app, it will be were the base templates and views live
        app_names=['Home','Repository','ProjectTracker','CheckStandard',
                   'Uncertainties','Measurement','Preferences','Help']
        # run a system command to create the project
        os.system('django-admin startproject %s'%project_name)
        # move into the directory with manage.py in it
        os.chdir(os.path.join(current_directory,'%s'%project_name))
        # keep the current directory
        current_directory=os.getcwd()
        manage_directory=os.getcwd() # we will want this directory for a lot of things
        # write a urls for the project
        os.chdir(os.path.join(manage_directory,'%s'%project_name))
        write_project_urls(app_names)
        os.chdir(manage_directory)
        # loop through the apps creating them 
        for app in app_names:
            os.system('python manage.py startapp %s'%app)   
        # Now write the urls.py for each app, and a general admin that imports all models from models into the admin
        for app in app_names:
            os.chdir(os.path.join(manage_directory,'%s'%app))
            write_app_urls(app)
            write_admin_file()
        # Once the apps are made, make static and 
        # template directories in each app for {{ static files }}
        # Note this could be combined with the 'startapp' loop
        for app in app_names:
            # static directory is redundant for makedirs, but retained for clarity
            # These directories are in the location django will look for them
            static_directory=os.path.join(current_directory,'%s'%app,'static','%s'%app)
            template_directory=os.path.join(current_directory,'%s'%app,'templates','%s'%app)
            # This could be a list of exec commands
            img_directory=os.path.join(current_directory,'%s'%app,'static','%s'%app,'img')
            js_directory=os.path.join(current_directory,'%s'%app,'static','%s'%app,'js')
            css_directory=os.path.join(current_directory,'%s'%app,'static','%s'%app,'css')
            # directories specific to my way of doing help or documentation
            jupyter_directory=os.path.join(current_directory,'%s'%app,'static','%s'%app,'jupyter')
            html_directory=os.path.join(current_directory,'%s'%app,'static','%s'%app,'html')
            cache=os.path.join(current_directory,'%s'%app,'static','%s'%app,'cache')
            # help application
            if app in ['Help','help','doc','docs','documentation']:
                os.makedirs(static_directory)
                os.makedirs(template_directory)
                os.makedirs(img_directory)
                os.makedirs(js_directory)
                os.makedirs(css_directory)
                os.makedirs(cache)
                os.makedirs(jupyter_directory)
                os.makedirs(html_directory)
                
            else:
                os.makedirs(static_directory)
                os.makedirs(template_directory)
                os.makedirs(img_directory)
                os.makedirs(js_directory)
                os.makedirs(css_directory)
                os.makedirs(cache)
    except:raise
#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass