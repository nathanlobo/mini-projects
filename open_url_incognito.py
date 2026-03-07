import subprocess
import platform
import os
import random
import time
import psutil

# Optional dependency: requests (used for proxy validation). If not installed, validation will be skipped.
try:
    import requests
except ImportError:  # Keep lightweight if requests missing
    requests = None

USER_AGENTS = [
    # Common desktop user agents (can expand as needed)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/118.0.2088.76",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
]

# Local proxy file (one proxy per line) and optional remote proxy list sources.
# You can add or remove sources below; each URL should return plain text with one proxy per line.
PROXY_FILE = 'proxies.txt'
REMOTE_PROXY_SOURCES = [
    # Public raw lists (availability/quality varies; rotate or curate as needed)
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt',
    'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
    # Add more sources here:
    # 'https://example.com/my-proxy-list.txt',
]

def _read_proxies_from_file(path: str):
    if not os.path.exists(path):
        return []
    proxies = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            proxies.append(line)
    return proxies

def _fetch_proxies_from_urls(urls):
    if not requests:
        return []
    fetched = []
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    for u in urls:
        try:
            resp = requests.get(u, headers=headers, timeout=8)
            if resp.ok:
                for line in resp.text.splitlines():
                    line = line.strip()
                    if line and ':' in line:
                        if not line.startswith('http'):
                            line = 'http://' + line  # assume http if scheme missing
                        fetched.append(line)
        except Exception:
            pass
    return fetched

def _validate_proxy(proxy: str, test_url: str = "http://httpbin.org/ip", timeout: float = 5.0):
    if not requests:
        return True  # Skip validation if requests missing
    try:
        scheme_split = proxy.split('://', 1)
        if len(scheme_split) == 2:
            scheme = scheme_split[0]
        else:
            scheme = 'http'
        proxies = {"http": proxy, "https": proxy}
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        r = requests.get(test_url, proxies=proxies, headers=headers, timeout=timeout)
        return r.ok
    except Exception:
        return False

def get_proxy_list(
    local_file: str = "proxies.txt",
    remote_sources = None,
    max_validate: int = 30,
    require_validation: bool = True
):
    """Aggregate and optionally validate proxies.

    Args:
        local_file: Path to a local file with one proxy per line (ip:port or scheme://ip:port).
        remote_sources: Iterable of URLs returning plain text proxy lists.
        max_validate: Cap number of proxies to validate for speed.
        require_validation: If True, only return proxies that pass validation.

    Returns:
        List of proxy strings.
    """
    if remote_sources is None:
        remote_sources = []  # Supply list of proxy provider URLs if desired.

    proxies = []
    proxies.extend(_read_proxies_from_file(local_file))
    proxies.extend(_fetch_proxies_from_urls(remote_sources))

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for p in proxies:
        if p not in seen:
            seen.add(p)
            unique.append(p)

    if not require_validation:
        return unique

    validated = []
    to_check = unique[:max_validate]
    print(f"Validating up to {len(to_check)} proxies...")
    for proxy in to_check:
        if _validate_proxy(proxy):
            validated.append(proxy)
    if not validated:
        print("No valid proxies found (or validation skipped). Returning unvalidated list.")
        return unique if not require_validation else []
    print(f"Validated proxies: {len(validated)}")
    return validated

