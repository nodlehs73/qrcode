import sys
from read_qr_code_normal import read_qr_code_normal
from read_qr_code_structured_append import read_qr_code_structured_append
from generate_qrcode import get_single_qr_code, get_multiple_qr_codes

arguments = sys.argv[1:]

# Vrem sa generam folosind modul normal, atunci comanda este
# python3 qrcode.py generate_normal [message] [error_correction_level] [file_path]

# Vrem sa citim folosind modul structured_append, atunci comanda este
# Imaginile se salveaza in folder-ul din proiect numit "photos"

#python3 qrcode.py generate_structured_append [message] [error_correction_level] [number_of_splits]

# Vrem sa citim normal, atunci comanda este
# python3 qrcode.py normal_read [path_qr_code]

# Vrem sa citim cu modul structured append, atunci comanda este
# Citim din folder-ul photos din proiect
# python3 qrcode.py structured_append_read

command_type = arguments[0]

if command_type == "generate_normal":
    message = arguments[1]
    error_correction_level = arguments[2]
    path = arguments[3]
    get_single_qr_code(message, error_correction_level, path)
elif command_type == "generate_structured_append":
    message, error_correction_level, number_of_splits = arguments[1:]
    number_of_splits = int(number_of_splits)

    get_multiple_qr_codes(message, error_correction_level, number_of_splits)
elif command_type == "normal_read":
    path_qr_code = arguments[1]
    read_qr_code_normal(path_qr_code)
elif command_type == "structured_append_read":
    read_qr_code_structured_append()
else:
    print("Unknown command")