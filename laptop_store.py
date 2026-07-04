import tkinter as tk
from tkinter import ttk, messagebox
import random

# --- Laptop specifications ---
specs = ["Brand","Model","CPU","Speed","RAM","Storage","Screensize"]

master_dict = {
    "Brands":["Wdell","Wlenovo","Wacer","Wasus","WHP"],
    "Models":["AAA","BBB","CCC"],
    "CPUs":["Wintel i5","Wintel i7","WAMD ryzen"],
    "Speeds":["2GHz","3GHz","3.5GHz"],
    "RAMs":["2 GB","4 GB","8 GB"],
    "Storages":["128 GB","256 GB","512 GB","1 TB"],
    "Screensizes":["9 in","12 in","14.9 in","17 in"]
}

# --- Bonuses system ---
bonuses = [
    "Free Mouse", "Extended Warranty", "Laptop Bag",
    "Cooling Pad", "Headset", "Free Antivirus",
    "Discount Coupon", "USB Hub",
    "Wireless Charger", "Bluetooth Speaker", "Portable SSD",
    "Stylus Pen", "Screen Cleaning Kit"
]

# --- Combo bonuses system ---
combo_bonuses = {
    ("WAMD ryzen", "1 TB"): ["Gaming Mouse", "RGB Keyboard"],
    ("Wintel i7", "512 GB"): ["Docking Station"],
    ("Epic",): ["Premium Cooling Pad"],
    ("Legendary",): ["VR Headset", "Extended Warranty"],
    ("Mythic",): ["Gold-Plated Mouse", "Exclusive Skin"],
    ("Rare",): ["Custom Laptop Skin"],
    ("Uncommon",): ["Extra USB-C Cable"],
    ("Legendary", "17 in"): ["4K External Monitor"]
}

def apply_combo_bonuses(laptop):
    extra = []
    for combo, rewards in combo_bonuses.items():
        if len(combo) == 1 and laptop["Rarity"] == combo[0]:
            extra.extend(rewards)
        elif len(combo) == 2 and laptop["CPU"] == combo[0] and laptop["Storage"] == combo[1]:
            extra.extend(rewards)
        elif len(combo) == 2 and laptop["Rarity"] == combo[0] and laptop["Screensize"] == combo[1]:
            extra.extend(rewards)
    return extra

# --- Rarity weights ---
rarity_weights = {
    "CPUs": {"Wintel i5":0.5, "Wintel i7":0.3, "WAMD ryzen":0.2},
    "Speeds": {"2GHz":0.5, "3GHz":0.3, "3.5GHz":0.2},
    "RAMs": {"2 GB":0.5, "4 GB":0.3, "8 GB":0.2},
    "Storages": {"128 GB":0.4, "256 GB":0.3, "512 GB":0.2, "1 TB":0.1},
    "Screensizes": {"9 in":0.4, "12 in":0.3, "14.9 in":0.2, "17 in":0.1}
}

def weighted_choice(options):
    return random.choices(list(options.keys()), weights=list(options.values()), k=1)[0]

# --- Rarity calculation ---
def rarity_from_score(score):
    if score <= 5:
        return "Common","₹20000"
    elif score <= 7:
        return "Uncommon","₹25000"
    elif score <= 9:
        return "Rare","₹30000"
    elif score == 10:
        return "Epic","₹35000"
    elif score == 11:
        return "Legendary","₹40000"
    else:  # score >= 12
        return "Mythic","₹50000"

def calculate_rarity_and_price(laptop):
    score = 0
    if laptop["CPU"] == "WAMD ryzen": score += 3
    elif laptop["CPU"] == "Wintel i7": score += 2
    else: score += 1
    if laptop["Speed"] == "3.5GHz": score += 3
    elif laptop["Speed"] == "3GHz": score += 2
    else: score += 1
    if laptop["RAM"] == "8 GB": score += 3
    elif laptop["RAM"] == "4 GB": score += 2
    else: score += 1
    if laptop["Storage"] == "1 TB": score += 3
    elif laptop["Storage"] == "512 GB": score += 2
    else: score += 1
    rarity, price = rarity_from_score(score)
    return rarity, price, score

# --- Generate laptops ---
def generate_laptops(n=30):
    laptops = []
    for _ in range(n):
        new_laptop = {}
        for kk in specs:
            if kk+"s" in rarity_weights:
                new_laptop[kk] = weighted_choice(rarity_weights[kk+"s"])
            else:
                new_laptop[kk] = random.choice(master_dict[kk+"s"])
        new_laptop["Bonuses"] = random.sample(bonuses + ["None"], k=random.randint(1,3))
        rarity, price, score = calculate_rarity_and_price(new_laptop)
        new_laptop["Rarity"] = rarity
        new_laptop["Price"] = price
        new_laptop["Score"] = score
        extra = apply_combo_bonuses(new_laptop)
        if extra:
            new_laptop["Bonuses"].extend(extra)
            new_laptop["Score"] += len(extra)
            new_laptop["Rarity"], new_laptop["Price"] = rarity_from_score(new_laptop["Score"])
        laptops.append(new_laptop)
    return laptops

