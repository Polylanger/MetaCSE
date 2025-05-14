import requests


def fofa_search_resource(key):
    params = {
        "key": key
    }
    try:
        resp = requests.get('https://fofa.info/api/v1/info/my', data=params)
        data = resp.json()
        if "'error': True" in str(data):
            return f"[!] Error: {data['errmsg']}\n"
        string = f"======== Fofa ========\n[+] Email: {data['email']}\n[+] Username: {data['username']}\n[+] Fcoin: {data['fcoin']}\n[+] isVip: {data['isvip']}\n[+] Vip_level: {data['vip_level']}\n[+] is_Verified: {data['is_verified']}\n[+] Avatar: {data['avatar']}\n========================\n"
        return string
    except Exception as e:
        return e
