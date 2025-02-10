# Cititor si Generator de Coduri QR

## Descriere

Acest proiect este o aplicație completă pentru generarea și decodarea codurilor QR, oferind funcționalități avansate pentru personalizarea și manipularea datelor.

---

### 1. **Generare Coduri QR**
- Utilizatorul poate introduce un mesaj pentru a fi encodat într-un cod QR.
- Aplicația permite alegerea nivelului de **error correction** (L, M, Q, H) pentru a controla rezistența codului QR la deteriorare.
- Programul optimizează dimensiunea codului QR, selectând automat **cea mai mică versiune posibilă** care poate conține mesajul.

### 2. **Modul Structured Append**
- Utilizatorul poate activa opțiunea **structured append**, care împarte mesajele lungi în mai multe coduri QR.
- Fiecare cod QR conține informații adiționale necesare pentru reconstrucția mesajului:
  - Encoding special: `0011`.
  - Poziția secțiunii în mesajul complet.
  - Lungimea totală a mesajului.
  - Paritatea pentru verificarea integrității datelor.
- Codurile QR multiple pot fi citite în orice ordine, iar programul va reconstitui corect mesajul.

### 3. **Decodare Coduri QR**
- Programul poate decoda atât coduri QR standard, cât și cele generate cu **structured append**.
- La detectarea mai multor coduri QR cu structured append, aplicația le reordonează automat, verifică paritatea și reconstituie mesajul inițial.

## **Functionalitati ale fiecarui fisier**

---

## 1. read_qr_code_normal.py

### 1.1. Detectarea informațiilor de bază
Codul extrage informațiile esențiale din codul QR, cum ar fi:
- **Versiunea QR**  
- **Nivelul de corecție a erorilor (EC)**  
- **Masca aplicată QR-ului**  
Acestea sunt citite din format string-ul stocat în matricea QR.


### 1.2. Anularea măștii aplicate
Pe baza valorii `mask_pattern`, matricea QR este readusă la forma inițială. Aceasta implică inversarea modulelor specificate, pentru a putea decoda corect datele.


### 1.3. Extracția datelor codificate
Codul parcurge matricea QR pentru a extrage datele codificate sub formă de `data codewords`. Acestea sunt organizate într-o matrice de mesaje, urmând să fie citite secvențial.


### 1.4. Corectarea erorilor
Algoritmul implementează corecția erorilor folosind **algoritmul de corectie Reed-Solomon **.  
- Sunt extrase atât `data codewords`, cât și `error codewords`.  
- După aplicarea corecției, se reconstruiește un șir de date secvențial corect.


### 1.5. Reconstrucția mesajului
Codul reconstituie mesajul complet folosind informațiile despre poziția fiecărui cod QR în secvență.  
- Mesajele multiple sunt reasamblate în ordinea corectă.

---

### 2. read_qr_code_structured_append.py
Acest program implementează citirea, decodarea și corectarea mesajelor din coduri QR structurale ("structured append"). Spre deosebire de versiunea anterioară, acesta poate procesa mai multe imagini QR dintr-un folder și reconstruiește mesajele complete, indiferent de ordinea în care sunt citite codurile QR.


### 2.1. Detectarea informațiilor de bază
Programul citește informațiile esențiale din format string-ul codului QR, cum ar fi:
- **Versiunea QR**  
- **Nivelul de corecție a erorilor (EC)**  
- **Masca aplicată**

### 2.2. Anularea măștii aplicate
Pe baza valorii `mask_pattern`, matricea QR este readusă la forma inițială, prin inversarea modulelor specifice. Acest pas este necesar pentru a decoda corect datele.

### 2.3. Extracția datelor codificate
Programul parcurge matricea QR pentru a extrage datele intercalate (`data codewords`). Acestea sunt organizate într-o matrice de mesaje și citite secvențial.


### 2.4. Corectarea erorilor
Algoritmul implementează corecția erorilor folosind **algoritmul de corectie Reed-Solomon**.  
- Sunt extrase atât `data codewords`, cât și `error codewords`.  
- După corectare, se reconstruiește un șir de date secvențial corect.

### 2.5. Reconstrucția mesajului complet
Codurile QR multiple sunt folosite pentru a reconstitui mesajele mari împărțite în părți. Fiecare cod QR conține informații despre poziția sa în mesajul complet, iar mesajele sunt reasamblate în ordinea corectă.


Acest program implementează generarea de coduri QR, incluzând suport pentru:  
- **Coduri QR individuale**  
- **Coduri QR structurale ("structured append")** pentru mesaje mari împărțite pe mai multe coduri.  
Programul gestionează automat corecția erorilor, alegerea celei mai bune măști și generarea imaginilor QR.

---

## 3. generate_qr_code.py

### 3.1. Generarea string-ului de format  
Funcția `generate_format_string` generează un string de format care conține nivelul de corecție a erorilor și masca selectată pentru QR. Acest string este inserat în matricea QR.

### 3.2. Corecția erorilor cu coduri Reed-Solomon
Pentru fiecare bloc de date, programul generează `error codewords` folosind algoritmul **Reed-Solomon (`RSCodec`)**. Această corecție permite recuperarea datelor în cazul deteriorării parțiale a codului QR.


