import os
import sys
import time
import random
import threading
import subprocess
import re
import urllib.parse

# --- AUTOMATIC DEPENDENCY INSTALLER (FIXED FOR EXTERNALLY-MANAGED ENVIRONMENT) ---
def install_dependencies():
    dependencies = ['requests', 'urllib3', 'selenium', 'beautifulsoup4']
    missing = []
    for pkg in dependencies:
        try:
            # beautifulsoup4 diimport sebagai bs4
            __import__(pkg.replace('-', '_'))
        except ImportError:
            missing.append(pkg)

    if not missing:
        return

    print(f"\n[\033[93m!\033[0m] Missing dependencies: {', '.join(missing)}")
    print("    Attempting to install...")

    # Cek apakah apt tersedia (Debian/Ubuntu)
    try:
        subprocess.run(['which', 'apt'], check=True, capture_output=True)
        use_apt = True
    except:
        use_apt = False

    installed_via_apt = []
    if use_apt:
        apt_map = {
            'requests': 'python3-requests',
            'urllib3': 'python3-urllib3',
            'selenium': 'python3-selenium',
            'beautifulsoup4': 'python3-bs4'
        }
        for pkg in missing:
            apt_pkg = apt_map.get(pkg)
            if apt_pkg:
                try:
                    print(f"    Installing {apt_pkg} via apt...")
                    subprocess.check_call(['sudo', 'apt', 'install', '-y', apt_pkg],
                                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    installed_via_apt.append(pkg)
                except Exception:
                    pass

    still_missing = [p for p in missing if p not in installed_via_apt]
    if still_missing:
        for pkg in still_missing:
            try:
                print(f"    Installing {pkg} via pip (--break-system-packages)...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg,
                                       "--break-system-packages", "--quiet"])
            except:
                try:
                    print(f"    Installing {pkg} via pip (--user)...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg,
                                           "--user", "--quiet"])
                except Exception as e:
                    print(f"\n[\033[91m✘\033[0m] Failed to install {pkg}.")
                    print("    Please install manually with:")
                    print(f"        pip install {pkg} --break-system-packages")
                    print("    or use a virtual environment.\n")
                    sys.exit(1)

    print("[\033[92m✔\033[0m] All dependencies installed successfully.\n")

install_dependencies()

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import bs4  # BeautifulSoup untuk parsing HTML ringan

# Optimalisasi Jaringan Dasar & DNS Bypass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.util.connection.HAS_IPV6 = False

# Pengaturan Warna Terminal untuk Antarmuka EVO+ v4.1
class Color:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'
    BG_CYAN = '\033[46m'

# Database 50+ User-Agent Premium (Pembaruan Masif Android 12-15 & Desktop 2024-2025)
USER_AGENTS = [
    # --- ANDROID (SAMSUNG, PIXEL, XIAOMI, OPPO, VIVO, REALME) ---
    "Mozilla/5.0 (Linux; Android 15; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-A556B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; 23127PN0CG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; M2101K6G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; 2201116SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; CPH2381) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; V2202) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; motorola edge 30 pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; NE2215) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; RMX3301) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-F731B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-F946B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; vivo 1906) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
    
    # --- iOS DEVICES (iPhone & iPad) ---
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.7 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",

    # --- DESKTOP HIGH-END (Windows, macOS, Linux) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
]

