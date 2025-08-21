import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import threading

def is_valid_url(url):
    try:
        result = urlparse(url)
        return result.scheme in ("http", "https")
    except:
        return False

def check_link(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code >= 400
    except:
        return True

def crawl(url, depth, visited, broken_links, base_domain):
    if depth < 0 or url in visited:
        return
    visited.add(url)
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link_tag in soup.find_all('a', href=True):
            link = urljoin(url, link_tag['href'])
            parsed_link = urlparse(link)
            if parsed_link.netloc and base_domain in parsed_link.netloc:
                if link not in visited:
                    if check_link(link):
                        broken_links.append(link)
                    crawl(link, depth - 1, visited, broken_links, base_domain)
    except:
        broken_links.append(url)

def start_crawl():
    url = url_entry.get()
    try:
        depth = int(depth_entry.get())
    except ValueError:
        result_box.insert(tk.END, "Depth must be an integer.\n")
        return

    if not is_valid_url(url):
        result_box.insert(tk.END, "Invalid URL.\n")
        return

    result_box.delete(1.0, tk.END)
    result_box.insert(tk.END, f"Scanning {url} up to depth {depth}...\n")

    def run():
        visited = set()
        broken_links = []
        base_domain = urlparse(url).netloc
        crawl(url, depth, visited, broken_links, base_domain)
        result_box.insert(tk.END, f"\nBroken links found:\n")
        for link in broken_links:
            result_box.insert(tk.END, f"{link}\n")

    threading.Thread(target=run).start()

# GUI Setup
root = tk.Tk()
root.title("Broken Link Finder - Corporate Secretary, DND")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky="nsew")

ttk.Label(frame, text="Enter URL:").grid(row=0, column=0, sticky="w")
url_entry = ttk.Entry(frame, width=60)
url_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text="Depth Level:").grid(row=1, column=0, sticky="w")
depth_entry = ttk.Entry(frame, width=10)
depth_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

ttk.Button(frame, text="Start Scan", command=start_crawl).grid(row=2, column=0, columnspan=2, pady=10)

result_box = scrolledtext.ScrolledText(root, width=80, height=25)
result_box.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()
# Broken Link Finder GUI Application
# This application allows users to input a URL and a depth level to scan for broken links.
# It uses threading to perform the scan without freezing the GUI.