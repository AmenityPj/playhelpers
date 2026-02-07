import hashlib

import binascii
from Crypto.Cipher import AES
from itertools import cycle

from play_helpers.ph_defaults import PhDefaults
from play_helpers.ph_util import PhUtil


class PhCrypto:

    @classmethod
    def hash_algos_list(cls):
        return list(sorted(hashlib.algorithms_available))

    @classmethod
    def hash_str(cls, msg, hash_algo='sha256', hex_digest=True,
                 encoding=PhDefaults.CHAR_ENCODING, encoding_errors=PhDefaults.CHAR_ENCODING_ERRORS):
        """
        :param msg:
        :param hash_algo: check hash_algos_list()

        'md5-sha1', 'sha3_224', 'sha3_256', 'shake_128', 'sm3', 'sha512', 'sha3_384', 'sha256', 'sha384',
        'whirlpool', 'sha3_512', 'mdc2', 'sha1', 'md4', 'sha512_256', 'ripemd160', 'blake2s', 'blake2b',
        'sha512_224', 'md5', 'shake_256', 'sha224'
        :param hex_digest:
        :param encoding:
        :param encoding_errors:

        :return:
        """
        hash_obj = hashlib.new(hash_algo)
        hash_obj.update(msg.encode(encoding=encoding, errors=encoding_errors))
        return hash_obj.hexdigest() if hex_digest else hash_obj.digest()

    @classmethod
    def hash_str_sha256(cls, msg, hex_digest=True, encoding=PhDefaults.CHAR_ENCODING,
                        encoding_errors=PhDefaults.CHAR_ENCODING_ERRORS):
        """

        :param msg:
        :param hex_digest:
        :param encoding:
        :param encoding_errors:

        :return:
        """
        sha256 = hashlib.sha256()
        sha256.update(msg.encode(encoding=encoding, errors=encoding_errors))
        return sha256.hexdigest() if hex_digest else sha256.digest()

    @classmethod
    def hash_file(cls, file_obj, hex_digest=True):
        """

        :param hex_digest:
        :param msg:
        :return:
        """
        # A arbitrary (but fixed) buffer size (change accordingly)
        # 65536 = 65536 bytes = 64 kilobytes
        BUF_SIZE = 65536
        # Initializing the sha256() method
        sha256 = hashlib.sha256()

        # Opening the file provided as the first commandline argument
        with open(file_obj, 'rb') as f:
            while True:
                # reading data = BUF_SIZE from the file and saving it in a variable
                data = f.read(BUF_SIZE)
                # True if eof = 1
                if not data:
                    break
                # Passing that data to that sh256 hash function (updating the function with that data)
                sha256.update(data)
        # sha256.hexdigest() hashes all the input data passed to the sha256() via sha256.update()
        # Acts as a finalize method, after which all the input data gets hashed hexdigest()
        # hashes the data, and returns the output in hexadecimal format
        return sha256.hexdigest() if hex_digest else sha256.digest()

    @classmethod
    def logical_xor_(cls, hex_str_msg, hex_str_key):
        """
        Logical XOR among two hex String
        :param hex_str_msg: Main Message as Hex Str
        :param hex_str_key: Key as Hex Str
        :return: output as hex String
        """
        # Convert to Binary
        bin_str_msg = bytearray.fromhex(hex_str_msg)
        bin_str_key = bytearray.fromhex(hex_str_key)
        data = bytearray()
        # Cycle of key is needed for scenario when len(data) > len(key)
        for c, k in zip(bin_str_msg, cycle(bin_str_key)):
            data.append(c ^ k)
        data = data.hex().upper()
        # print('data' + data)
        return data

    @classmethod
    def logical_xor(cls, str1_hex, str2_hex):
        """

        :param str1_hex:
        :param str2_hex:
        :return:
        """
        if len(str1_hex) != len(str2_hex):
            return False
        data = bytearray(
            [x ^ y for x, y in zip(bytearray.fromhex(str1_hex), bytearray.fromhex(str2_hex))]).hex().upper()
        return data

    @classmethod
    def aes_encrypt(cls, hex_strkey, hex_str_buff, algo=AES.MODE_CBC, hex_str_iv='00000000000000000000000000000000'):
        """
        AES Encryption
        :param hex_strkey: Key as Hex Str
        :param hex_str_buff: Main Message as Hex Str to be encrypted
        :param algo: algo to be used
        :param hex_str_iv: iv value as Hex Str
        :return: output as hex String
        """
        encryptor = AES.new(binascii.unhexlify(hex_strkey), algo, binascii.unhexlify(hex_str_iv))
        data = encryptor.encrypt(binascii.unhexlify(hex_str_buff))
        data = data.hex().upper()
        # print('data' + data)
        return data

    @classmethod
    def generate_opc(cls, hex_str_ki, hex_str_op):
        """
        Generate Opc using Ki and Op
        :param hex_str_ki: Ki as hex String
        :param hex_str_op: OP as hex String
        :return: hexStrOpc: OPC as hex String
        """
        hex_str_opc = cls.aes_encrypt(hex_str_ki, hex_str_op)
        return cls.logical_xor_(hex_str_opc, hex_str_op)

    @classmethod
    def gen_opc(cls, ki_hex, op_hex):
        """

        :param ki_hex:
        :param op_hex:
        :return:
        """
        iv = '00000000000000000000000000000000'
        opc_hex = binascii.hexlify(AES.new(binascii.unhexlify(ki_hex), AES.MODE_CBC, IV=binascii.unhexlify(iv)).encrypt(
            binascii.unhexlify(op_hex))).decode()
        # print(opc_hex)
        return cls.logical_xor(opc_hex, op_hex)

    @classmethod
    def sum_to_single_digit(cls, num):
        return int(num) if (num < 10) else int(cls.sum_to_single_digit(num / 10) + num % 10)

    @classmethod
    def get_odd_even_digits(cls, msg, sum_to_single_digit=True):
        digits = list(msg)
        odd_digits_rev = [*map(int, digits[-2::-2])]
        even_digits_rev = [
            *map(lambda x: cls.sum_to_single_digit(int(x) * 2), digits[-1::-2])] if sum_to_single_digit else [
            *map(int, digits[-1::-2])]
        return odd_digits_rev, even_digits_rev

    @classmethod
    def get_luhn_digit(cls, msg):
        """
	    TODO: Function needs to be thoroughly tested

        :param msg:
        :return:
        """
        try:
            odd_digits_rev, even_digits_rev = cls.get_odd_even_digits(msg, sum_to_single_digit=True)
            x = sum(odd_digits_rev) + sum(even_digits_rev)
            x = (10 - x % 10)
            return 0 if x == 10 else x
        except ValueError:
            return None
        except IndexError:
            return None

    @classmethod
    def validate_luhn_digit(cls, msg):
        """
        TODO:Check if iccid last digit is with or without Luhn Check sum digit
        :param msg:
        :return:
        """
        msg = PhUtil.trim_and_kill_all_white_spaces(msg)
        check_sum_length = 1
        if not msg:
            return False
        if not PhUtil.is_numeric(msg):
            return False
        last_digit = int(msg[-check_sum_length:])
        luhn = cls.get_luhn_digit(msg[:-check_sum_length])
        return luhn == last_digit

    @classmethod
    def validate_eid(cls, msg):
        """
        TODO:Check if EID last digit is with or without Luhn Check sum digit
        :param msg:
        :return:
        """
        msg = PhUtil.trim_and_kill_all_white_spaces(msg)
        if not msg:
            return False
        if not PhUtil.is_numeric(msg):
            return False
        msg_int = int(msg)
        reminder = msg_int % 97
        return reminder == 1

    @classmethod
    def append_luhn(cls, str_plain_data, min_len_iccid_wo_luhn=18):
        return cls.append_luhn_if_needed(str_plain_data, len(str_plain_data))

    @classmethod
    def append_luhn_if_needed(cls, str_plain_data, min_len_iccid_wo_luhn=18):
        """
        Consider the case:
            89446172120000011  : 17 Chars, Luhn digit 4
            894461721200000114 : 18 Chars, Luhn digit 6
        :param str_plain_data:
        :param min_len_iccid_wo_luhn:
        :return:
        """
        #
        if (len(str_plain_data) == min_len_iccid_wo_luhn) or (not (cls.validate_luhn_digit(str_plain_data))):
            # luhn has to be added, as length is minimum
            # Lugn Digit is not Present
            str_plain_data = str_plain_data + str(cls.get_luhn_digit(str_plain_data))
        return str_plain_data

    @classmethod
    def remove_luhn_if_present(cls, str_plain_data):
        if cls.validate_luhn_digit(str_plain_data):  # Lugn Digit is Present
            str_plain_data = str_plain_data[0:-1]
        return str_plain_data

    @classmethod
    def compare_two_files(cls, file_1, file_2):
        """

        :param file_1:
        :param file_2:
        :return:
        """
        # TODO: Validate it, using getting generated files?
        # Ref: https://www.geeksforgeeks.org/compare-two-files-using-hashing-in-python/
        # Ref: https://docs.python.org/3/library/hashlib.html#file-hashing
        f1_hash = cls.hash_file(file_1)
        f2_hash = cls.hash_file(file_2)
        # Doing primitive string comparison to check whether the two hashes match or not
        if f1_hash == f2_hash:
            print('Both files are same')
            print(f'Hash: {f1_hash}')

        else:
            print('Files are different!')
            print(f'Hash of 1st File: {f1_hash}')
            print(f'Hash of 2nd File: {f2_hash}')
