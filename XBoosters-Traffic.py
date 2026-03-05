import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3
import threading
import random
import time
import sys
import os

# Menonaktifkan peringatan SSL untuk efisiensi eksekusi
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Pengaturan Warna Terminal untuk Antarmuka
class Color:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Daftar User-Agent Mutakhir (Standar 2024-2025)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
]

# Database Rujukan (Referrer) Terdistribusi
REFERRERS = {
    "1": ["https://www.facebook.com/", "https://m.facebook.com/", "https://l.facebook.com/l.php"],
    "2": ["https://x.com/", "https://t.co/", "https://mobile.x.com/"],
    "3": ["https://www.instagram.com/", "https://l.instagram.com/"],
    "4": ["https://www.google.com/", "https://www.bing.com/", "https://duckduckgo.com/"]
}

# Kamus Bahasa (Fasih dan Profesional)
TEXT = {
    "EN": {
        "title": "HIGH PERFORMANCE WEB TRAFFIC UTILITY",
        "select_lang": "Select Language / Pilih Bahasa:",
        "ask_url": "Enter Target URL (http:// or https://): ",
        "err_url": "Error: Invalid URL format!",
        "ask_ref": "Select Traffic Origin:",
        "ref_1": "1. Facebook",
        "ref_2": "2. X (Twitter)",
        "ref_3": "3. Instagram",
        "ref_4": "4. Search Engines",
        "ref_5": "5. Mix All Sources (Highly Recommended)",
        "ask_choice": "Selection (1-5): ",
        "ask_hits": "Total Visits to Deliver: ",
        "ask_threads": "Worker Threads (Min 1-2): ",
        "err_val": "Error: Please enter a valid number!",
        "init": "[!] Initializing high-speed traffic delivery...",
        "success": "SUCCESS",
        "fail": "FAILED",
        "host": "Origin",
        "conn_err": "CONNECTION DROPPED",
        "completed": "Completed",
        "all_done": "✔ ALL TRAFFIC OPERATIONS COMPLETED SUCCESSFULLY.",
        "press_exit": "Press Enter to exit...",
        "interrupted": "Operation terminated by user."
    },
    "ID": {
        "title": "UTILITAS TRAFIK WEB PERFORMA TINGGI",
        "select_lang": "Pilih Bahasa / Select Language:",
        "ask_url": "Masukkan Alamat URL Target (http:// atau https://): ",
        "err_url": "Kesalahan: Format URL tidak valid!",
        "ask_ref": "Pilih Sumber Rujukan Trafik:",
        "ref_1": "1. Facebook",
        "ref_2": "2. X (Dahulu Twitter)",
        "ref_3": "3. Instagram",
        "ref_4": "4. Mesin Pencari",
        "ref_5": "5. Campuran Semua Sumber (Sangat Disarankan)",
        "ask_choice": "Pilihan (1-5): ",
        "ask_hits": "Total Kunjungan yang Didistribusikan: ",
        "ask_threads": "Jumlah Jalur Pekerja (Min 1-2): ",
        "err_val": "Kesalahan: Harap masukkan angka yang valid!",
        "init": "[!] Memulai pengiriman trafik berkecepatan tinggi...",
        "success": "BERHASIL",
        "fail": "GAGAL",
        "host": "Asal",
        "conn_err": "KONEKSI TERPUTUS",
        "completed": "Selesai",
        "all_done": "✔ SELURUH OPERASI TRAFIK TELAH DISELESAIKAN DENGAN SUKSES.",
        "press_exit": "Tekan Enter untuk keluar...",
        "interrupted": "Operasi dihentikan oleh pengguna."
    }
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_optimized_session():
    """
    Menghasilkan sesi HTTP yang dioptimalkan dengan fitur Retry otomatis.
    Mencegah trafik lolos atau gagal akibat putusnya koneksi sesaat.
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=3,  # Mengulang maksimal 3 kali jika gagal
        backoff_factor=0.3, # Jeda dinamis antar pengulangan
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    # Meningkatkan ukuran pool koneksi untuk mendukung multi-threading intensif
    adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def generate_headers(referrer_url):
    """Menyusun struktur header yang identik dengan perilaku peramban aktual."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": referrer_url,
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Upgrade-Insecure-Requests": "1"
    }

