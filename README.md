=== cgiproxy

A reverse-proxy CGI script. Translates CGI requests to a downstream HTTP(S) requests.

Useful when you need to expose your local Web service to the Internet, but the rest of your infrastructure comes from the previous century.

== Requirements
 - Python 3.6

== What works
 - GET, POST, PUT

== Limitations
 - No streaming due to the way CGI works -- the response bodies need to be dechunked.
 - Almost no headers can be propagated.
 - No Cookies (yet.)

== Usage
 - Copy cgiproxy.py to the path your HTTP server sees and change the TARGET at the top of the script *OR* place cgiproxy.py anywhere you want and create a script in the server path containing:
    !/bin/sh
    exec PATH_TO_CGIPROXY TARGET
 - Ensure that the script is executable by the HTTP user and that all its path components are accessible.
 - Avoid symlinks, as executing CGI through symlinks is usually disabled for security reasons.

= Apache
To make `cgiproxy` work under Apache, CGI support needs to be enabled:

    <IfModule !mpm_prefork_module>
        LoadModule cgid_module modules/mod_cgid.so
    </IfModules>
    <IfModule mpm_prefork_module>
        LoadModule cgi_module modules/mod_cgi.so
    </IfModules>

and the directory containing `cgiproxy.py` needs to be configured to run CGI:

    <Directory "CGIPROXY_DIRECTORY">
        AddHandler cgi-script .py
        Options +ExecCGI
    </Directory>
