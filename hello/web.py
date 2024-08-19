import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import validators


class WebCrawlerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sahan Web Crawler")
        self.root.configure(bg='#FFC0CB')

        # URL input
        self.url_label = ttk.Label(root, text="Enter URL:", background='#FFC0CB')
        self.url_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)

        # Crawl depth input
        self.depth_label = ttk.Label(root, text="Crawl Depth:", background='#FFC0CB')
        self.depth_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.depth_entry = ttk.Entry(root, width=5)
        self.depth_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.depth_entry.insert(0, "1")

        # Search entry
        self.search_entry = ttk.Entry(root, width=30)
        self.search_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Search button
        self.search_button = ttk.Button(root, text="Search", command=self.search)
        self.search_button.grid(row=2, column=2, padx=10, pady=10)

        # Crawl button
        self.crawl_button = ttk.Button(root, text="Crawl", command=self.crawl)
        self.crawl_button.grid(row=0, column=2, padx=10, pady=10)

        # Save button
        self.save_button = ttk.Button(root, text="Save Results", command=self.save_results)
        self.save_button.grid(row=1, column=2, padx=10, pady=10)

        # Result display
        self.result_text = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD, bg='#FFF0F5')
        self.result_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def crawl(self):
        url = self.url_entry.get()
        depth = self.depth_entry.get()
        self.result_text.delete(1.0, tk.END)

        # Validate URL
        if not validators.url(url):
            messagebox.showerror("Invalid URL", "Please enter a valid URL.")
            return

        # Validate depth
        try:
            depth = int(depth)
            if depth < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Depth", "Please enter a valid depth (positive integer).")
            return

        # Start crawling
        self.result_text.insert(tk.END, "Crawling started...\n\n")
        self.crawl_url(url, depth)
        self.result_text.insert(tk.END, "\nCrawling finished.")

    def crawl_url(self, url, depth):
        if depth == 0:
            return

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')

            self.result_text.insert(tk.END, f"Found {len(links)} links at depth {depth}:\n\n")
            for link in links:
                href = link.get('href')
                if href:
                    self.result_text.insert(tk.END, href + "\n")
                    # Recursively crawl the links (simple approach, may need to handle relative URLs)
                    if href.startswith("http://") or href.startswith("https://"):
                        self.crawl_url(href, depth - 1)
        except requests.exceptions.RequestException as e:
            self.result_text.insert(tk.END, f"Error: {e}\n")

    def save_results(self):
        result = self.result_text.get(1.0, tk.END)
        if not result.strip():
            messagebox.showerror("No Results", "There are no results to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"),
                                                            ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(result)
            messagebox.showinfo("Success", "Results saved successfully.")

    def search(self):
        search_text = self.search_entry.get()
        if not search_text:
            messagebox.showwarning("Search Text Required", "Please enter text to search.")
            return

        content = self.result_text.get(1.0, tk.END)
        self.result_text.tag_remove("highlight", 1.0, tk.END)
        start_index = 1.0

        while True:
            start_index = self.result_text.search(search_text, start_index, nocase=True, stopindex=tk.END)
            if not start_index:
                break
            end_index = f"{start_index}+{len(search_text)}c"
            self.result_text.tag_add("highlight", start_index, end_index)
            start_index = end_index

        self.result_text.tag_config("highlight", background="yellow", foreground="black")

        if not self.result_text.tag_ranges("highlight"):
            messagebox.showinfo("Not Found", f"'{search_text}' not found in results.")


def main():
    root = tk.Tk()
    app = WebCrawlerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
