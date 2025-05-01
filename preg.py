from urllib.parse import urlparse, parse_qs, unquote

def parse_wireguard_url():
    print("Введите URL WireGuard в формате:")
    print("wireguard://PrivateKey@ServerIP:Port?param1=value1&param2=value2")
    print("Или просто вставьте ссылку, которую вам прислали:")
    
    url = input("> ").strip()
    
    if not url.startswith('wireguard://'):
        url = 'wireguard://' + url
    
    try:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        
        private_key = unquote(parsed.username)
        endpoint = parsed.hostname
        port = parsed.port
        address = unquote(query.get('address', [''])[0])
        public_key = unquote(query.get('publickey', [''])[0])
        mtu = query.get('mtu', ['1280'])[0]
        keepalive = query.get('keepalive', ['25'])[0]
        
        config = f"""[Interface]
PrivateKey = {private_key}
Address = {address}
DNS = 8.8.8.8
MTU = {mtu}

[Peer]
PublicKey = {public_key}
Endpoint = {endpoint}:{port}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = {keepalive}"""
        
        print("\nГотовый конфиг WireGuard:\n")
        print(config)
        
        with open('wg.conf', 'w') as f:
            f.write(config)
        print("\nКонфиг также сохранен в файл 'wg0.conf'")
        
    except Exception as e:
        print(f"Неверный формат URL: {e}")

if __name__ == "__main__":
    parse_wireguard_url()