# Database Rujukan (Referrer) Skala Global (100+ Media Internasional & Sosial Media)
REFERRERS = {
    "1": [ # Media Sosial Global yang Diperluas
        "https://www.facebook.com/", "https://m.facebook.com/", "https://l.facebook.com/",
        "https://t.co/", "https://x.com/", "https://twitter.com/",
        "https://www.instagram.com/", "https://l.instagram.com/",
        "https://www.tiktok.com/", "https://www.reddit.com/", "https://www.linkedin.com/",
        "https://www.pinterest.com/", "https://www.tumblr.com/", "https://www.snapchat.com/",
        "https://vk.com/", "https://weibo.com/", "https://www.quora.com/"
    ],
    "2": [ # Mesin Pencari Utama (Dipertahankan & Diperkuat)
        "https://www.google.com/", "https://www.google.co.id/", "https://www.bing.com/",
        "https://duckduckgo.com/", "https://search.yahoo.com/", "https://yandex.com/",
        "https://www.ecosia.org/", "https://www.baidu.com/", "https://www.qwant.com/"
    ],
    "3": [ # 100+ Portal Berita Internasional (Otoritas Sangat Tinggi)
        # --- Amerika Serikat & Eropa ---
        "https://www.cnn.com/", "https://www.nytimes.com/", "https://www.washingtonpost.com/", 
        "https://www.wsj.com/", "https://www.foxnews.com/", "https://www.nbcnews.com/", 
        "https://www.usatoday.com/", "https://www.bloomberg.com/", "https://www.cnbc.com/", 
        "https://www.reuters.com/", "https://www.apnews.com/", "https://www.npr.org/", 
        "https://www.latimes.com/", "https://www.nypost.com/", "https://www.forbes.com/",
        "https://www.bbc.com/", "https://www.theguardian.com/", "https://www.dailymail.co.uk/", 
        "https://www.telegraph.co.uk/", "https://www.independent.co.uk/", "https://www.ft.com/", 
        "https://www.thetimes.co.uk/", "https://www.france24.com/", "https://www.lemonde.fr/", 
        "https://www.dw.com/", "https://www.spiegel.de/", "https://www.elpais.com/",
        # --- Timur Tengah ---
        "https://www.aljazeera.com/", "https://www.arabnews.com/", "https://www.gulfnews.com/", 
        "https://www.thenationalnews.com/", "https://www.khaleejtimes.com/", "https://www.jpost.com/", 
        "https://www.haaretz.com/", "https://www.timesofisrael.com/", "https://www.middleeasteye.net/",
        "https://www.dailysabah.com/", "https://www.hurriyetdailynews.com/",
        # --- Asia Timur ---
        "https://www.scmp.com/", "https://www.japantimes.co.jp/", "https://www.yomiuri.co.jp/", 
        "https://www.asahi.com/", "https://www.mainichi.jp/", "https://www.koreatimes.co.kr/", 
        "https://www.koreaherald.com/", "https://en.yna.co.kr/", "https://www.xinhuanet.com/", 
        "https://www.globaltimes.cn/", "https://www.taipeitimes.com/", "https://www.chinadaily.com.cn/",
        # --- Asia Tenggara ---
        "https://www.straitstimes.com/", "https://www.channelnewsasia.com/", "https://www.bangkokpost.com/", 
        "https://www.thestar.com.my/", "https://www.nst.com.my/", "https://www.malaysiakini.com/", 
        "https://www.philstar.com/", "https://newsinfo.inquirer.net/", "https://www.rappler.com/", 
        "https://e.vnexpress.net/", "https://tuoitrenews.vn/", "https://www.vietnamnet.vn/",
        # --- Indonesia ---
        "https://www.kompas.com/", "https://www.detik.com/", "https://www.tribunnews.com/", 
        "https://www.cnnindonesia.com/", "https://www.kumparan.com/", "https://www.liputan6.com/", 
        "https://www.merdeka.com/", "https://www.suara.com/", "https://www.viva.co.id/", 
        "https://www.okezone.com/", "https://www.antaranews.com/", "https://www.republika.co.id/", 
        "https://www.sindonews.com/", "https://www.jpnn.com/", "https://www.pikiran-rakyat.com/", 
        "https://www.cnbcindonesia.com/", "https://www.bisnis.com/", "https://www.investor.id/"
    ]
}

