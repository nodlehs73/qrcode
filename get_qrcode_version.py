import sys

from qr_code_table import qr_code_table

def get_qr_code_version(lungime_sir, correction_level):
    for version in range (1, 41):
        information = qr_code_table[version][correction_level]
        total_ec_codewords = information['ec_codewords_per_block'] * (information['blocks_in_group1'] + information['blocks_in_group2'])
        total_symbols = information['total_data_codewords']

        print (version)
        print (total_ec_codewords, total_symbols)
        if total_symbols >= lungime_sir:
            return version
