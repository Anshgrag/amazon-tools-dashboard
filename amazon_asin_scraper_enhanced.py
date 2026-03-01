import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import requests
from bs4 import BeautifulSoup
import threading
import zipfile
import os
from urllib.parse import urljoin
import time
import random
from datetime import datetime


class AmazonASINScraper:
    def __init__(self, root):
        self.root = root
        self.root.title("Amazon ASIN Scraper Pro")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e2e')

        # Style configuration
        self.setup_styles()

        # Variables
        self.asins = []
        self.scraped_data = []
        self.scraping_active = False
        self.country_domains = {
            'United States': 'amazon.com',
            'United Kingdom': 'amazon.co.uk',
            'Germany': 'amazon.de',
            'France': 'amazon.fr',
            'Italy': 'amazon.it',
            'Spain': 'amazon.es',
            'Canada': 'amazon.ca',
            'Japan': 'amazon.co.jp',
            'India': 'amazon.in',
            'Australia': 'amazon.com.au'
        }

        # Data field selection variables
        self.scrape_title_var = tk.BooleanVar(value=True)
        self.scrape_brand_var = tk.BooleanVar(value=True)
        self.scrape_price_var = tk.BooleanVar(value=True)
        self.scrape_rating_var = tk.BooleanVar(value=True)
        self.scrape_images_var = tk.BooleanVar(value=True)

        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Configure modern dark theme
        style.configure('TNotebook', background='#1e1e2e', borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background='#313244', 
                       foreground='#cdd6f4',
                       padding=[20, 10],
                       focuscolor='none')
        style.map('TNotebook.Tab',
                 background=[('selected', '#89b4fa'), ('active', '#45475a')],
                 foreground=[('selected', '#1e1e2e'), ('active', '#cdd6f4')])

        style.configure('Modern.TFrame', background='#1e1e2e')
        style.configure('Card.TFrame', 
                       background='#313244', 
                       relief='flat', 
                       borderwidth=1)

        style.configure('Modern.TLabel', 
                       background='#1e1e2e', 
                       foreground='#cdd6f4',
                       font=('Inter', 10))

        style.configure('Card.TLabel', 
                       background='#313244', 
                       foreground='#cdd6f4',
                       font=('Inter', 10))

        style.configure('Title.TLabel', 
                       background='#1e1e2e', 
                       foreground='#89b4fa',
                       font=('Inter', 16, 'bold'))

        style.configure('CardTitle.TLabel', 
                       background='#313244', 
                       foreground='#89b4fa',
                       font=('Inter', 14, 'bold'))

        style.configure('Modern.TButton',
                       background='#89b4fa',
                       foreground='#1e1e2e',
                       font=('Inter', 10, 'bold'),
                       focuscolor='none',
                       borderwidth=0,
                       relief='flat')
        style.map('Modern.TButton',
                 background=[('active', '#74c0fc')])

        style.configure('Success.TButton',
                       background='#a6e3a1',
                       foreground='#1e1e2e')
        style.map('Success.TButton',
                 background=[('active', '#94d3a2')])

        style.configure('Danger.TButton',
                       background='#f38ba8',
                       foreground='#1e1e2e')
        style.map('Danger.TButton',
                 background=[('active', '#f2a2ba')])

        style.configure('Small.TButton',
                       background='#45475a',
                       foreground='#cdd6f4',
                       font=('Inter', 9),
                       padding=[5, 2])
        style.map('Small.TButton',
                 background=[('active', '#585b70')])

        # Checkbutton style for card background
        style.configure('Card.TCheckbutton',
                       background='#313244',
                       foreground='#cdd6f4',
                       font=('Inter', 10))
        style.map('Card.TCheckbutton',
                 background=[('active', '#313244')])

    def create_widgets(self):
        # Main container
        main_container = ttk.Frame(self.root, style='Modern.TFrame')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Header
        header_frame = ttk.Frame(main_container, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))

        title_label = ttk.Label(header_frame, 
                               text="Amazon ASIN Scraper Pro", 
                               style='Title.TLabel')
        title_label.pack()

        subtitle_label = ttk.Label(header_frame, 
                                  text="Extract product data, images, and pricing from multiple Amazon regions",
                                  style='Modern.TLabel')
        subtitle_label.pack(pady=(5, 0))

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        self.create_input_tab()
        self.create_scraping_tab()
        self.create_results_tab()
        self.create_settings_tab()

    def create_input_tab(self):
        # Input Tab
        input_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(input_frame, text='📁 Input')

        # Input methods card
        input_card = ttk.Frame(input_frame, style='Card.TFrame')
        input_card.pack(fill='x', padx=20, pady=20)

        ttk.Label(input_card, 
                 text="Input Methods", 
                 style='Title.TLabel').pack(anchor='w', padx=20, pady=(20, 10))

        # File input section
        file_frame = ttk.Frame(input_card, style='Card.TFrame')
        file_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(file_frame, 
                 text="Upload Excel/TXT file with ASINs:",
                 style='Card.TLabel').pack(anchor='w', pady=(0, 5))

        file_btn_frame = ttk.Frame(file_frame, style='Card.TFrame')
        file_btn_frame.pack(fill='x', pady=5)

        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_btn_frame, textvariable=self.file_path_var, width=50)
        file_entry.pack(side='left', padx=(0, 10))

        ttk.Button(file_btn_frame, 
                  text="Browse", 
                  style='Modern.TButton',
                  command=self.browse_file).pack(side='left')

        ttk.Button(file_btn_frame, 
                  text="Load ASINs", 
                  style='Success.TButton',
                  command=self.load_asins).pack(side='left', padx=(10, 0))

        # Manual input section
        manual_frame = ttk.Frame(input_card, style='Card.TFrame')
        manual_frame.pack(fill='both', expand=True, padx=20, pady=(20, 20))

        ttk.Label(manual_frame, 
                 text="Or enter ASINs manually (one per line):",
                 style='Card.TLabel').pack(anchor='w', pady=(0, 5))

        self.manual_text = tk.Text(manual_frame, 
                                  height=10, 
                                  bg='#45475a', 
                                  fg='#cdd6f4',
                                  insertbackground='#cdd6f4',
                                  selectbackground='#89b4fa',
                                  font=('Inter', 10),
                                  relief='flat',
                                  borderwidth=5)
        self.manual_text.pack(fill='both', expand=True, pady=5)

        ttk.Button(manual_frame, 
                  text="Add Manual ASINs", 
                  style='Success.TButton',
                  command=self.add_manual_asins).pack(pady=10)

        # ASIN display
        display_frame = ttk.Frame(input_frame, style='Card.TFrame')
        display_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        ttk.Label(display_frame, 
                 text="Loaded ASINs", 
                 style='Title.TLabel').pack(anchor='w', padx=20, pady=(20, 10))

        # Treeview for ASINs
        columns = ('Index', 'ASIN')
        self.asin_tree = ttk.Treeview(display_frame, columns=columns, show='headings', height=8)

        for col in columns:
            self.asin_tree.heading(col, text=col)
            self.asin_tree.column(col, width=100)

        scrollbar_asins = ttk.Scrollbar(display_frame, orient='vertical', command=self.asin_tree.yview)
        self.asin_tree.configure(yscrollcommand=scrollbar_asins.set)

        tree_frame = ttk.Frame(display_frame, style='Card.TFrame')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        self.asin_tree.pack(side='left', fill='both', expand=True)
        scrollbar_asins.pack(side='right', fill='y')

    def create_scraping_tab(self):
        # Scraping Tab
        scraping_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(scraping_frame, text='🔄 Scraping')

        # Create a canvas with scrollbar for the scraping tab
        canvas = tk.Canvas(scraping_frame, bg='#1e1e2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(scraping_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Modern.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ============ DATA FIELDS SELECTION CARD ============
        fields_card = ttk.Frame(scrollable_frame, style='Card.TFrame')
        fields_card.pack(fill='x', padx=20, pady=20)

        ttk.Label(fields_card, 
                 text="📋 Select Data Fields to Scrape", 
                 style='CardTitle.TLabel').pack(anchor='w', padx=20, pady=(20, 10))

        ttk.Label(fields_card, 
                 text="Choose which product information you want to extract:",
                 style='Card.TLabel').pack(anchor='w', padx=20, pady=(0, 10))

        # Checkboxes frame
        checkbox_frame = ttk.Frame(fields_card, style='Card.TFrame')
        checkbox_frame.pack(fill='x', padx=20, pady=10)

        # Row 1 of checkboxes
        row1_frame = ttk.Frame(checkbox_frame, style='Card.TFrame')
        row1_frame.pack(fill='x', pady=5)

        ttk.Checkbutton(row1_frame, 
                       text="📝 Title",
                       variable=self.scrape_title_var,
                       style='Card.TCheckbutton').pack(side='left', padx=(0, 30))

        ttk.Checkbutton(row1_frame, 
                       text="🏷️ Brand",
                       variable=self.scrape_brand_var,
                       style='Card.TCheckbutton').pack(side='left', padx=(0, 30))

        ttk.Checkbutton(row1_frame, 
                       text="💰 Price",
                       variable=self.scrape_price_var,
                       style='Card.TCheckbutton').pack(side='left', padx=(0, 30))

        # Row 2 of checkboxes
        row2_frame = ttk.Frame(checkbox_frame, style='Card.TFrame')
        row2_frame.pack(fill='x', pady=5)

        ttk.Checkbutton(row2_frame, 
                       text="⭐ Rating",
                       variable=self.scrape_rating_var,
                       style='Card.TCheckbutton').pack(side='left', padx=(0, 30))

        ttk.Checkbutton(row2_frame, 
                       text="🖼️ Images",
                       variable=self.scrape_images_var,
                       style='Card.TCheckbutton').pack(side='left', padx=(0, 30))

        # Quick selection buttons
        quick_btn_frame = ttk.Frame(fields_card, style='Card.TFrame')
        quick_btn_frame.pack(fill='x', padx=20, pady=(10, 20))

        ttk.Label(quick_btn_frame, 
                 text="Quick Select:",
                 style='Card.TLabel').pack(side='left', padx=(0, 10))

        ttk.Button(quick_btn_frame, 
                  text="Select All", 
                  style='Small.TButton',
                  command=self.select_all_fields).pack(side='left', padx=(0, 5))

        ttk.Button(quick_btn_frame, 
                  text="Deselect All", 
                  style='Small.TButton',
                  command=self.deselect_all_fields).pack(side='left', padx=(0, 5))

        ttk.Button(quick_btn_frame, 
                  text="Only Images", 
                  style='Small.TButton',
                  command=self.select_only_images).pack(side='left', padx=(0, 5))

        ttk.Button(quick_btn_frame, 
                  text="Only Prices", 
                  style='Small.TButton',
                  command=self.select_only_prices).pack(side='left', padx=(0, 5))

        ttk.Button(quick_btn_frame, 
                  text="Only Brands", 
                  style='Small.TButton',
                  command=self.select_only_brands).pack(side='left', padx=(0, 5))

        ttk.Button(quick_btn_frame, 
                  text="Brand + Price", 
                  style='Small.TButton',
                  command=self.select_brand_price).pack(side='left', padx=(0, 5))

        ttk.Button(quick_btn_frame, 
                  text="Price + Images", 
                  style='Small.TButton',
                  command=self.select_price_images).pack(side='left', padx=(0, 5))

        # ============ SCRAPING CONFIGURATION CARD ============
        settings_card = ttk.Frame(scrollable_frame, style='Card.TFrame')
        settings_card.pack(fill='x', padx=20, pady=(0, 20))

        ttk.Label(settings_card, 
                 text="⚙️ Scraping Configuration", 
                 style='CardTitle.TLabel').pack(anchor='w', padx=20, pady=(20, 10))

        config_frame = ttk.Frame(settings_card, style='Card.TFrame')
        config_frame.pack(fill='x', padx=20, pady=10)

        # Country selection
        ttk.Label(config_frame, 
                 text="Select Amazon Region:",
                 style='Card.TLabel').grid(row=0, column=0, sticky='w', pady=5)

        self.country_var = tk.StringVar(value='United States')
        country_combo = ttk.Combobox(config_frame, 
                                    textvariable=self.country_var,
                                    values=list(self.country_domains.keys()),
                                    state='readonly',
                                    width=20)
        country_combo.grid(row=0, column=1, padx=(10, 0), pady=5)

        # Threading options
        ttk.Label(config_frame, 
                 text="Number of Threads:",
                 style='Card.TLabel').grid(row=1, column=0, sticky='w', pady=5)

        self.threads_var = tk.StringVar(value='5')
        threads_spin = ttk.Spinbox(config_frame, 
                                  from_=1, to=10, 
                                  textvariable=self.threads_var,
                                  width=10)
        threads_spin.grid(row=1, column=1, padx=(10, 0), pady=5)

        # Delay settings
        ttk.Label(config_frame, 
                 text="Delay between requests (seconds):",
                 style='Card.TLabel').grid(row=2, column=0, sticky='w', pady=5)

        self.delay_var = tk.StringVar(value='2')
        delay_spin = ttk.Spinbox(config_frame, 
                                from_=1, to=10, 
                                textvariable=self.delay_var,
                                width=10)
        delay_spin.grid(row=2, column=1, padx=(10, 0), pady=5)

        # Control buttons
        control_frame = ttk.Frame(settings_card, style='Card.TFrame')
        control_frame.pack(fill='x', padx=20, pady=20)

        ttk.Button(control_frame, 
                  text="🚀 Start Scraping", 
                  style='Success.TButton',
                  command=self.start_scraping).pack(side='left', padx=(0, 10))

        ttk.Button(control_frame, 
                  text="⏹️ Stop Scraping", 
                  style='Danger.TButton',
                  command=self.stop_scraping).pack(side='left')

        # ============ PROGRESS SECTION ============
        progress_card = ttk.Frame(scrollable_frame, style='Card.TFrame')
        progress_card.pack(fill='x', padx=20, pady=(0, 20))

        ttk.Label(progress_card, 
                 text="📊 Progress", 
                 style='CardTitle.TLabel').pack(anchor='w', padx=20, pady=(20, 10))

        self.progress_var = tk.StringVar(value="Ready to start scraping...")
        progress_label = ttk.Label(progress_card, 
                                  textvariable=self.progress_var,
                                  style='Card.TLabel')
        progress_label.pack(anchor='w', padx=20, pady=5)

        # Selected fields display
        self.selected_fields_var = tk.StringVar(value="Selected fields: All")
        selected_label = ttk.Label(progress_card, 
                                  textvariable=self.selected_fields_var,
                                  style='Card.TLabel')
        selected_label.pack(anchor='w', padx=20, pady=5)

        self.progress_bar = ttk.Progressbar(progress_card, 
                                           mode='determinate',
                                           length=400)
        self.progress_bar.pack(anchor='w', padx=20, pady=10)

        # ============ LOG SECTION ============
        log_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        log_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        ttk.Label(log_frame, 
                 text="📜 Scraping Log", 
                 style='CardTitle.TLabel').pack(anchor='w', padx=20, pady=(20, 10))

        self.log_text = tk.Text(log_frame, 
                               height=10, 
                               bg='#45475a', 
                               fg='#cdd6f4',
                               font=('Inter', 9),
                               relief='flat',
                               state='disabled')

        log_scroll = ttk.Scrollbar(log_frame, orient='vertical', command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)

        log_container = ttk.Frame(log_frame, style='Card.TFrame')
        log_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        self.log_text.pack(side='left', fill='both', expand=True)
        log_scroll.pack(side='right', fill='y')

    # ============ QUICK SELECT METHODS ============
    def select_all_fields(self):
        self.scrape_title_var.set(True)
        self.scrape_brand_var.set(True)
        self.scrape_price_var.set(True)
        self.scrape_rating_var.set(True)
        self.scrape_images_var.set(True)
        self.update_selected_fields_display()

    def deselect_all_fields(self):
        self.scrape_title_var.set(False)
        self.scrape_brand_var.set(False)
        self.scrape_price_var.set(False)
        self.scrape_rating_var.set(False)
        self.scrape_images_var.set(False)
        self.update_selected_fields_display()

    def select_only_images(self):
        self.scrape_title_var.set(False)
        self.scrape_brand_var.set(False)
        self.scrape_price_var.set(False)
        self.scrape_rating_var.set(False)
        self.scrape_images_var.set(True)
        self.update_selected_fields_display()

    def select_only_prices(self):
        self.scrape_title_var.set(False)
        self.scrape_brand_var.set(False)
        self.scrape_price_var.set(True)
        self.scrape_rating_var.set(False)
        self.scrape_images_var.set(False)
        self.update_selected_fields_display()

    def select_only_brands(self):
        self.scrape_title_var.set(False)
        self.scrape_brand_var.set(True)
        self.scrape_price_var.set(False)
        self.scrape_rating_var.set(False)
        self.scrape_images_var.set(False)
        self.update_selected_fields_display()

    def select_brand_price(self):
        self.scrape_title_var.set(False)
        self.scrape_brand_var.set(True)
        self.scrape_price_var.set(True)
        self.scrape_rating_var.set(False)
        self.scrape_images_var.set(False)
        self.update_selected_fields_display()

    def select_price_images(self):
        self.scrape_title_var.set(False)
        self.scrape_brand_var.set(False)
        self.scrape_price_var.set(True)
        self.scrape_rating_var.set(False)
        self.scrape_images_var.set(True)
        self.update_selected_fields_display()

    def update_selected_fields_display(self):
        fields = []
        if self.scrape_title_var.get():
            fields.append("Title")
        if self.scrape_brand_var.get():
            fields.append("Brand")
        if self.scrape_price_var.get():
            fields.append("Price")
        if self.scrape_rating_var.get():
            fields.append("Rating")
        if self.scrape_images_var.get():
            fields.append("Images")

        if fields:
            self.selected_fields_var.set(f"Selected fields: {', '.join(fields)}")
        else:
            self.selected_fields_var.set("Selected fields: None (Please select at least one)")

    def get_selected_fields(self):
        """Return dictionary of selected fields"""
        return {
            'title': self.scrape_title_var.get(),
            'brand': self.scrape_brand_var.get(),
            'price': self.scrape_price_var.get(),
            'rating': self.scrape_rating_var.get(),
            'images': self.scrape_images_var.get()
        }

    def create_results_tab(self):
        # Results Tab
        results_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(results_frame, text='📊 Results')

        # Results summary
        summary_card = ttk.Frame(results_frame, style='Card.TFrame')
        summary_card.pack(fill='x', padx=20, pady=20)

        ttk.Label(summary_card, 
                 text="Scraping Results", 
                 style='Title.TLabel').pack(anchor='w', padx=20, pady=(20, 10))

        self.results_summary_var = tk.StringVar(value="No data scraped yet")
        summary_label = ttk.Label(summary_card, 
                                 textvariable=self.results_summary_var,
                                 style='Card.TLabel')
        summary_label.pack(anchor='w', padx=20, pady=(0, 20))

        # Results table
        table_card = ttk.Frame(results_frame, style='Card.TFrame')
        table_card.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        ttk.Label(table_card, 
                 text="Product Data", 
                 style='Title.TLabel').pack(anchor='w', padx=20, pady=(20, 10))

        # Treeview for results - will be dynamically updated
        self.result_columns = ('ASIN', 'Brand', 'Title', 'Price', 'Rating', 'Images', 'Status')
        self.results_tree = ttk.Treeview(table_card, columns=self.result_columns, show='headings', height=12)

        for col in self.result_columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=100)

        results_scroll = ttk.Scrollbar(table_card, orient='vertical', command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=results_scroll.set)

        results_container = ttk.Frame(table_card, style='Card.TFrame')
        results_container.pack(fill='both', expand=True, padx=20, pady=(0, 10))

        self.results_tree.pack(side='left', fill='both', expand=True)
        results_scroll.pack(side='right', fill='y')

        # Export buttons
        export_frame = ttk.Frame(table_card, style='Card.TFrame')
        export_frame.pack(fill='x', padx=20, pady=20)

        ttk.Button(export_frame, 
                  text="📄 Export to Excel", 
                  style='Success.TButton',
                  command=self.export_to_excel).pack(side='left', padx=(0, 10))

        ttk.Button(export_frame, 
                  text="📦 Download Images ZIP", 
                  style='Modern.TButton',
                  command=self.download_images_zip).pack(side='left')

    def create_settings_tab(self):
        # Settings Tab
        settings_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(settings_frame, text='⚙️ Settings')

        # User Agent settings
        ua_card = ttk.Frame(settings_frame, style='Card.TFrame')
        ua_card.pack(fill='x', padx=20, pady=20)

        ttk.Label(ua_card, 
                 text="Request Headers", 
                 style='Title.TLabel').pack(anchor='w', padx=20, pady=(20, 10))

        ttk.Label(ua_card, 
                 text="User Agent:",
                 style='Card.TLabel').pack(anchor='w', padx=20, pady=(0, 5))

        self.user_agent_var = tk.StringVar(value="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        ua_entry = ttk.Entry(ua_card, textvariable=self.user_agent_var, width=80)
        ua_entry.pack(fill='x', padx=20, pady=(0, 20))

        # Output settings
        output_card = ttk.Frame(settings_frame, style='Card.TFrame')
        output_card.pack(fill='x', padx=20, pady=(0, 20))

        ttk.Label(output_card, 
                 text="Output Settings", 
                 style='Title.TLabel').pack(anchor='w', padx=20, pady=(20, 10))

        output_frame = ttk.Frame(output_card, style='Card.TFrame')
        output_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(output_frame, 
                 text="Output Directory:",
                 style='Card.TLabel').pack(anchor='w', pady=(0, 5))

        dir_frame = ttk.Frame(output_frame, style='Card.TFrame')
        dir_frame.pack(fill='x', pady=5)

        self.output_dir_var = tk.StringVar(value="./output")
        dir_entry = ttk.Entry(dir_frame, textvariable=self.output_dir_var, width=60)
        dir_entry.pack(side='left', padx=(0, 10))

        ttk.Button(dir_frame, 
                  text="Browse", 
                  style='Modern.TButton',
                  command=self.browse_output_dir).pack(side='left')

        # Image settings
        img_frame = ttk.Frame(output_card, style='Card.TFrame')
        img_frame.pack(fill='x', padx=20, pady=(10, 20))

        self.download_images_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(img_frame, 
                       text="Download product images",
                       variable=self.download_images_var,
                       style='Card.TCheckbutton').pack(anchor='w', pady=5)

        self.create_zip_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(img_frame, 
                       text="Create ZIP file for images",
                       variable=self.create_zip_var,
                       style='Card.TCheckbutton').pack(anchor='w', pady=5)

    def log_message(self, message):
        """Add message to log with timestamp"""
        self.log_text.config(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update_idletasks()

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select ASIN file",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)

    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select output directory")
        if directory:
            self.output_dir_var.set(directory)

    def load_asins(self):
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file first")
            return

        try:
            if file_path.endswith('.txt'):
                with open(file_path, 'r') as f:
                    asins = [line.strip() for line in f.readlines() if line.strip()]
            else:
                df = pd.read_excel(file_path)
                # Try to find ASIN column
                asin_col = None
                for col in df.columns:
                    if 'asin' in col.lower():
                        asin_col = col
                        break

                if asin_col is not None:
                    asins = df[asin_col].dropna().astype(str).tolist()
                else:
                    # Use first column
                    asins = df.iloc[:, 0].dropna().astype(str).tolist()

            self.asins = asins
            self.update_asin_display()
            self.log_message(f"Loaded {len(asins)} ASINs from {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def add_manual_asins(self):
        text_content = self.manual_text.get("1.0", tk.END).strip()
        if text_content:
            manual_asins = [line.strip() for line in text_content.split('\n') if line.strip()]
            self.asins.extend(manual_asins)
            self.update_asin_display()
            self.manual_text.delete("1.0", tk.END)
            self.log_message(f"Added {len(manual_asins)} ASINs manually")

    def update_asin_display(self):
        # Clear existing items
        for item in self.asin_tree.get_children():
            self.asin_tree.delete(item)

        # Add ASINs to tree
        for i, asin in enumerate(self.asins, 1):
            self.asin_tree.insert('', 'end', values=(i, asin))

    def start_scraping(self):
        if not self.asins:
            messagebox.showerror("Error", "Please load ASINs first")
            return

        # Check if at least one field is selected
        selected = self.get_selected_fields()
        if not any(selected.values()):
            messagebox.showerror("Error", "Please select at least one data field to scrape")
            return

        if self.scraping_active:
            messagebox.showwarning("Warning", "Scraping is already in progress")
            return

        self.scraping_active = True
        self.scraped_data = []

        # Clear results tree
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Update selected fields display
        self.update_selected_fields_display()

        # Setup progress
        self.progress_bar['maximum'] = len(self.asins)
        self.progress_bar['value'] = 0
        self.progress_var.set("Starting scraping process...")

        # Log selected fields
        fields_list = [k.capitalize() for k, v in selected.items() if v]
        self.log_message(f"Selected fields: {', '.join(fields_list)}")
        self.log_message("Starting Amazon ASIN scraping...")
        self.log_message(f"Target: {self.country_domains[self.country_var.get()]}")
        self.log_message(f"ASINs to process: {len(self.asins)}")
        self.log_message(f"Threads: {self.threads_var.get()}")

        # Start scraping in separate thread
        thread = threading.Thread(target=self.scrape_products)
        thread.daemon = True
        thread.start()

    def stop_scraping(self):
        self.scraping_active = False
        self.log_message("Stopping scraping process...")

    def scrape_products(self):
        """Main scraping function with threading"""
        domain = self.country_domains[self.country_var.get()]
        threads_count = int(self.threads_var.get())
        delay = float(self.delay_var.get())
        selected_fields = self.get_selected_fields()

        # Create output directory
        output_dir = self.output_dir_var.get()
        images_dir = os.path.join(output_dir, "images")
        os.makedirs(output_dir, exist_ok=True)
        if selected_fields['images']:
            os.makedirs(images_dir, exist_ok=True)

        # Thread function
        def scrape_asin(asin):
            if not self.scraping_active:
                return

            try:
                url = f"https://{domain}/dp/{asin}"
                headers = {
                    'User-Agent': self.user_agent_var.get(),
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Connection': 'keep-alive',
                }

                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Initialize product data with ASIN
                    product_data = {'ASIN': asin}

                    # Extract only selected fields
                    if selected_fields['title']:
                        product_data['Title'] = self.extract_title(soup)
                    else:
                        product_data['Title'] = 'N/A (Not Selected)'

                    if selected_fields['brand']:
                        product_data['Brand'] = self.extract_brand(soup)
                    else:
                        product_data['Brand'] = 'N/A (Not Selected)'

                    if selected_fields['price']:
                        product_data['Price'] = self.extract_price(soup)
                    else:
                        product_data['Price'] = 'N/A (Not Selected)'

                    if selected_fields['rating']:
                        product_data['Rating'] = self.extract_rating(soup)
                    else:
                        product_data['Rating'] = 'N/A (Not Selected)'

                    if selected_fields['images']:
                        images = self.extract_images(soup)
                        product_data['Images_Count'] = len(images)

                        # Download images if enabled
                        if self.download_images_var.get() and images:
                            brand = product_data.get('Brand', 'Unknown')
                            if brand == 'N/A (Not Selected)':
                                brand = self.extract_brand(soup)  # Get brand for folder naming
                            self.download_product_images(asin, images, images_dir, brand)
                    else:
                        product_data['Images_Count'] = 'N/A (Not Selected)'

                    product_data['Status'] = 'Success'

                    self.scraped_data.append(product_data)

                    # Update UI
                    self.root.after(0, lambda pd=product_data: self.update_results_display(pd))

                    # Log message based on what was scraped
                    log_info = asin
                    if selected_fields['title'] and product_data.get('Title', 'N/A') != 'N/A':
                        log_info = f"{asin}: {product_data['Title'][:40]}..."
                    self.root.after(0, lambda li=log_info: self.log_message(f"✓ Successfully scraped {li}"))

                else:
                    error_data = {
                        'ASIN': asin,
                        'Title': 'N/A',
                        'Brand': 'N/A',
                        'Price': 'N/A',
                        'Rating': 'N/A',
                        'Images_Count': 0,
                        'Status': f'HTTP {response.status_code}'
                    }
                    self.scraped_data.append(error_data)
                    self.root.after(0, lambda ed=error_data: self.update_results_display(ed))
                    self.root.after(0, lambda a=asin, sc=response.status_code: self.log_message(f"✗ Failed to scrape {a}: HTTP {sc}"))

            except Exception as e:
                error_data = {
                    'ASIN': asin,
                    'Title': 'N/A',
                    'Brand': 'N/A',
                    'Price': 'N/A',
                    'Rating': 'N/A',
                    'Images_Count': 0,
                    'Status': f'Error: {str(e)[:20]}'
                }
                self.scraped_data.append(error_data)
                self.root.after(0, lambda ed=error_data: self.update_results_display(ed))
                self.root.after(0, lambda a=asin, er=str(e): self.log_message(f"✗ Error scraping {a}: {er}"))

            # Update progress
            self.root.after(0, self.update_progress)

            # Delay between requests
            if self.scraping_active:
                time.sleep(delay + random.uniform(0, 1))

        # Process ASINs with threading
        processed = 0
        for i in range(0, len(self.asins), threads_count):
            if not self.scraping_active:
                break

            batch = self.asins[i:i+threads_count]
            threads = []

            for asin in batch:
                if not self.scraping_active:
                    break
                thread = threading.Thread(target=scrape_asin, args=(asin,))
                threads.append(thread)
                thread.start()

            # Wait for all threads in batch to complete
            for thread in threads:
                thread.join()

            processed += len(batch)
            self.root.after(0, lambda p=processed: self.progress_var.set(f"Processed {p}/{len(self.asins)} ASINs"))

        # Scraping completed
        self.scraping_active = False
        self.root.after(0, lambda: self.progress_var.set(f"Scraping completed! Processed {len(self.scraped_data)} ASINs"))
        self.root.after(0, lambda: self.log_message("✓ Scraping process completed!"))
        self.root.after(0, self.update_results_summary)

        # Create images ZIP if enabled and images were scraped
        if self.create_zip_var.get() and self.download_images_var.get() and selected_fields['images']:
            self.root.after(0, lambda: self.create_images_zip(images_dir))

    def extract_title(self, soup):
        """Extract product title"""
        selectors = [
            '#productTitle',
            '.product-title',
            '[data-automation-id="product-title"]',
            'h1.a-size-large'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        return 'N/A'

    def extract_brand(self, soup):
        """Extract brand name"""
        selectors = [
            '[data-automation-id="product-brand-popover"]',
            '#bylineInfo',
            '.author',
            '[data-testid="product-detail-brand"] span',
            '.po-brand .po-break-word'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text().strip()
                # Clean brand text
                if 'Visit the' in text:
                    text = text.replace('Visit the', '').replace('Store', '').strip()
                if 'Brand:' in text:
                    text = text.replace('Brand:', '').strip()
                return text
        return 'N/A'

    def extract_price(self, soup):
        """Extract product price"""
        selectors = [
            '.a-price-whole',
            '.a-offscreen',
            '[data-automation-id="product-price"] .sr-only',
            '.a-price.a-text-price.a-size-medium.apexPriceToPay .a-offscreen',
            '#corePrice_feature_div .a-price .a-offscreen'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price = element.get_text().strip()
                if price and price != '':
                    return price

        # Try alternative price selectors
        price_elements = soup.find_all('span')
        for element in price_elements:
            text = element.get_text().strip()
            if text and '$' in text and len(text) < 20:
                return text

        return 'N/A'

    def extract_rating(self, soup):
        """Extract product rating"""
        selectors = [
            '[data-hook="average-star-rating"] span.a-sr-only',
            '.reviewCountTextLinkedHistogram .a-sr-only',
            '[data-automation-id="product-rating-badge"] span.a-sr-only'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                rating = element.get_text().strip()
                if 'out of' in rating:
                    return rating.split()[0]
        return 'N/A'

    def extract_images(self, soup):
        """Extract product image URLs"""
        images = []

        # Main product images
        img_elements = soup.find_all('img', {'data-a-image-name': True})
        for img in img_elements:
            if img.get('src'):
                # Get high resolution version
                src = img['src']
                if '._' in src:
                    high_res = src.split('._')[0] + '._AC_SL1500_.jpg'
                    images.append(high_res)
                else:
                    images.append(src)

        # Alternative image selectors
        if not images:
            img_selectors = [
                '#landingImage',
                '[data-automation-id="product-image"] img',
                '.image.item img'
            ]

            for selector in img_selectors:
                elements = soup.select(selector)
                for element in elements:
                    if element.get('src'):
                        images.append(element['src'])

        return list(set(images))  # Remove duplicates

    def download_product_images(self, asin, image_urls, images_dir, brand="Unknown"):
        """Download product images into brand-wise folders"""
        # Sanitize brand name for folder creation
        if not brand or brand.strip() == "" or brand == "N/A" or "Not Selected" in str(brand):
            brand = "Unknown"
        safe_brand = "".join(c for c in brand if c.isalnum() or c in (" ", "_", "-")).strip()

        # Create brand folder
        brand_dir = os.path.join(images_dir, safe_brand)
        os.makedirs(brand_dir, exist_ok=True)

        for i, img_url in enumerate(image_urls[:5]):  # Limit to 5 images per product
            try:
                response = requests.get(img_url, timeout=10)
                if response.status_code == 200:
                    # Determine file extension
                    if img_url.lower().endswith('.jpg') or 'jpg' in img_url.lower():
                        ext = '.jpg'
                    elif img_url.lower().endswith('.png') or 'png' in img_url.lower():
                        ext = '.png'
                    else:
                        ext = '.jpg'  # Default

                    # Save as ASIN_number.ext inside brand folder
                    filename = f"{asin}_{i+1}{ext}"
                    filepath = os.path.join(brand_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(response.content)

            except Exception as e:
                self.root.after(0, lambda a=asin, er=str(e): self.log_message(f"Failed to download image for {a}: {er}"))


    def update_results_display(self, product_data):
        """Update results tree view"""
        title_display = str(product_data.get('Title', 'N/A'))
        if len(title_display) > 50:
            title_display = title_display[:50] + '...'

        self.results_tree.insert('', 'end', values=(
            product_data.get('ASIN', 'N/A'),
            product_data.get('Brand', 'N/A'),
            title_display,
            product_data.get('Price', 'N/A'),
            product_data.get('Rating', 'N/A'),
            product_data.get('Images_Count', 'N/A'),
            product_data.get('Status', 'N/A')
        ))

    def update_progress(self):
        """Update progress bar"""
        current_value = self.progress_bar['value']
        self.progress_bar['value'] = current_value + 1

    def update_results_summary(self):
        """Update results summary"""
        total = len(self.scraped_data)
        successful = len([d for d in self.scraped_data if d.get('Status') == 'Success'])
        failed = total - successful

        # Show which fields were scraped
        selected = self.get_selected_fields()
        fields_list = [k.capitalize() for k, v in selected.items() if v]

        summary = f"Total: {total} | Successful: {successful} | Failed: {failed} | Fields: {', '.join(fields_list)}"
        self.results_summary_var.set(summary)

    def export_to_excel(self):
        """Export scraped data to Excel - only include selected fields"""
        if not self.scraped_data:
            messagebox.showwarning("Warning", "No data to export")
            return

        try:
            output_dir = self.output_dir_var.get()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"amazon_scraped_data_{timestamp}.xlsx"
            filepath = os.path.join(output_dir, filename)

            # Create DataFrame and filter columns based on selection
            df = pd.DataFrame(self.scraped_data)

            # Get selected fields
            selected = self.get_selected_fields()

            # Define column mapping
            columns_to_keep = ['ASIN']  # Always keep ASIN
            if selected['title']:
                columns_to_keep.append('Title')
            if selected['brand']:
                columns_to_keep.append('Brand')
            if selected['price']:
                columns_to_keep.append('Price')
            if selected['rating']:
                columns_to_keep.append('Rating')
            if selected['images']:
                columns_to_keep.append('Images_Count')
            columns_to_keep.append('Status')  # Always keep Status

            # Filter DataFrame to only include selected columns
            df_export = df[[col for col in columns_to_keep if col in df.columns]]

            df_export.to_excel(filepath, index=False)

            self.log_message(f"✓ Data exported to: {filepath}")
            messagebox.showinfo("Success", f"Data exported successfully to:\n{filepath}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")

    def create_images_zip(self, images_dir):
        """Create ZIP file containing all downloaded images, preserving brand folder structure"""
        try:
            output_dir = self.output_dir_var.get()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_filename = f"amazon_product_images_{timestamp}.zip"
            zip_filepath = os.path.join(output_dir, zip_filename)

            with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root_dir, dirs, files in os.walk(images_dir):
                    for file in files:
                        file_path = os.path.join(root_dir, file)
                        if os.path.isfile(file_path):
                            # Keep relative folder structure inside ZIP
                            arcname = os.path.relpath(file_path, images_dir)
                            zipf.write(file_path, arcname)

            self.log_message(f"✓ Images ZIP created: {zip_filepath}")

        except Exception as e:
            self.log_message(f"✗ Failed to create ZIP: {str(e)}")


    def download_images_zip(self):
        """Manual trigger for downloading images ZIP"""
        images_dir = os.path.join(self.output_dir_var.get(), "images")
        if os.path.exists(images_dir):
            # Check if there are any files in subdirectories
            has_files = False
            for root, dirs, files in os.walk(images_dir):
                if files:
                    has_files = True
                    break

            if has_files:
                self.create_images_zip(images_dir)
                messagebox.showinfo("Success", "Images ZIP file created successfully!")
            else:
                messagebox.showwarning("Warning", "No images found to zip")
        else:
            messagebox.showwarning("Warning", "No images found to zip")



def main():
    """Main function to run the application"""
    # Create the main window
    root = tk.Tk()

    # Set window properties
    root.resizable(True, True)
    root.minsize(1000, 700)

    # Create and run the application
    app = AmazonASINScraper(root)

    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    # Start the GUI event loop
    root.mainloop()



if __name__ == "__main__":
    main()


# Installation Instructions:
# Run this command to install required packages:
# pip install pandas requests beautifulsoup4 pillow openpyxl lxml


# Application Features:
# ✅ Beautiful modern dark theme UI
# ✅ Multi-tab interface (Input, Scraping, Results, Settings)
# ✅ Excel/TXT file input support for ASINs
# ✅ Manual ASIN input capability
# ✅ Multi-threading support (1-10 threads)
# ✅ Multiple Amazon country/region support
# ✅ Real-time progress tracking and logging
# ✅ SELECTABLE DATA FIELDS - Choose what to scrape:
#    - Title only
#    - Brand only
#    - Price only
#    - Rating only
#    - Images only
#    - Any combination (Brand + Price, Price + Images, etc.)
# ✅ Quick select buttons for common combinations
# ✅ Smart Excel export - only includes selected fields
# ✅ All images saved in brand-wise folders (ASIN_1.jpg, ASIN_2.jpg, etc.)
# ✅ ZIP file creation for all downloaded images
# ✅ Configurable request delays and headers
# ✅ Comprehensive error handling and status reporting
