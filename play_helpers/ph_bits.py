class PhBits:
    """
    Python integer size is four bytes; 32 Bits
    """
    MIN_BIT_INDEX = 1
    MAX_BIT_INDEX = 32

    def __init__(self, int_value=None, bit_indexes=None):
        if int_value is None:
            self.reset_all_bits()
        else:
            if isinstance(int_value, str):
                int_value = int(int_value)
            if isinstance(int_value, int):
                self.int_value = int_value
            else:
                raise ValueError('Invalid Input Type')
        self.set_bits(bit_indexes)

    def reset_all_bits(self):
        self.int_value = 0

    def set_bits(self, bit_indexes):
        def __set_bit(bit_index):
            self.int_value |= (1 << bit_index)

        if bit_indexes is None:
            return
        if not isinstance(bit_indexes, list):
            bit_indexes = [bit_indexes]
        for bit_index in bit_indexes:
            __set_bit(bit_index)

    def is_bit_set(self, bit_index):
        return bool(self.int_value & (1 << bit_index))

    def find_index_kth_set_bit(self, k):
        cnt, ind = 0, 0
        n = self.int_value
        # Traverse in the binary
        while n > 0:
            # Check if the last bit is set or not
            if n & 1:
                cnt += 1
            # Check if the count is equal to k then return the index
            if cnt == k:
                return ind
            # Increase the index as we move right
            ind += 1
            # Right shift the number by 1
            n = n >> 1
        return None