def worker(target, ref_choice, hits, thread_id, lang):
    """Jalur pekerja (worker thread) untuk eksekusi pengiriman trafik."""
    session = get_optimized_session()
    success = 0
    failed = 0
    
    for _ in range(hits):
        if ref_choice == "5":
            category = random.choice(list(REFERRERS.values()))
            ref = random.choice(category)
        else:
            ref = random.choice(REFERRERS.get(ref_choice, REFERRERS["4"]))

        try:
            response = session.get(target, headers=generate_headers(ref), timeout=10, verify=False)
            
            if response.status_code < 400:
                success += 1
                status_text = f"{Color.GREEN}{TEXT[lang]['success']}{Color.END}"
            else:
                failed += 1
                status_text = f"{Color.RED}{TEXT[lang]['fail']} {response.status_code}{Color.END}"
                
            print(f" {Color.CYAN}[Thread-{thread_id:02d}]{Color.END} {status_text} | {TEXT[lang]['host']}: {ref.split('/')[2]}")
            
        except Exception:
            failed += 1
            print(f" {Color.RED}[Thread-{thread_id:02d}] {TEXT[lang]['conn_err']}{Color.END}")

        # Menggunakan jeda mikro untuk kecepatan maksimal namun tetap stabil
        time.sleep(random.uniform(0.05, 0.5))

    print(f"\n{Color.YELLOW}>> Thread-{thread_id:02d} {TEXT[lang]['completed']}. (S: {success}, F: {failed}){Color.END}")

def main():
    clear_screen()
    print(f"{Color.BOLD}{Color.CYAN}")
    print("    1. English")
    print("    2. Bahasa Indonesia")
    print(f"{Color.END}")
    
    lang_choice = input(f"{Color.BOLD}Select Language / Pilih Bahasa (1/2): {Color.END}").strip()
    lang = "EN" if lang_choice == "1" else "ID"

    clear_screen()
    print(f"""{Color.BOLD}{Color.BLUE}
    ╔═════════════════════════════════════════════════════════════╗
    ║                 XBOOSTERS TRAFFIC v2.5                      ║
    ║         {TEXT[lang]['title'].center(43)}         ║
    ╚═════════════════════════════════════════════════════════════╝{Color.END}
    """)

    target_url = input(f"{Color.CYAN}{TEXT[lang]['ask_url']}{Color.END}").strip()
    if not target_url.startswith("http"):
        print(f"{Color.RED}{TEXT[lang]['err_url']}{Color.END}")
        return

    print(f"\n{Color.BOLD}{TEXT[lang]['ask_ref']}{Color.END}")
    print(f" {TEXT[lang]['ref_1']}")
    print(f" {TEXT[lang]['ref_2']}")
    print(f" {TEXT[lang]['ref_3']}")
    print(f" {TEXT[lang]['ref_4']}")
    print(f" {TEXT[lang]['ref_5']}")
    ref_choice = input(f"{Color.CYAN}{TEXT[lang]['ask_choice']}{Color.END}").strip()

    try:
        total_hits = int(input(f"\n{Color.CYAN}{TEXT[lang]['ask_hits']}{Color.END}"))
        thread_count = int(input(f"{Color.CYAN}{TEXT[lang]['ask_threads']}{Color.END}"))
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
            t = threading.Thread(target=worker, args=(target_url, ref_choice, count, i+1, lang))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

    print(f"\n{Color.BOLD}{Color.GREEN}{TEXT[lang]['all_done']}{Color.END}")
    input(f"\n{TEXT[lang]['press_exit']}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Menghapus log error panjang saat user menekan Ctrl+C
        print(f"\n{Color.RED} \n[!] Operation Interrupted / Operasi Dihentikan.{Color.END}")
        sys.exit()