TEXT = {
    "EN": {
        "title": "ULTIMATE WEB & MEDIA ENGINE",
        "subtitle": "E V O L U T I O N   +   V 4 . 1",
        "select_lang": "Select Language / Pilih Bahasa:",
        "ask_mode": "Select Execution Mode:",
        "mode_1": "1. Advanced HTTP Injection (Supports Shortlinks & Anti-Drop)",
        "mode_2": "2. Authentic Media Engagement (Video/Browser Engine)",
        "ask_url": "Enter Target URL (Shortlinks allowed, e.g., bit.ly, s.id): ",
        "err_url": "Error: Invalid URL format!",
        "ask_ref": "Select Traffic Origin Network:",
        "ref_1": "1. Social Media Ecosystems (FB, X, IG, TikTok, Reddit, etc.)",
        "ref_2": "2. Global Search Authorities (Google, Bing, Yahoo, Yandex)",
        "ref_3": "3. 100+ International News Portals (Asia, EU, US, MENA)",
        "ref_4": "4. Hybrid Mix (Highly Recommended for Organic Profile)",
        "ask_choice": "Selection: ",
        "ask_hits": "Total Visits to Deliver: ",
        "ask_threads": "Worker Threads (Web: 10-50 | Media: 1-5): ",
        "ask_duration": "Watch Duration in Seconds (e.g., 30): ",
        "err_val": "Error: Please enter a valid number!",
        "init": "[!] Initializing distributed traffic protocol...",
        "resolving": "[*] Resolving shortlink to actual destination...",
        "success": "SUCCESS",
        "fail": "FAILED",
        "host": "Origin",
        "conn_err": "NETWORK DROPPED",
        "completed": "Task Completed",
        "all_done": "✔ ALL VISITS DELIVERED SUCCESSFULLY.",
        "press_exit": "Press Enter to exit...",
        "interrupted": "Task terminated by user.",
        "watching": "Engaging"
    },
    "ID": {
        "title": "MESIN WEB & MEDIA ULTIMAT",
        "subtitle": "E D I S I   E V O L U S I   +   V 4 . 1",
        "select_lang": "Pilih Bahasa / Select Language:",
        "ask_mode": "Pilih Mode Eksekusi:",
        "mode_1": "1. Injeksi HTTP Lanjutan (Mendukung Tautan Pendek & Anti-Gagal)",
        "mode_2": "2. Keterlibatan Media Otentik (Mesin Peramban/Video)",
        "ask_url": "Masukkan Alamat URL (Mendukung tautan pendek seperti bit.ly, s.id): ",
        "err_url": "Kesalahan: Format URL tidak valid!",
        "ask_ref": "Pilih Jaringan Sumber Trafik:",
        "ref_1": "1. Ekosistem Media Sosial (FB, X, IG, TikTok, Reddit, dll)",
        "ref_2": "2. Otoritas Pencarian Global (Google, Bing, Yahoo, Yandex)",
        "ref_3": "3. 100+ Portal Berita Internasional (Asia, Eropa, AS, TimTeng)",
        "ref_4": "4. Campuran Hibrida (Sangat Disarankan untuk Profil Organik)",
        "ask_choice": "Pilihan: ",
        "ask_hits": "Total Kunjungan yang Didistribusikan: ",
        "ask_threads": "Jalur Pekerja (Web: 10-50 | Media: 1-5): ",
        "ask_duration": "Durasi Kunjungan/Tonton dalam Detik (Contoh: 30): ",
        "err_val": "Kesalahan: Harap masukkan angka yang valid!",
        "init": "[!] Memulai protokol distribusi trafik...",
        "resolving": "[*] Mengurai tautan pendek ke tujuan asli...",
        "success": "BERHASIL",
        "fail": "GAGAL",
        "host": "Asal",
        "conn_err": "JARINGAN TERPUTUS",
        "completed": "Tugas Selesai",
        "all_done": "✔ SELURUH KUNJUNGAN TELAH BERHASIL DIDISTRIBUSIKAN.",
        "press_exit": "Tekan Enter untuk keluar...",
        "interrupted": "Tugas dihentikan oleh pengguna.",
        "watching": "Menonton"
    }
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def resolve_shortlink(url, lang):
    """Membuka tautan pendek untuk mendapatkan URL domain utama sebenarnya."""
    print(f"{Color.CYAN}{TEXT[lang]['resolving']}{Color.END}")
    try:
        session = requests.Session()
        response = session.head(url, allow_redirects=True, timeout=15)
        real_url = response.url
        print(f"{Color.GREEN}[+] Target Asli / Real Target: {real_url}{Color.END}\n")
        return real_url
    except Exception as e:
        print(f"{Color.YELLOW}[!] Resolving lambat, menggunakan URL bawaan...{Color.END}\n")
        return url

def get_optimized_session():
    """
    Sesi tingkat lanjut untuk memperbaiki masalah DNS dan koneksi Failed.
    Pool diperbesar, dan penyesuaian Retry ditambahkan agar lebih stabil.
    """
    session = requests.Session()
    retry = Retry(
        total=4, 
        backoff_factor=0.2, 
        status_forcelist=[403, 406, 429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(pool_connections=500, pool_maxsize=500, max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def generate_advanced_headers(ref_url, ua):
    """Injeksi header kelas berat untuk memanipulasi deteksi firewall."""
    if "Android" in ua:
        is_mobile, platform = "?1", '"Android"'
    elif "iPhone" in ua or "iPad" in ua:
        is_mobile, platform = "?1", '"iOS"'
    elif "Windows" in ua:
        is_mobile, platform = "?0", '"Windows"'
    elif "Macintosh" in ua:
        is_mobile, platform = "?0", '"macOS"'
    else:
        is_mobile, platform = "?0", '"Linux"'
        
    return {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": ref_url,
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "sec-ch-ua-mobile": is_mobile,
        "sec-ch-ua-platform": platform
    }

# ========== FITUR ANTI-JINGLING TAMBAHAN (TIDAK MENGUBAH TAMPILAN) ==========

def fetch_and_simulate_assets(session, base_url, html_content, lang):
    """
    [ANTI-JINGLING] Setelah load halaman utama, ambil beberapa resource statis
    (CSS, JS, gambar) untuk mensimulasikan perilaku browser sungguhan.
    """
    try:
        soup = bs4.BeautifulSoup(html_content, 'html.parser')
        asset_urls = set()
        parsed_base = urllib.parse.urlparse(base_url)
        base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"

        # Ambil link CSS
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                full_url = urllib.parse.urljoin(base_url, href)
                if full_url.startswith(base_domain):
                    asset_urls.add(full_url)

        # Ambil script JS
        for script in soup.find_all('script', src=True):
            src = script.get('src')
            full_url = urllib.parse.urljoin(base_url, src)
            if full_url.startswith(base_domain):
                asset_urls.add(full_url)

        # Ambil gambar (acak 3-5 gambar)
        imgs = soup.find_all('img', src=True)
        random.shuffle(imgs)
        for img in imgs[:random.randint(3, 6)]:
            src = img.get('src')
            full_url = urllib.parse.urljoin(base_url, src)
            if full_url.startswith(base_domain):
                asset_urls.add(full_url)

        # Request aset secara berurutan dengan jeda kecil
        for asset in list(asset_urls)[:8]:  # maksimal 8 aset
            try:
                time.sleep(random.uniform(0.2, 0.6))
                session.get(asset, timeout=8, verify=False)
            except:
                pass
    except Exception as e:
        # Jika parsing gagal (misal tidak ada bs4), lewati
        pass

def simulate_human_http_behavior(session, target, lang, response):
    """
    [ANTI-JINGLING] Simulasikan perilaku manusia setelah load halaman utama:
    - Tunggu beberapa detik (membaca)
    - Muat aset statis (jika HTML tersedia)
    """
    # Waktu membaca acak 2-7 detik
    read_time = random.uniform(2.0, 7.0)
    time.sleep(read_time)
    # Coba parsing HTML jika tipe konten mendukung
    if 'text/html' in response.headers.get('Content-Type', ''):
        fetch_and_simulate_assets(session, target, response.text, lang)

def simulate_human_selenium_behavior(driver, duration, lang):
    """
    [ANTI-JINGLING] Simulasikan interaksi manusia di browser:
    - Scroll bertahap
    - Gerakan mouse acak
    - Klik tautan internal secara acak (jika memungkinkan)
    - Menangani popup cookie consent sederhana
    """
    try:
        # Tangani popup cookie / GDPR sederhana (coba klik tombol "Accept" atau "Setuju")
        try:
            accept_buttons = driver.find_elements(By.XPATH, 
                "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept') or "
                "contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'setuju') or "
                "contains(@id, 'cookie') or contains(@class, 'cookie')]")
            for btn in accept_buttons[:2]:
                try:
                    btn.click()
                    time.sleep(0.5)
                except:
                    pass
        except:
            pass

        # Dapatkan tinggi halaman
        total_height = driver.execute_script("return document.body.scrollHeight")
        viewport_height = driver.execute_script("return window.innerHeight")
        
        # Scroll bertahap
        current_scroll = 0
        steps = random.randint(3, 7)
        for _ in range(steps):
            scroll_amount = random.randint(100, min(400, total_height - current_scroll))
            current_scroll += scroll_amount
            driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
            time.sleep(random.uniform(0.5, 1.5))
            
            # Gerakan mouse acak (jika memungkinkan)
            try:
                action = ActionChains(driver)
                x_offset = random.randint(-100, 100)
                y_offset = random.randint(-50, 50)
                action.move_by_offset(x_offset, y_offset).perform()
                action.reset_actions()
            except:
                pass

        # Scroll ke atas lagi secara perlahan
        driver.execute_script("window.scrollTo({ top: 0, behavior: 'smooth' })")
        time.sleep(1.5)

        # Jika durasi > 20 detik, coba klik link internal secara acak
        if duration > 20:
            try:
                links = driver.find_elements(By.TAG_NAME, 'a')
                internal_links = []
                current_url = driver.current_url
                domain = urllib.parse.urlparse(current_url).netloc
                for link in links:
                    href = link.get_attribute('href')
                    if href and domain in href and not href.startswith('javascript'):
                        internal_links.append(link)
                if internal_links:
                    chosen_link = random.choice(internal_links)
                    # Scroll ke link
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", chosen_link)
                    time.sleep(1)
                    chosen_link.click()
                    # Tunggu sebentar di halaman baru
                    time.sleep(random.uniform(3, 5))
                    driver.back()
            except Exception:
                pass

    except Exception as e:
        # Abaikan error saat simulasi
        pass

# ========== FUNGSI UTAMA YANG DIPERBARUI DENGAN ANTI-JINGLING ==========

def run_http_worker(target, ref_choice, visits, thread_id, lang):
    """Mode 1: Arsitektur Eksekusi Hibrida - Distribusi HTTP tingkat tinggi + Anti-Jingling."""
    session = get_optimized_session()
    success, failed = 0, 0
    
    # Warm-Up Connection
    initial_ua = random.choice(USER_AGENTS)
    try:
        session.get(target, headers=generate_advanced_headers("https://www.google.com/", initial_ua), timeout=8, verify=False)
    except:
        pass 
    
    for _ in range(visits):
        if ref_choice == "4":
            category = random.choice(list(REFERRERS.values()))
            ref = random.choice(category)
        else:
            ref = random.choice(REFERRERS.get(ref_choice, REFERRERS["2"]))
            
        ua = random.choice(USER_AGENTS)
        headers = generate_advanced_headers(ref, ua)
        
        try:
            response = session.get(target, headers=headers, timeout=10, verify=False)
            
            if response.status_code < 400:
                success += 1
                status = f"{Color.GREEN}{TEXT[lang]['success']}{Color.END}"
                # --- ANTI-JINGLING: simulasi perilaku setelah sukses ---
                simulate_human_http_behavior(session, target, lang, response)
            else:
                failed += 1
                status = f"{Color.RED}{TEXT[lang]['fail']} {response.status_code}{Color.END}"
                
            origin_name = ref.split('/')[2].replace("www.", "")
            print(f" {Color.CYAN}[Jalur-{thread_id:02d}]{Color.END} {status} | {TEXT[lang]['host']}: {origin_name}")
            
        except requests.exceptions.Timeout:
            failed += 1
            print(f" {Color.YELLOW}[Jalur-{thread_id:02d}] {TEXT[lang]['conn_err']}{Color.END}")
        except Exception:
            failed += 1
            print(f" {Color.RED}[Jalur-{thread_id:02d}] {TEXT[lang]['fail']}{Color.END}")
        
        time.sleep(random.uniform(0.1, 0.4))

    print(f"\n{Color.BOLD}>> Jalur-{thread_id:02d} {TEXT[lang]['completed']}. (Berhasil/Success: {success}, Gagal/Failed: {failed}){Color.END}")

def run_browser_worker(target, visits, thread_id, lang, duration):
    """Mode 2: Keterlibatan Media Otentik (Authentic Media Engagement) - Bypass Anti-Bot Lanjutan + Anti-Jingling."""
    success, failed = 0, 0
    
    for visit_num in range(visits):
        driver = None
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--mute-audio")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--disable-notifications")
            
            # Anti-Bot Bypass lebih kuat
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-web-security")  # untuk bypass beberapa batasan
            
            # Resolusi layar acak
            window_sizes = ["1920,1080", "1366,768", "1440,900", "1536,864", "1280,720"]
            chrome_options.add_argument(f"--window-size={random.choice(window_sizes)}")
            
            ua = random.choice(USER_AGENTS)
            chrome_options.add_argument(f"user-agent={ua}")
            
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_argument('--silent')

            driver = webdriver.Chrome(options=chrome_options)
            
            # Sembunyikan jejak webdriver
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                      get: () => undefined
                    });
                    Object.defineProperty(navigator, 'plugins', {
                      get: () => [1, 2, 3, 4, 5]
                    });
                    Object.defineProperty(navigator, 'languages', {
                      get: () => ['en-US', 'en']
                    });
                """
            })

            print(f" {Color.MAGENTA}[Peramban-{thread_id:02d}]{Color.END} Mengakses kunjungan ke-{visit_num+1}...")
            driver.set_page_load_timeout(35)
            driver.get(target)
            
            # Interaksi video (jika ada)
            try:
                driver.execute_script("""
                    let vids = document.getElementsByTagName('video'); 
                    if(vids.length > 0) {
                        vids[0].muted = true;
                        vids[0].play();
                    }
                """)
            except:
                pass

            # --- ANTI-JINGLING: simulasi manusia sebelum durasi utama ---
            simulate_human_selenium_behavior(driver, duration, lang)
            
            print(f" {Color.GREEN}[Peramban-{thread_id:02d}]{Color.END} {TEXT[lang]['watching']} ({duration} detik)...")
            time.sleep(duration)
            
            success += 1
            print(f" {Color.CYAN}[Peramban-{thread_id:02d}]{Color.END} Kunjungan {visit_num+1} {Color.GREEN}{TEXT[lang]['success']}{Color.END}")
            
        except Exception as e:
            failed += 1
            print(f" {Color.RED}[Peramban-{thread_id:02d}] {TEXT[lang]['fail']}{Color.END}")
        finally:
            if driver:
                driver.quit()

    print(f"\n{Color.BOLD}>> Mesin Peramban-{thread_id:02d} {TEXT[lang]['completed']}. (Berhasil/Success: {success}, Gagal/Failed: {failed}){Color.END}")

def main():
    clear_screen()
    print(f"{Color.BOLD}{Color.CYAN}")
    print("    1. English")
    print("    2. Bahasa Indonesia")
    print(f"{Color.END}")
    
    lang_choice = input(f"{Color.BOLD}Select Language / Pilih Bahasa (1/2): {Color.END}").strip()
    lang = "EN" if lang_choice == "1" else "ID"

    clear_screen()
    print(f"""{Color.BOLD}{Color.CYAN}
    ██╗  ██╗██████╗  ██████╗  ██████╗ ███████╗████████╗███████╗██████╗ ███████╗
    ╚██╗██╔╝██╔══██╗██╔═══██╗██╔═══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔════╝
     ╚███╔╝ ██████╔╝██║   ██║██║   ██║███████╗   ██║   █████╗  ██████╔╝███████╗
     ██╔██╗ ██╔══██╗██║   ██║██║   ██║╚════██║   ██║   ██╔══╝  ██╔══██╗╚════██║
    ██╔╝ ██╗██████╔╝╚██████╔╝╚██████╔╝███████║   ██║   ███████╗██║  ██║███████║
    ╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝
    {Color.MAGENTA}======================================================================
    {Color.END}{Color.BOLD}{Color.BG_CYAN} {TEXT[lang]['subtitle'].center(68)} {Color.END}
    """)

    print(f"{Color.BOLD}{TEXT[lang]['ask_mode']}{Color.END}")
    print(f" {Color.CYAN}{TEXT[lang]['mode_1']}{Color.END}")
    print(f" {Color.MAGENTA}{TEXT[lang]['mode_2']}{Color.END}")
    mode_type = input(f"{Color.YELLOW}{TEXT[lang]['ask_choice']}{Color.END}").strip()

    if mode_type not in ['1', '2']:
        mode_type = '1'

    print("-" * 70)

    target_url = input(f"{Color.BOLD}{TEXT[lang]['ask_url']}{Color.END}").strip()
    if not target_url.startswith("http"):
        print(f"{Color.RED}{TEXT[lang]['err_url']}{Color.END}")
        return

    # Terapkan fungsi pemecah tautan pendek (Shortlink Resolver)
    target_url = resolve_shortlink(target_url, lang)

    ref_choice = "4"
    watch_duration = 0

    if mode_type == '1':
        print(f"\n{Color.BOLD}{TEXT[lang]['ask_ref']}{Color.END}")
        for k, v in TEXT[lang].items():
            if k.startswith('ref_'): print(f" {v}")
        ref_choice = input(f"{Color.CYAN}{TEXT[lang]['ask_choice']}{Color.END}").strip()
    else:
        try:
            watch_duration = int(input(f"\n{Color.MAGENTA}{TEXT[lang]['ask_duration']}{Color.END}"))
        except ValueError:
            print(f"{Color.RED}{TEXT[lang]['err_val']}{Color.END}")
            return

    try:
        total_visits = int(input(f"\n{Color.BOLD}{TEXT[lang]['ask_hits']}{Color.END}"))
        thread_count = int(input(f"{Color.BOLD}{TEXT[lang]['ask_threads']}{Color.END}"))
    except ValueError:
        print(f"{Color.RED}{TEXT[lang]['err_val']}{Color.END}")
        return

    visits_per_thread = total_visits // thread_count
    remaining = total_visits % thread_count

    print(f"\n{Color.GREEN}{TEXT[lang]['init']}{Color.END}\n")
    
    threads = []
    for i in range(thread_count):
        count = visits_per_thread + (remaining if i == 0 else 0)
        if count > 0:
            if mode_type == '1':
                t = threading.Thread(target=run_http_worker, args=(target_url, ref_choice, count, i+1, lang))
            else:
                t = threading.Thread(target=run_browser_worker, args=(target_url, count, i+1, lang, watch_duration))
            
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

    print(f"\n{Color.BOLD}{Color.BG_CYAN}  {TEXT[lang]['all_done']}  {Color.END}")
    input(f"\n{TEXT[lang]['press_exit']}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Color.RED} \n[!] {TEXT.get('EN', {}).get('interrupted', 'Task Interrupted')} / {TEXT.get('ID', {}).get('interrupted', 'Tugas Dihentikan')}.{Color.END}")
        sys.exit()