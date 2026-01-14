import tkinter as tk
from tkinter import messagebox, filedialog
import string
import random
import os
import sys
import tempfile
import platform
from PIL import Image, ImageTk

# ================= Funcții =================
def genereaza_parola():
    try:
        lungime = int(entry_lungime.get())
        include_cifre = var_cifre.get()
        include_speciale = var_speciale.get()
        optiune_litere = var_litere.get()

        caractere = ""

        # AICI ERA PROBLEMA: Am actualizat valorile să corespundă cu cele din engleză
        if optiune_litere == "Small":      # Era "mici"
            caractere += string.ascii_lowercase
        elif optiune_litere == "Capital":  # Era "mari"
            caractere += string.ascii_uppercase
        elif optiune_litere == "Both":     # Era "ambele"
            caractere += string.ascii_letters

        if include_cifre:
            caractere += string.digits
        if include_speciale:
            caractere += string.punctuation

        if not caractere:
            messagebox.showerror("Eroare", "Selectează cel puțin un tip de caractere!")
            return

        parola = ''.join(random.choice(caractere) for _ in range(lungime))
        entry_rezultat.delete(0, tk.END)
        entry_rezultat.insert(0, parola)

        actualizeaza_strength_bar(parola)

    except ValueError:
        messagebox.showerror("Eroare", "Introdu o lungime validă!")

def salveaza_parola():
    parola = entry_rezultat.get()
    if parola:
        fisier = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if fisier:
            with open(fisier, "w") as f:
                f.write(parola)
            messagebox.showinfo("Succed", "Password has been saved!")
    else:
        messagebox.showwarning("Warning", "Generate password first!")

def printeaza_parola():
    parola = entry_rezultat.get()
    if parola:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w') as tmp:
            tmp.write(parola)
            tmp_path = tmp.name
        if platform.system() == "Windows":
            os.startfile(tmp_path, "print")
        else:
            os.system(f"lp {tmp_path}")
    else:
        messagebox.showwarning("Warning", "Generate password first!")

def calculeaza_putere(parola):
    scor = 0
    lungime = len(parola)
    if lungime >= 8:
        scor += 2
    if lungime >= 12:
        scor += 2
    if any(c.isdigit() for c in parola):
        scor += 2
    if any(c in string.punctuation for c in parola):
        scor += 2
    if any(c.islower() for c in parola) and any(c.isupper() for c in parola):
        scor += 2
    return min(int((scor / 10) * 20), 20)

def actualizeaza_strength_bar(parola):
    strength = calculeaza_putere(parola)
    for i in range(20):
        if i < strength:
            if strength <= 6:
                culoare = "#ff4d4d"  # rosu
            elif strength <= 13:
                culoare = "#ffcc00"  # galben
            else:
                culoare = "#33cc33"  # verde
            bar_segments[i].config(bg=culoare)
        else:
            bar_segments[i].config(bg="#444444")

# ================= Interfață GUI =================
root = tk.Tk()
root.title("= Password Generator V0.1 =")
root.geometry("380x250")
root.configure(bg="#1e1e1e")

# Setează pictograma aplicației (ico) dacă există
def resource_path(relative_path):
    """ Obține calea absolută către resurse, funcționează și pentru dev și pentru PyInstaller """
    try:
        # PyInstaller creează un folder temporar și stochează calea în _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

folder_curent = resource_path("")

ico_path = os.path.join(folder_curent, "Icon.ico")
if os.path.exists(ico_path):
    try:
        root.iconbitmap(ico_path)
    except Exception as e:
        print(f"Icon Error: {e}")
else:
    print("File 'Icon.ico' not found in root folder.")

# Culori și fonturi
grey = "#2e2e2e"
white = "#f0f0f0"
font = ("Segoe UI", 10)

# Stiluri vizuale pentru Checkbutton și Radiobutton
style_args = {
    "selectcolor": grey,
    "activebackground": "#1e1e1e",
    "bg": "#1e1e1e",
    "fg": white,
    "font": font
}

# Etichete
tk.Label(root, text="Password Length  = ", bg="#1e1e1e", fg=white, font=font).place(x=10, y=10)
tk.Label(root, text="Characters", bg="#1e1e1e", fg=white, font=font).place(x=185, y=10)
entry_lungime = tk.Entry(root, bg=grey, fg=white, font=font, width=5)
entry_lungime.place(x=140, y=12)

# Bife opțiuni
var_cifre = tk.BooleanVar()
check_cifre = tk.Checkbutton(root, text="Include Numbers", variable=var_cifre, **style_args)
check_cifre.place(x=10, y=30)

var_speciale = tk.BooleanVar()
check_speciale = tk.Checkbutton(root, text="Include Special Characters", variable=var_speciale, **style_args)
check_speciale.place(x=10, y=50)

# Litere mici/mari
var_litere = tk.StringVar(value="Both")
tk.Label(root, text="Letter Type:", bg="#1e1e1e", fg=white, font=font).place(x=10, y=82)

tk.Radiobutton(root, text="Small", variable=var_litere, value="Small", **style_args).place(x=82, y=80)
tk.Radiobutton(root, text="Capital", variable=var_litere, value="Capital", **style_args).place(x=138, y=80)
tk.Radiobutton(root, text="Both", variable=var_litere, value="Both", **style_args).place(x=202, y=80)

# Buton generare
btn_gen = tk.Button(root, text="Generate", command=genereaza_parola, bg="#3e3e3e", fg=white, font=font)
btn_gen.place(x=22, y=185)

# Câmp parolă
entry_rezultat = tk.Entry(root, bg=grey, fg=white, font=("Consolas", 12), width=37)
entry_rezultat.place(x=20, y=120)

# Bara de putere (20 segmente)
bar_frame = tk.Frame(root, bg="#1e1e1e")
bar_frame.place(x=20, y=160)
bar_segments = []
for i in range(20):
    segment = tk.Frame(bar_frame, bg="#444444", width=15, height=10)
    segment.grid(row=0, column=i, padx=1)
    bar_segments.append(segment)

# Butoane suplimentare
btn_salveaza = tk.Button(root, text=" Save ", command=salveaza_parola, bg="#3e3e3e", fg=white, font=font)
btn_salveaza.place(x=170, y=185)

btn_printeaza = tk.Button(root, text="  Print  ", command=printeaza_parola, bg="#3e3e3e", fg=white, font=font)
btn_printeaza.place(x=305, y=185)

# Informații autor/versiune
tk.Label(root, text="= diwhy.engineering.86@gmail.com =", bg="#1e1e1e", fg="#888888", font=("Segoe UI", 9)).place(x=90, y=220)

# Afișare imagine Logo.png în rezoluția originală
logo_path = os.path.join(folder_curent, "Logo.png")
if os.path.exists(logo_path):
    try:
        imagine_originala = Image.open(logo_path)
        imagine_tk = ImageTk.PhotoImage(imagine_originala)
        eticheta_imagine = tk.Label(root, image=imagine_tk, bg="#1e1e1e")
        eticheta_imagine.image = imagine_tk  # păstrează referința
        eticheta_imagine.place(x=260, y=10)
    except Exception as e:
        print(f"Eroare la afișarea imaginii logo: {e}")
else:
    print("Image 'Logo.png' not found in root folder.")

root.mainloop()