def open_chrome_incognito(url, proxy=None):
    """Open URL in Chrome incognito mode with optional proxy"""
    system = platform.system()
    
    chrome_paths = {
        'Windows': [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            os.path.expanduser(r'~\AppData\Local\Google\Chrome\Application\chrome.exe')
        ],
        'Darwin': ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'],
        'Linux': ['google-chrome', 'chrome', 'chromium-browser']
    }
    
    chrome_path = None
    for path in chrome_paths.get(system, []):
        if os.path.exists(path):
            chrome_path = path
            break
    
    if not chrome_path:
        chrome_path = 'chrome'  # Try system PATH
    
    # Force new window instance with unique user data directory
    user_data_dir = os.path.join(os.path.expanduser('~'), '.chrome_temp_profiles', f'profile_{random.randint(100000, 999999)}')
    os.makedirs(user_data_dir, exist_ok=True)
    
    cmd = [chrome_path, '--incognito', f'--user-data-dir={user_data_dir}', '--no-first-run', '--no-default-browser-check']
    
    if proxy:
        cmd.append(f'--proxy-server={proxy}')
    
    cmd.append(url)
    
    try:
        process = subprocess.Popen(cmd)
        return process
    except Exception as e:
        print(f"Error opening Chrome: {e}")
        return None

def open_firefox_private(url, proxy=None):
    """Open URL in Firefox private mode with optional proxy"""
    system = platform.system()
    
    firefox_paths = {
        'Windows': [
            r'C:\Program Files\Mozilla Firefox\firefox.exe',
            r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe',
        ],
        'Darwin': ['/Applications/Firefox.app/Contents/MacOS/firefox'],
        'Linux': ['firefox']
    }
    
    firefox_path = None
    for path in firefox_paths.get(system, []):
        if os.path.exists(path):
            firefox_path = path
            break
    
    if not firefox_path:
        firefox_path = 'firefox'
    
    # Force new window instance
    cmd = [firefox_path, '--private-window', '--new-instance']
    
    if proxy:
        # Firefox proxy requires profile configuration
        # This is a simplified approach
        print("Note: Firefox proxy configuration requires additional setup")
    
    cmd.append(url)
    
    try:
        process = subprocess.Popen(cmd)
        return process
    except Exception as e:
        print(f"Error opening Firefox: {e}")
        return None

def open_edge_inprivate(url, proxy=None):
    """Open URL in Edge InPrivate mode with optional proxy"""
    system = platform.system()
    
    if system == 'Windows':
        edge_paths = [
            r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
        ]
        
        edge_path = None
        for path in edge_paths:
            if os.path.exists(path):
                edge_path = path
                break
        
        if not edge_path:
            edge_path = 'msedge'
        
        # Force new window instance with unique user data directory
        user_data_dir = os.path.join(os.path.expanduser('~'), '.edge_temp_profiles', f'profile_{random.randint(100000, 999999)}')
        os.makedirs(user_data_dir, exist_ok=True)
        
        cmd = [edge_path, '--inprivate', f'--user-data-dir={user_data_dir}', '--no-first-run', '--no-default-browser-check']
        
        if proxy:
            cmd.append(f'--proxy-server={proxy}')
        
        cmd.append(url)
        
        try:
            process = subprocess.Popen(cmd)
            return process
        except Exception as e:
            print(f"Error opening Edge: {e}")
            return None
    else:
        print("Edge is primarily available on Windows")
        return None

def close_browser_process(process):
    """Close browser process and all its child processes"""
    if process is None:
        return
    
    try:
        # Get the parent process
        parent = psutil.Process(process.pid)
        
        # Get all child processes
        children = parent.children(recursive=True)
        
        # Terminate all child processes
        for child in children:
            try:
                child.terminate()
            except psutil.NoSuchProcess:
                pass
        
        # Terminate parent process
        parent.terminate()
        
        # Wait for processes to terminate
        gone, alive = psutil.wait_procs(children + [parent], timeout=3)
        
        # Force kill if still alive
        for p in alive:
            try:
                p.kill()
            except psutil.NoSuchProcess:
                pass
                
        print("Browser closed successfully")
    except psutil.NoSuchProcess:
        print("Browser process already closed")
    except Exception as e:
        print(f"Error closing browser: {e}")

