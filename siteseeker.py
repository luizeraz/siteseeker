import argparse
import requests
import socket
import re
import whois

def get_domain(url):
    protocol, domain = url.split("://") if "://" in url else ("http", url)
    return protocol, domain.split("/")[0]

def get_ip(host):
    return socket.gethostbyname(host)

def display_web_server(headers):
    print(f'Server: {headers.get("Server")}')

def detect_cms(headers, webpage):
    detected_systems = []
    
    powered_by = headers.get('X-Powered-By', '')
    if 'WordPress' in powered_by:
        detected_systems.append('WordPress')
    if 'Joomla' in powered_by:
        detected_systems.append('Joomla')
    
    if any(s in webpage for s in ['/wp-content/', '/joomla/', '/sites/default/']):
        detected_systems.extend(['WordPress', 'Joomla', 'Drupal'])
    
    return detected_systems

def display_whois_info(domain):
    try:
        info = whois.whois(domain)
        print(f'WHOIS Information for {domain}')
        print(f'Created: {info.creation_date}')
        print(f'Expires: {info.expiration_date}')
        print(f'Registrar: {info.registrar}')
    except whois.parser.PywhoisError as e:
        print(f'WHOIS Information not available.')
        print(f'Error retrieving WHOIS information: {str(e)}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get website information")
    parser.add_argument("url", type=str, help="URL of the website to obtain information")

    args = parser.parse_args()
    url = args.url

    try:
        protocol, domain = get_domain(url)
        full_url = f"{protocol}://{domain}"
        site = requests.get(full_url)
        status = site.status_code

        ascii_logo = """
  ██████  ██▓▄▄▄█████▓▓█████      ██████ ▓█████ ▓█████  ██ ▄█▀▓█████  ██▀███  
▒██    ▒ ▓██▒▓  ██▒ ▓▒▓█   ▀    ▒██    ▒ ▓█   ▀ ▓█   ▀  ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
░ ▓██▄   ▒██▒▒ ▓██░ ▒░▒███      ░ ▓██▄   ▒███   ▒███   ▓███▄░ ▒███   ▓██ ░▄█ ▒
  ▒   ██▒░██░░ ▓██▓ ░ ▒▓█  ▄      ▒   ██▒▒▓█  ▄ ▒▓█  ▄ ▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
▒██████▒▒░██░  ▒██▒ ░ ░▒████▒   ▒██████▒▒░▒████▒░▒████▒▒██▒ █▄░▒████▒░██▓ ▒██▒
▒ ▒▓▒ ▒ ░░▓    ▒ ░░   ░░ ▒░ ░   ▒ ▒▓▒ ▒ ░░░ ▒░ ░░░ ▒░ ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░▒  ░ ░ ▒ ░    ░     ░ ░  ░   ░ ░▒  ░ ░ ░ ░  ░ ░ ░  ░░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
░  ░  ░   ▒ ░  ░         ░      ░  ░  ░     ░      ░   ░ ░░ ░    ░     ░░   ░ 
      ░   ░              ░  ░         ░     ░  ░   ░  ░░  ░      ░  ░   ░     

  Created by: luizera
  GitHub: https://github.com/luizeraz
------------------------------------------------------------------------------"""

        print(ascii_logo)

        print(f'Domain: {domain}')
        host = domain
        ip = get_ip(host)
        print(f'IP of {host}: {ip}')

        display_web_server(site.headers)

        detected_systems = detect_cms(site.headers, site.text)
        if detected_systems:
            print(f'Detected CMS: {", ".join(detected_systems)}')
        else:
            print('No CMS detected.')
        
        display_whois_info(domain)

    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
