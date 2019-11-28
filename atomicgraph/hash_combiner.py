# @credits https://github.com/google/guava/blob/master/guava/src/com/google/common/hash/Hashing.java
class HashCombiner:
    def combine_ordered(self, code_array):
        resultBytes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for code in iter(code_array):
            for i in range(0, 16):
                resultBytes[i] = ((resultBytes[i] * 37) % 256) ^ code[i]
        return bytes(resultBytes)