laptop_list = generate_laptops(10000)

# --- Tkinter GUI ---
root = tk.Tk()
root.title("Laptop Store")
root.geometry("1300x700")

# --- Preferences bar with horizontal scroll ---
pref_container = tk.Frame(root)
pref_container.pack(side=tk.TOP, fill=tk.X)

canvas = tk.Canvas(pref_container, height=80)
scroll_x = tk.Scrollbar(pref_container, orient="horizontal", command=canvas.xview)
scroll_frame = tk.Frame(canvas)
scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.configure(xscrollcommand=scroll_x.set)
canvas.pack(side=tk.TOP, fill=tk.X, expand=True)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

# --- Preferences dropdowns for ALL specs + Bonus + Rarity + Price ---
pref_vars = {}
for kk in specs + ["Bonus","Rarity","Price"]:
    lbl = tk.Label(scroll_frame, text=f"{kk} Preference:")
    lbl.pack(side=tk.LEFT, padx=5)
    var = tk.StringVar(value="none")
    if kk == "Bonus":
        values = ["none"] + bonuses
    elif kk == "Screensize":
        values = ["none"] + master_dict["Screensizes"]
    elif kk == "Rarity":
        values = ["none","Common","Uncommon","Rare","Epic","Legendary","Mythic"]
    elif kk == "Price":
        values = ["none","₹20000","₹25000","₹30000","₹35000","₹40000","₹50000"]
    else:
        values = ["none"] + master_dict[kk+"s"]
    combo = ttk.Combobox(scroll_frame, textvariable=var, values=values, height=10, width=15)
    combo.pack(side=tk.LEFT, padx=5)
    pref_vars[kk] = var

# --- Treeview with vertical + horizontal scrollbar ---
tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True)

tree_scroll_y = tk.Scrollbar(tree_frame, orient="vertical")
tree_scroll_x = tk.Scrollbar(tree_frame, orient="horizontal")

tree = ttk.Treeview(
    tree_frame,
    columns=specs + ["Rarity","Price","Bonuses"],
    show="headings",
    yscrollcommand=tree_scroll_y.set,
    xscrollcommand=tree_scroll_x.set
)

tree_scroll_y.config(command=tree.yview)
tree_scroll_x.config(command=tree.xview)

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

# Configure headings and column widths (make wider to force horizontal scroll)
for col in specs + ["Rarity","Price","Bonuses"]:
    tree.heading(col, text=col)
    tree.column(col, width=200, stretch=True)

# --- Fortnite rarity colors ---
rarity_colors = {
    "Common":"gray",
    "Uncommon":"green",
    "Rare":"blue",
    "Epic":"purple",
    "Legendary":"orange",
    "Mythic":"red"
}
for rarity, color in rarity_colors.items():
    tree.tag_configure(rarity, foreground=color)

# --- Update table based on preferences ---
# --- Update table based on preferences ---
def update_table(*args):
    for row in tree.get_children():
        tree.delete(row)
    for laptop in laptop_list:
        match = True
        for kk in specs+["Bonus","Rarity","Price"]:
            pref = pref_vars[kk].get()
            if pref.lower() != "none":
                if kk == "Bonus":
                    if pref not in laptop["Bonuses"]:
                        match = False
                        break
                elif laptop[kk] != pref:
                    match = False
                    break
        if match:
            values = [laptop[kk] for kk in specs] + [
                laptop["Rarity"],
                laptop["Price"],
                ", ".join(laptop["Bonuses"])  # show bonuses in table
            ]
            tree.insert("", tk.END, values=values, tags=(laptop["Rarity"],))

# Attach preference change triggers
for var in pref_vars.values():
    var.trace("w", update_table)

# --- Initial table population ---
update_table()

# --- Show full bonuses on double-click ---
def on_row_click(event):
    selected_item = tree.focus()
    if not selected_item:
        return
    laptop_values = tree.item(selected_item, "values")
    brand, model = laptop_values[0], laptop_values[1]
    for laptop in laptop_list:
        if laptop["Brand"] == brand and laptop["Model"] == model:
            bonuses_text = "\n".join(laptop["Bonuses"])
            messagebox.showinfo(
                "Laptop Bonuses",
                f"Full bonuses for {brand} {model}:\n\n{bonuses_text}"
            )
            break

tree.bind("<Double-1>", on_row_click)

# --- Run the app ---
root.mainloop()
