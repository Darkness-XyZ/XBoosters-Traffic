import os
import sys
import time
import random
import threading
import subprocess

# --- AUTOMATIC DEPENDENCY INSTALLER ---
def install_dependencies():
    dependencies = ['requests', 'urllib3', 'selenium']
    for pkg in dependencies:
        try:
            __import__(pkg)
        except ImportError:
            print(f"\n[\033[93m!\033[0m] Menginstal pustaka yang dibutuhkan: {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])
            print(f"[\033[92m✔\033[0m] {pkg} berhasil diinstal.")

install_dependencies()

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Pengaturan Warna Terminal untuk Antarmuka EVO+ (BETA)
class Color:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'
    BG_MAGENTA = '\033[45m'

# Database 35+ User-Agent Premium (Fokus Android 13 + Desktop Mutakhir 2024-2025)
USER_AGENTS = [
    # --- ANDROID 13 DEVICES ---
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", # Galaxy S23 Ultra
    "Mozilla/5.0 (Linux; Android 13; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36", # Galaxy A54
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", # Pixel 7 Pro
    "Mozilla/5.0 (Linux; Android 13; Pixel 6a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", # Pixel 6a
    "Mozilla/5.0 (Linux; Android 13; M2101K6G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36", # Xiaomi Redmi Note 10 Pro
    "Mozilla/5.0 (Linux; Android 13; 2201116SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", # Poco X4 Pro
    "Mozilla/5.0 (Linux; Android 13; CPH2381) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", # Oppo Reno 8
    "Mozilla/5.0 (Linux; Android 13; V2202) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36", # Vivo T1
    "Mozilla/5.0 (Linux; Android 13; motorola edge 30 pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", # Motorola
    "Mozilla/5.0 (Linux; Android 13; NE2215) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", # OnePlus 10 Pro
    "Mozilla/5.0 (Linux; Android 13; RMX3301) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", # Realme GT 2 Pro
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", # Galaxy S21 Ultra
    "Mozilla/5.0 (Linux; Android 13; SM-F721B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36", # Galaxy Z Flip 4
    "Mozilla/5.0 (Linux; Android 13; SM-F936B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", # Galaxy Z Fold 4
    "Mozilla/5.0 (Linux; Android 13; ASUS_AI2202) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", # Zenfone 9
    
    # --- ANDROID 12 & 14 (Variasi Tambahan) ---
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36",
    
    # --- iOS DEVICES (iPhone & iPad) ---
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",

    # --- DESKTOP HIGH-END (Windows, macOS, Linux) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
]

# Database Rujukan (Referrer) Skala Global Terbaru
REFERRERS = {
    "1": [ # Media Sosial Global
        "https://www.facebook.com/", "https://m.facebook.com/", "https://l.facebook.com/",
        "https://t.co/", "https://x.com/", "https://twitter.com/",
        "https://www.instagram.com/", "https://l.instagram.com/",
        "https://www.tiktok.com/", "https://www.reddit.com/", "https://www.linkedin.com/",
        "https://www.pinterest.com/"
    ],
    "2": [ # Mesin Pencari Utama
        "https://www.google.com/", "https://www.google.co.id/", "https://www.bing.com/",
        "https://duckduckgo.com/", "https://search.yahoo.com/", "https://yandex.com/",
        "https://www.ecosia.org/", "https://www.baidu.com/"
    ],
    "3": [ # Portal Berita Internasional (Otoritas Tinggi)
        "https://www.bbc.com/", "https://www.cnn.com/", "https://www.reuters.com/",
        "https://www.nytimes.com/", "https://www.bloomberg.com/", "https://www.aljazeera.com/",
        "https://www.forbes.com/", "https://www.wsj.com/"
    ]
}

TEXT = {
    "EN": {
        "title": "ULTIMATE WEB & MEDIA ENGINE",
        "subtitle": "E V O L U T I O N   +   B E T A",
        "select_lang": "Select Language / Pilih Bahasa:",
        "ask_mode": "Select Operation Mode:",
        "mode_1": "1. High-Speed Web Traffic (Anti-Fail Fast Protocol)",
        "mode_2": "2. Real Video Watch Metrics (Browser Engine)",
        "ask_url": "Enter Target URL (http:// or https://): ",
        "err_url": "Error: Invalid URL format!",
        "ask_ref": "Select Traffic Origin:",
        "ref_1": "1. Global Social Media (FB, X, IG, TikTok, Reddit)",
        "ref_2": "2. Global Search Engines (Google, Bing, Yahoo, Yandex)",
        "ref_3": "3. International News Portals (BBC, CNN, Reuters, NYT)",
        "ref_4": "4. Mix All Global Sources (Highly Recommended)",
        "ask_choice": "Selection: ",
        "ask_hits": "Total Operations to Deliver: ",
        "ask_threads": "Worker Threads (Web: 10-50 | Video: 1-5): ",
        "ask_duration": "Watch Duration in Seconds (e.g., 30): ",
        "err_val": "Error: Please enter a valid number!",
        "init": "[!] Initializing distributed operations...",
        "success": "SUCCESS",
        "fail": "FAILED",
        "host": "Origin",
        "conn_err": "TIMEOUT/DROPPED",
        "completed": "Completed",
        "all_done": "✔ ALL OPERATIONS COMPLETED SUCCESSFULLY.",
        "press_exit": "Press Enter to exit...",
        "interrupted": "Operation terminated by user.",
        "watching": "Watching"
    },
    "ID": {
        "title": "MESIN WEB & MEDIA ULTIMAT",
        "subtitle": "E D I S I   E V O L U S I   +   (B E T A)",
        "select_lang": "Pilih Bahasa / Select Language:",
        "ask_mode": "Pilih Mode Operasi:",
        "mode_1": "1. Distribusi Trafik Web Berkecepatan Tinggi (Protokol Anti-Gagal)",
        "mode_2": "2. Tayangan Video Nyata (Mesin Peramban/Browser)",
        "ask_url": "Masukkan Alamat URL Target (http:// atau https://): ",
        "err_url": "Kesalahan: Format URL tidak valid!",
        "ask_ref": "Pilih Sumber Rujukan Trafik:",
        "ref_1": "1. Media Sosial Global (FB, X, IG, TikTok, Reddit)",
        "ref_2": "2. Mesin Pencari Global (Google, Bing, Yahoo, Yandex)",
        "ref_3": "3. Portal Berita Internasional (BBC, CNN, Reuters, NYT)",
        "ref_4": "4. Campuran Semua Sumber (Sangat Disarankan)",
        "ask_choice": "Pilihan: ",
        "ask_hits": "Total Operasi yang Didistribusikan: ",
        "ask_threads": "Jalur Pekerja (Web: 10-50 | Video: 1-5): ",
        "ask_duration": "Durasi Tonton dalam Detik (Contoh: 30): ",
        "err_val": "Kesalahan: Harap masukkan angka yang valid!",
        "init": "[!] Memulai operasi terdistribusi...",
        "success": "BERHASIL",
        "fail": "GAGAL",
        "host": "Asal",
        "conn_err": "KONEKSI LAMBAT/TERPUTUS",
        "completed": "Selesai",
        "all_done": "✔ SELURUH OPERASI TELAH DISELESAIKAN DENGAN SUKSES.",
        "press_exit": "Tekan Enter untuk keluar...",
        "interrupted": "Operasi dihentikan oleh pengguna.",
        "watching": "Menonton"
    }
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_optimized_session():
    """
    Sesi dioptimalkan untuk kecepatan maksimum.
    Jeda retry dipersingkat agar tidak menyebabkan efek 'hang/lambat' pada antarmuka.
    """
    session = requests.Session()
    retry = Retry(
        total=3, 
        backoff_factor=0.1, # Backoff diturunkan drastis untuk kecepatan
        status_forcelist=[403, 406, 429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(pool_connections=500, pool_maxsize=500, max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def generate_advanced_headers(ref_url, ua):
    """Menyinkronkan header secara dinamis berdasarkan User-Agent untuk bypass tingkat tinggi."""
    # Deteksi Platform Pintar
    if "Android" in ua:
        is_mobile = "?1"
        platform = '"Android"'
    elif "iPhone" in ua or "iPad" in ua:
        is_mobile = "?1"
        platform = '"iOS"'
    elif "Windows" in ua:
        is_mobile = "?0"
        platform = '"Windows"'
    elif "Macintosh" in ua:
        is_mobile = "?0"
        platform = '"macOS"'
    else:
        is_mobile = "?0"
        platform = '"Linux"'
        
    return {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
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

def run_http_worker(target, ref_choice, hits, thread_id, lang):
    """Jalur pekerja performa tinggi. Lebih cepat, lebih ringan, error-rate sangat rendah."""
    session = get_optimized_session()
    success, failed = 0, 0
    
    # Bypass Warm-Up (Ping awal)
    initial_ua = random.choice(USER_AGENTS)
    try:
        session.get(target, headers=generate_advanced_headers("https://www.google.com/", initial_ua), timeout=5, verify=False)
    except:
        pass 
    
    for _ in range(hits):
        # Penentuan Referrer Dinamis
        if ref_choice == "4":
            category = random.choice(list(REFERRERS.values()))
            ref = random.choice(category)
        else:
            ref = random.choice(REFERRERS.get(ref_choice, REFERRERS["2"]))
            
        ua = random.choice(USER_AGENTS)
        headers = generate_advanced_headers(ref, ua)
        
        try:
            # Timeout 8 detik: Sangat optimal agar thread tidak tersendat (hang) jika server target lambat merespons
            response = session.get(target, headers=headers, timeout=8, verify=False)
            
            if response.status_code < 400:
                success += 1
                status = f"{Color.GREEN}{TEXT[lang]['success']}{Color.END}"
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
        
        # Micro-Delay: Memastikan distribusi yang sangat cepat namun tidak merusak socket jaringan mesin lokal
        time.sleep(random.uniform(0.05, 0.2))

    print(f"\n{Color.BOLD}>> Jalur-{thread_id:02d} {TEXT[lang]['completed']}. (Berhasil: {success}, Gagal: {failed}){Color.END}")

def run_browser_worker(target, hits, thread_id, lang, duration):
    """Jalur pekerja tayangan nyata menggunakan mesin peramban tersembunyi."""
    success, failed = 0, 0
    
    for operation in range(hits):
        driver = None
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--mute-audio")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
            
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

            driver = webdriver.Chrome(options=chrome_options)
            
            print(f" {Color.MAGENTA}[Peramban-{thread_id:02d}]{Color.END} Akses media operasi {operation+1}...")
            driver.set_page_load_timeout(30)
            driver.get(target)
            
            try:
                driver.execute_script("let vids = document.getElementsByTagName('video'); if(vids.length > 0) vids[0].play();")
            except:
                pass

            print(f" {Color.GREEN}[Peramban-{thread_id:02d}]{Color.END} {TEXT[lang]['watching']} ({duration} detik)...")
            time.sleep(duration)
            
            success += 1
            print(f" {Color.CYAN}[Peramban-{thread_id:02d}]{Color.END} Operasi {operation+1} {Color.GREEN}{TEXT[lang]['success']}{Color.END}")
            
        except Exception as e:
            failed += 1
            print(f" {Color.RED}[Peramban-{thread_id:02d}] {TEXT[lang]['fail']}{Color.END}")
        finally:
            if driver:
                driver.quit()

    print(f"\n{Color.BOLD}>> Mesin Peramban-{thread_id:02d} {TEXT[lang]['completed']}. (Berhasil: {success}, Gagal: {failed}){Color.END}")

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
    {Color.END}{Color.BOLD}{Color.BG_MAGENTA} {TEXT[lang]['subtitle'].center(68)} {Color.END}
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
        total_hits = int(input(f"\n{Color.BOLD}{TEXT[lang]['ask_hits']}{Color.END}"))
        thread_count = int(input(f"{Color.BOLD}{TEXT[lang]['ask_threads']}{Color.END}"))
    except ValueError:
        print(f"{Color.RED}{TEXT[lang]['err_val']}{Color.END}")
        return

    hits_per_thread = total_hits // thread_count
    remaining = total_hits % thread_count

    print(f"\n{Color.GREEN}{TEXT[lang]['init']}{Color.END}\n")
    
    threads = []
    for i in range(thread_count):
        count = hits_per_thread + (remaining if i == 0 else 0)
        if count > 0:
            if mode_type == '1':
                t = threading.Thread(target=run_http_worker, args=(target_url, ref_choice, count, i+1, lang))
            else:
                t = threading.Thread(target=run_browser_worker, args=(target_url, count, i+1, lang, watch_duration))
            
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

    print(f"\n{Color.BOLD}{Color.BG_MAGENTA}  {TEXT[lang]['all_done']}  {Color.END}")
    input(f"\n{TEXT[lang]['press_exit']}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Color.RED} \n[!] {TEXT.get('EN', {}).get('interrupted', 'Operation Interrupted')} / {TEXT.get('ID', {}).get('interrupted', 'Operasi Dihentikan')}.{Color.END}")
        sys.exit()