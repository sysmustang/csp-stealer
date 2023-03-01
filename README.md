CSPstealer
=========

This is tool used to retrieve web-page secrets and bypass Content Security Policy.  
In general, the functionality is similar to xsshunter.  

It's helpful when you have an XSS, but there is no way to steal secrets because of CSP.  
Especially it may increase your chanses to find Blind Stored XSS.  

The concept was introduced at VolgaCTF 2021. To have more information you can read see original [report](csp_bypass.pdf).


Installation & Usage
------------
To simple run you need docker and docker-compose:
```
./run.sh
```
To run app without docker you need python 3.6+ and installed requirements:
```
pip install -r requirements.txt
./run.sh --no-docker
```

If you need https you can put `cert.crt` and `private.key` to ./ssl directory.  
SSL isn't required and CSP bypass will work even on pages with https.

Application works on 0.0.0.0:[80 | 443] ports. For example, to login you have to go to http://localhost/admin. 
