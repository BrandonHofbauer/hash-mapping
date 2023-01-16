# Name: Brandon Hofbauer
# OSU Email: hofbaueb@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/2/2022
# Description: Hash Map implementation using chaining for collision resolution.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates key/value pairs in the hash map. Will replace a value if a key already exists,
        otherwise will create a new entry. Automatically resizes and rehashes the underlying
        DynamicArray if the load factor is equal or greater than 1
        """
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        # search buckets for existing key first
        hash = self._hash_function(key)
        index = hash % self._capacity
        if self.get(key) is not None:
            self._buckets[index].contains(key).value = value
        else:
            self._buckets[index].insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash
        """
        empty = 0
        for index in range(self._capacity):
            if self._buckets[index].length() == 0:
                empty += 1

        return empty

    def table_load(self) -> float:
        """
        Returns the current load factor of the hash table
        """
        # wait wouldn't this just be size / capacity? test later
        elements = 0
        for i in range(self._capacity):
            if self._buckets[i].length() > 0:
                elements += self._buckets[i].length()

        return elements / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map. Does not change capacity.
        """
        for _ in range(self._capacity):
            self._buckets[_] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the hash table. Rehashes all entries. Will attempt to resize
        to the next prime number capacity that keeps load factor under 1. A future challenge
        would be to rewrite it to use its own put() method.
        """
        if new_capacity < 1:
            return
        else:
            buckets = DynamicArray()
            p_capacity = new_capacity
            if not self._is_prime(p_capacity):
                p_capacity = self._next_prime(p_capacity)
            # when new_capacity makes a high load
            while (self.get_size() / p_capacity) > 1:
                p_capacity *= 2
                p_capacity = self._next_prime(p_capacity)

            size = 0
            for _ in range(p_capacity):
                buckets.append(LinkedList())
            for i in range(self._capacity):
                if self._buckets[i].length() > 0:
                    for node in self._buckets[i]:
                        hash = self._hash_function(node.key)
                        index = hash % p_capacity
                        buckets[index].insert(node.key, node.value)
                        size += 1
            self._buckets = buckets
            self._capacity = p_capacity
            self._size = size

    def get(self, key: str):
        """
        Returns value associated with the key.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        if self._buckets[index].contains(key) is not None:
            return self._buckets[index].contains(key).value
        else:
            return None
        # could the if else be simply replaced with return self._buckets[index].contains(key)?

    def contains_key(self, key: str) -> bool:
        """
        Returns a boolean indicating if the given key exists in the hash map.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        if self._buckets[index].contains(key):
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes the entry with the matching key from the table.
        """
        if self.contains_key(key):
            hash = self._hash_function(key)
            index = hash % self._capacity
            self._buckets[index].remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array filled with tuples of the key value pairs in the hash table.
        """
        out_arr = DynamicArray()
        for i in range(self._capacity):
            if self._buckets[i].length() > 0:
                for node in self._buckets[i]:
                    out_arr.append((node.key, node.value))

        return out_arr


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Uses a hashmap to find the mode of a given dynamic array filled with values. The value
    in the array becomes the key in the hash, with its corresponding value being a counter
    for how many times it occurs.
    """
    map = HashMap()
    out_arr = DynamicArray()
    # value in dynamic array becomes key, value becomes a count of that key in array
    # check if it exists first, increment value

    incident = 0
    for index in range(da.length()):
        if map.contains_key(da[index]):
            map.put(da[index], map.get(da[index]) + 1)
        else:
            map.put(da[index], 1)

        # keep track of highest value (int)
        if map.get(da[index]) > incident:
            incident = map.get(da[index])

    look = map.get_keys_and_values()
    for index in range(look.length()):
        if look[index][1] == incident:
            out_arr.append(look[index][0])

    # return a tuple
    return out_arr, incident


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")