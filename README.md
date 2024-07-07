CSPstealer
=========

CSPstealer is a tool designed to retrieve web-page secrets and bypass Content Security Policy (CSP) restrictions. The tool significantly increases your chances of finding Blind Stored XSS. Also if you've identified an XSS vulnerability but are hindered by CSP, CSPstealer can help you overcome these limitations.

The concept was first presented at VolgaCTF 2021. For a deeper understanding of how CSPstealer operates, you can refer to the original [presentation slides](csp_bypass.pdf).

## Primary Use Cases
* Finding Blind Stored XSS: CSPstealer is particularly useful in scenarios where Blind XSS might be present. The majority of sites have weak CSP that includes 'unsafe-inline' in the script-src directive, so this tool gives you significantly more chances to find Blind XSS compared to any other tool for this purpose.
* Bypassing CSP with XSS: When you have an XSS vulnerability that allows you to execute JavaScript, but CSP restrictions prevent you from sending any data out. CSPstealer helps in bypassing these restrictions to extract the secrets you need.



Installation
------------
#### Docker installation
You can set up CSPstealer using Docker for easy deployment:
```
docker-compose up -d
```
Modify the default credentials to access the admin panel:
```
docker exec -it csp_stealer python credentials.py
```

By default, the application runs on port 80. If you need to change the port, modify the docker-compose.yaml file.      



        
#### Using Python (without Docker)
Alternatively, you can set up CSPstealer without Docker for manual deployment. Python 3.6 or higher is required to run CSPstealer.
```
pip3 install -r requirements.txt
python3 credentials.py # change default credentials
./gunicorn.sh # run app
```


#### SSL configuration (optional)
If you need HTTPS, you can place `cert.crt` and `private.key` files in the `./ssl` directory.  
Please note that SSL is not required for successful exploitation; however, data will be transmitted over an unencrypted channel. 

Usage
------------

The application is accessible on http[s]://0.0.0.0/admin page.

Default Credentials: admin / cspstealer   

Note: It is strongly recommended to change the default credentials.

# License
CSPstealer is licensed under the MIT License.

