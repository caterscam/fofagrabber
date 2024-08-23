import requests
from bs4 import BeautifulSoup
import socket
import time

# Menampilkan banner
def print_banner():
    banner = """
        
    █▀▀ █▀█ █▀▀ ▄▀█ ░ █ █▄░█ █▀▀ █▀█   █▀▀ █▀█ ▄▀█ █▄▄ █▄▄ █▀▀ █▀█
    █▀░ █▄█ █▀░ █▀█ ▄ █ █░▀█ █▀░ █▄█   █▄█ █▀▄ █▀█ █▄█ █▄█ ██▄ █▀▄
                    devel0perz t.me/devonaji
    """
    print(banner)

# URL yang akan diambil
url = 'https://en.fofa.info/result?qbase64=YXBpLncub3Jn'

# User-Agent untuk header HTTP
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

def get_domain_from_ip(ip):
    try:
        # Melakukan reverse DNS lookup untuk mendapatkan domain dari IP
        domain = socket.gethostbyaddr(ip)
        return domain[0]  # Mengembalikan nama domain
    except socket.herror:
        return None  # Jika tidak ada domain yang ditemukan

def fetch_data():
    try:
        # Mengirim permintaan GET ke URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Memastikan permintaan berhasil

        # Parsing konten HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Temukan semua tag yang diinginkan, misalnya <a> untuk link
        links = soup.find_all('a')

        # Ambil dan tampilkan domain dari atribut href tag <a>
        domains = set()  # Menggunakan set untuk menghindari duplikat
        for link in links:
            href = link.get('href', '')
            if href:
                parts = href.split('/')
                if len(parts) > 2:
                    # Mendapatkan domain dari URL
                    domain = parts[2]
                    if domain and 'No domain found' not in domain:
                        domains.add(domain)
                else:
                    # Jika tidak ada domain, cek apakah ini IP
                    ip = parts[0]
                    try:
                        # Mengecek apakah IP valid
                        socket.inet_aton(ip)
                        # Mendapatkan domain dari IP
                        domain = get_domain_from_ip(ip)
                        if domain:
                            domains.add(domain)
                    except socket.error:
                        # Jika IP tidak valid, abaikan
                        continue

        return domains

    except requests.RequestException as e:
        print(f'Error during requests to {url}: {str(e)}')
        return set()

def save_results(domains, filename):
    with open(filename, 'a') as file:
        for domain in domains:
            file.write(f'{domain}\n')
    print(f'[*] Results saved to {filename}')

def display_domains():
    displayed_domains = set()

    # Menampilkan menu untuk menyimpan hasil
    filename = input('[*] Enter filename to save results (e.g., results.txt): ').strip()

    while True:
        new_domains = fetch_data()
        new_domains_to_display = new_domains - displayed_domains
        if new_domains_to_display:
            for domain in new_domains_to_display:
                print(domain)  # Tampilkan domain baru di terminal
            displayed_domains.update(new_domains_to_display)

            # Simpan hasil ke file setiap detik
            save_results(displayed_domains, filename)
        
        time.sleep(1)  # Delay selama 1 detik

if __name__ == "__main__":
    print_banner()
    display_domains()