def open_url_with_ip_rotation(url, browser='chrome', use_proxy=False):
    """
    Main function to open URL in incognito mode with optional IP rotation
    
    Args:
        url (str): URL to open
        browser (str): Browser choice - 'chrome', 'firefox', or 'edge'
        use_proxy (bool): Whether to use proxy for IP masking
    
    Returns:
        process: Browser process object or None
    """
    proxy = None
    user_agent = random.choice(USER_AGENTS)

    if use_proxy:
        proxies = get_proxy_list(
            local_file=PROXY_FILE,
            remote_sources=REMOTE_PROXY_SOURCES,
            max_validate=50,
            require_validation=True
        )
        if proxies:
            proxy = random.choice(proxies)
            print(f"Using proxy: {proxy}")
        else:
            print("Warning: No proxies available, opening without proxy")
    
    print(f"Opening URL in {browser} incognito mode...")
    print(f"Random User-Agent selected: {user_agent}")
    
    process = None
    if browser.lower() == 'chrome':
        process = open_chrome_incognito(url, proxy)
    elif browser.lower() == 'firefox':
        process = open_firefox_private(url, proxy)
    elif browser.lower() == 'edge':
        process = open_edge_inprivate(url, proxy)
    else:
        print(f"Unsupported browser: {browser}")
        print("Trying Chrome as fallback...")
        process = open_chrome_incognito(url, proxy)
    
    if process:
        print("Browser opened successfully!")
        return process
    else:
        print("Failed to open browser. Please check if the browser is installed.")
        return None

if __name__ == "__main__":
    # Target URL
    target_url = "https://jubileebread.com/sxta6axa?key=79bb96b3c4214a050f80d0f5f58a374b"
    
    # Configuration
    BROWSER = 'chrome'      # Options: 'chrome', 'firefox', 'edge'
    USE_PROXY = False       # Set to True to enable proxy (requires valid proxy list)
    MIN_WAIT_TIME = 7      # Minimum time in seconds before closing browser
    MAX_WAIT_TIME = 20      # Maximum time in seconds before closing browser
    LOOP_CONTINUOUSLY = True  # Set to False to run only once
    
    print("=" * 60)
    print("Incognito Browser Launcher with IP Rotation - LOOP MODE")
    print("=" * 60)
    print(f"Configuration:")
    print(f"  - Browser: {BROWSER}")
    print(f"  - Proxy: {'Enabled' if USE_PROXY else 'Disabled'}")
    print(f"  - Wait time: {MIN_WAIT_TIME}-{MAX_WAIT_TIME} seconds (random)")
    print(f"  - Loop mode: {'Enabled' if LOOP_CONTINUOUSLY else 'Disabled'}")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the loop at any time\n")
    
    loop_count = 0
    
    try:
        while True:
            loop_count += 1
            print(f"\n--- Loop #{loop_count} ---")
            
            # Open the URL
            browser_process = open_url_with_ip_rotation(
                target_url, 
                browser=BROWSER, 
                use_proxy=USE_PROXY
            )
            
            if browser_process:
                # Wait for random time to avoid bot detection
                wait_time = random.uniform(MIN_WAIT_TIME, MAX_WAIT_TIME)
                print(f"Waiting {wait_time:.2f} seconds before closing...")
                time.sleep(wait_time)
                
                # Close the browser
                print("Closing browser...")
                close_browser_process(browser_process)
                
                # Small delay before next iteration
                if LOOP_CONTINUOUSLY:
                    print("Starting next iteration in 2 seconds...")
                    time.sleep(2)
            else:
                print("Failed to open browser. Retrying in 5 seconds...")
                time.sleep(5)
            
            # Break if not in continuous loop mode
            if not LOOP_CONTINUOUSLY:
                break
                
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("Loop stopped by user")
        print(f"Total iterations completed: {loop_count}")
        print("=" * 60)
    
    print("\nNote: For actual IP masking, you need to:")
    print("1. Update get_proxy_list() with working proxy servers")
    print("2. Or use a VPN service")
    print("3. Or use Tor Browser for anonymity")
    print("=" * 60)

