#!/usr/bin/env python
"""Update phone numbers using phone_mapping"""

phone_mapping = {
        '(512) 246-7941': '+1-512-246-7941',
        '+1 (512) 469-7000': '+1-512-469-7000',
        '+1 (512) 759-5900': '+1-512-759-5900',
        '+1 512 218 5062': '+1-512-218-5062',
        '+1 512 218 9888': '+1-512-218-9888',
        '+1 512 238 0820': '+1-512-238-0820',
        '+1 512 244 3737': '+1-512-244-3737',
        '+1 512 248 7000': '+1-512-248-7000',
        '+1 512 252 1133': '+1-512-252-1133',
        '+1 512 255 7000': '+1-512-255-7000',
        '+1 512 255 7530': '+1-512-255-7530',
        '+1 512 258 8114': '+1-512-258-8114',
        '+1 512 277 6959': '+1-512-277-6959',
        '+1 512 310 7600': '+1-512-310-7600',
        '+1 512 310 7678': '+1-512-310-7678',
        '+1 512 324 4000': '+1-512-324-4000',
        '+1 512 341 1000': '+1-512-341-1000',
        '+1 512 362 9525': '+1-512-362-9525',
        '+1 512 402 7811': '+1-512-402-7811',
        '+1 512 528 7000': '+1-512-528-7000',
        '+1 512 532 2200': '+1-512-532-2200',
        '+1 512 600 0145': '+1-512-600-0145',
        '+1 512 637 6890': '+1-512-637-6890',
        '+1 512 733 9660': '+1-512-733-9660',
        '+1 512 990 5413': '+1-512-990-5413',
        '+1 512)351 3179': '+1-512-351-3179',
        '+1 512-244-8500': '+1-512-244-8500',
        '+1 512-260-5443': '+1-512-260-5443',
        '+1 512-260-6363': '+1-512-260-6363',
        '+1 512-310-8952': '+1-512-310-8952',
        '+1 512-338-8805': '+1-512-338-8805',
        '+1 512-341-7387': '+1-512-341-7387',
        '+1 512-421-5911': '+1-512-421-5911',
        '+1 512-535-5160': '+1-512-535-5160',
        '+1 512-535-6317': '+1-512-535-6317',
        '+1 512-733-6767': '+1-512-733-6767',
        '+1 512-851-8777': '+1-512-851-8777',
        '+1 737 757 3100': '+1-737-757-3100',
        u'+1-512-251\u20113173': '+1-512-251-3173',
        u'+1-737-484\u20110700': '+1-737-484-0700',
        '+1512-413-9671': '+1-512-413-9671',
        '+1512-909-2528': '+1-512-909-2528',
        '+15123885728': '+1-512-388-5728',
        '+15124282300': '+1-512-428-2300',
        '+15124648382': '+1-512-464-8382',
        '1+512-696-5209': '+1-512-696-5209'
        }

# ************************* update_phone() *************************

def update_phone(phone):
        if phone in phone_mapping.keys():
                return(phone_mapping[phone])
        else:
                return phone