### 3.3. Alegerea celei mai bune măști  
Funcțiile din fișierul `best_mask` aplică opt măști posibile pe matricea QR. Se calculează penalități (`total_penalty`), iar masca cu cea mai mică penalitate este selectată automat.


### 3.4. Generarea unui cod QR individual
Funcția `get_single_qr_code` procesează un mesaj unic, transformându-l în blocuri de date și aplicând corecția erorilor. Codul QR este generat și salvat ca imagine.


### 3.5. Generarea codurilor QR structurale ("structured append")
Funcția `get_multiple_qr_codes` împarte mesajele mari în părți mai mici, fiecare cod QR conținând informații despre poziția sa în mesajul complet și paritatea întregului mesaj. Programul poate genera până la 16 coduri QR pentru un singur mesaj.

---

## 4. qr_code_data_encoding.py

Această funcție `transformare` encodează mesajul într-un format compatibil pentru generarea unui cod QR, incluzând adăugarea informațiilor necesare, cum ar fi lungimea mesajului, modul de codificare (Byte Mode) și, dacă este cazul, un **header de structured append**. De asemenea, împarte mesajul în blocuri pentru gestionarea corecției de erori.

### 4.1. Adăugarea header-ului de structured append (opțional)
Dacă este activată opțiunea `structured_append`, funcția adaugă un header care conține următoarele informații:
- **Poziția codului QR în secvență**  
- **Numărul total de coduri QR din secvență**  
- **Paritatea mesajului**


### 4.2. Specificarea modului de codificare
Funcția inițializează encoding-ul cu indicatorul de **Byte Mode** (`0100`), specific pentru mesaje bazate pe caractere ASCII.


### 4.3. Adăugarea lungimii mesajului
Funcția determină lungimea mesajului și o encodează sub formă binară. Lungimea depinde de versiunea QR utilizată:
- Versiuni 1-9: 8 biți pentru lungime  
- Versiuni 10-40: 16 biți pentru lungime  


### 4.4. Transformarea fiecărui caracter în cod binar
Fiecare caracter din mesaj este convertit într-o secvență binară de 8 biți și concatenat la fluxul final de date.


### 4.5. Completarea fluxului de date
Funcția adaugă date suplimentare pentru a respecta cerințele codului QR:
- Adaugă un minim de 4 biți `0` dacă fluxul nu este complet  
- Completează fluxul cu secvențe alternante `11101100` și `00010001` până când atinge dimensiunea necesară în funcție de versiunea și nivelul de corecție a erorilor


### 4.6. Împărțirea în blocuri de date
După generarea fluxului complet de date, funcția împarte datele în blocuri, conform specificațiilor QR pentru versiunea și nivelul de corecție a erorilor:
- **Primul grup de blocuri** – conține un număr specific de blocuri și codewords  
- **Al doilea grup de blocuri** (dacă există) – poate conține mai puține blocuri și codewords  

---

## 5. qr_to_matrix.py

Acest program implementează funcționalități pentru conversia între imagini cu coduri QR și matrice binare, precum și generarea de imagini PNG dintr-o matrice binară.


### 1. Conversia unei imagini QR în matrice binară (`png_to_binary_matrix`)
Această funcție transformă o imagine QR într-o matrice de 0 și 1, unde:  
- **1** reprezintă un pixel negru.  
- **0** reprezintă un pixel alb.


### 2. Generarea unei imagini PNG din matrice binară (`matrix_to_qrcode`)
Această funcție creează o imagine PNG pe baza unei matrice binare.

Funcționarea procesului:
1. Fiecare pixel din matrice este colorat în negru sau alb, în funcție de valoarea sa.
2. Imaginea este scalată pentru o rezoluție mai bună.
3. Imaginea este salvată într-un fișier PNG:
   - Dacă opțiunea `structured_append` este activată, fișierul este salvat cu un nume generat aleator în folderul `photos/`.
   - În caz contrar, imaginea este salvată cu numele specificat.

---

## Cum se foloseste programul ?
### Cu ajutorul fisierului **qr_code.py** putem rula programul. Acest fisier asista la generarea/citirea codurilor QR prin intermediul terminalului.

### Generare cod QR normal
```bash
python3 qr_code.py generate_normal [message] [error_correction_level] [file_path]
```
  - Message este textul pe care doriți să-l codificați în QR.
  - Error_correction_level poate fi unul dintre: L, M, Q, H (nivelul de corecție al erorilor în QR).
  - File_path reprezintă locația unde se va salva imaginea QR generată (ex. qrcode.png).

### Generare coduri QR folosind structured append
```bash
python3 qr_code.py generate_structured_append [message] [error_correction_level] [number_of_splits]
```
  - Message este textul pe care doriți să-l codificați.
  - Error_correction_level poate fi: L, M, Q, H.
  - Number_of_splits indică în câte segmente se împarte textul (câte coduri QR vor fi generate, maxim 16).
  - Imaginile rezultate sunt salvate implicit în folderul photos din proiect.

### Citire cod QR normal
```bash
python3 qr_code.py normal_read [path_qr_code]
```
  - path_qr_code este calea către fișierul imagine care conține codul QR de citit (ex. qrcode.png).

### Citire cod QR folosind structured_append
```bash
python3 qr_code.py structured_append_read
```
Această comandă citește automat toate imaginile din folderul **photos** și asamblează mesajul dacă acesta este împărțit în mai multe coduri QR.

