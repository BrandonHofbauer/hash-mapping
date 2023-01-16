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
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
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
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
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