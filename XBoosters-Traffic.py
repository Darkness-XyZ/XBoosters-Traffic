import requests
import threading
import random
import time
import sys
import os

# Warna Terminal untuk UI yang lebih segar
class Color:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Database User-Agent yang diperbarui (2024-2025 Standard)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
]

# Sumber Referrer (Diperbarui ke X.com)
REFERRERS = {
    "1": ["https://www.facebook.com/", "https://m.facebook.com/", "https://l.facebook.com/l.php"],
    "2": ["https://x.com/", "https://t.co/", "https://mobile.x.com/"],
    "3": ["https://www.instagram.com/", "https://l.instagram.com/"],
    "4": ["https://www.google.com/", "https://www.bing.com/", "https://duckduckgo.com/"]
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_header(referrer_url):
    """Menghasilkan header yang sangat mirip dengan perilaku browser asli."""
    ua = random.choice(USER_AGENTS)
    return {
        "User-Agent": ua,
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

def worker(target, ref_choice, hits, thread_id):
    """Fungsi eksekusi traffic menggunakan Session untuk kecepatan optimal."""
    session = requests.Session()
    success = 0
    failed = 0
    
    for _ in range(hits):
        # Pilih sumber referrer berdasarkan input
        if ref_choice == "5": # Mix All
            category = random.choice(list(REFERRERS.values()))
            ref = random.choice(category)
        else:
            ref = random.choice(REFERRERS.get(ref_choice, REFERRERS["4"]))

        try:
            # Pengiriman request dengan session lebih cepat daripada requests.get biasa
            response = session.get(target, headers=get_header(ref), timeout=15)
            
            if response.status_code < 400:
                success += 1
                status_text = f"{Color.GREEN}SUCCESS{Color.END}"
            else:
                failed += 1
                status_text = f"{Color.RED}STATUS {response.status_code}{Color.END}"
                
            print(f" {Color.CYAN}[Thread-{thread_id}]{Color.END} {status_text} | Target: {target[:30]}... | Ref: {ref.split('/')[2]}")
            
        except Exception as e:
            failed += 1
            print(f" {Color.RED}[Thread-{thread_id}] ERROR: {str(e)[:50]}{Color.END}")

        # Jeda minimal agar tidak membebani CPU secara berlebihan
        time.sleep(random.uniform(0.1, 1.0))

    print(f"\n{Color.YELLOW}>> Thread-{thread_id} Selesai. (S: {success}, G: {failed}){Color.END}")

def main():
    clear_screen()
    print(f"""{Color.BOLD}{Color.BLUE}
    ╔══════════════════════════════════════════════════════╗
    ║           MODERN TRAFFIC GENERATOR v2.0              ║
    ║        Optimized for Performance & Stealth           ║
    ╚══════════════════════════════════════════════════════╝{Color.END}
    """)

    # Input Konfigurasi
    target_url = input(f"{Color.CYAN}Target URL (https://...): {Color.END}").strip()
    if not target_url.startswith("http"):
        print(f"{Color.RED}Error: URL tidak valid!{Color.END}")
        return

    print(f"\n{Color.BOLD}Pilih Sumber Referrer:{Color.END}")
    print(" 1. Facebook")
    print(" 2. X (Twitter)")
    print(" 3. Instagram")
    print(" 4. Search Engine (Google/Bing)")
    print(" 5. Mix All (Sangat Disarankan)")
    ref_choice = input(f"{Color.CYAN}Pilihan (1-5): {Color.END}").strip()

    try:
        total_hits = int(input(f"{Color.CYAN}Total Hit yang diinginkan: {Color.END}"))
        thread_count = int(input(f"{Color.CYAN}Jumlah Thread (Min 1-2): {Color.END}"))
    except ValueError:
        print(f"{Color.RED}Harap masukkan angka yang valid!{Color.END}")
        return

    # Hitung distribusi hit per thread
    hits_per_thread = total_hits // thread_count
    remaining = total_hits % thread_count

    print(f"\n{Color.GREEN}[!] Inisialisasi pengiriman traffic...{Color.END}\n")
    
    threads = []
    for i in range(thread_count):
        count = hits_per_thread + (remaining if i == 0 else 0)
        t = threading.Thread(target=worker, args=(target_url, ref_choice, count, i+1))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\n{Color.BOLD}{Color.GREEN}✔ SEMUA PROSES TELAH DISELESAIKAN.{Color.END}")
    input("\nTekan Enter untuk keluar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Color.RED} Prosedur dihentikan oleh pengguna.{Color.END}")
        sys.exit()