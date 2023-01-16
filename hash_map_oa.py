# Description: Hash Map implementation using chaining for collision resolution.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        DynamicArray if the load factor is equal or greater than .5. Utilizes quadratic probing to find the next empty
        or tombstone value if a bucket is filled.
        """
        # check load, resize
        if self.table_load() >= .5:
            self.resize_table(self._capacity * 2)

        # check if key exists first
        hash = self._hash_function(key)
        index = hash % self._capacity
        c_index = index
        set = False
        j = 1
        # key exists
        if self.contains_key(key):
            while not set:
                if self._buckets[c_index].key == key:
                    self._buckets[c_index].value = value
                    set = True
                else:
                    c_index = (index + (j ** 2)) % self._capacity
                    j += 1
        else:
            while not set:
                if self._buckets[c_index] is None or self._buckets[c_index].is_tombstone:
                    self._buckets[c_index] = HashEntry(key, value)
                    self._size += 1
                    set = True
                else:
                    c_index = (index + (j ** 2)) % self._capacity
                    j += 1

    def table_load(self) -> float:
        """
        Returns the current load factor of the hash table
        """
        # check on this later
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash. Tombstones are counted.
        """
        # this could just be capacity - size
        empty = 0
        for index in range(self._capacity):
            if self._buckets[index] is not None:
                if self._buckets[index].is_tombstone:
                    empty += 1
            elif self._buckets[index] is None:
                empty += 1

        return empty

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the hash table. Rehashes all entries. Will attempt to resize
        to the next prime number capacity that keeps load factor under .5. Commented out code illustrates
        the danger of creating the same class within a class method.
        """
        if new_capacity < self._size:
            return
        else:
            p_capacity = new_capacity
            if not self._is_prime(p_capacity):
                p_capacity = self._next_prime(p_capacity)
            #while self.table_load() > .5:
                #p_capacity *= 2
                #p_capacity = self._next_prime(p_capacity)

            buckets = self._buckets
            self._buckets = DynamicArray()
            self._capacity = p_capacity
            self._size = 0

            for _ in range(p_capacity):
                self._buckets.append(None)
            for i in range(buckets.length()):
                if buckets[i] is not None and not buckets[i].is_tombstone:
                    self.put(buckets[i].key, buckets[i].value)

            #new_map = HashMap(p_capacity, self._hash_function)
            #for i in range(self._capacity):
                #if self._buckets[i] is not None and not self._buckets[i].is_tombstone:
                    #new_map.put(self._buckets[i].key, self._buckets[i].value)
            #self._buckets = new_map._buckets
            #self._capacity = p_capacity
            #self._size = new_map._size

    def get(self, key: str) -> object:
        """
        Returns value associated with the key.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        c_index = index
        j = 1
        while self._buckets[c_index] is not None:
            if self._buckets[c_index].key == key and not self._buckets[c_index].is_tombstone:
                return self._buckets[c_index].value
            else:
                c_index = (index + (j ** 2)) % self._capacity
                j += 1

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns a boolean indicating if the given key exists in the hash map.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        c_index = index
        j = 1
        while self._buckets[c_index] is not None:
            if self._buckets[c_index].key == key and not self._buckets[c_index].is_tombstone:
                return True
            else:
                c_index = (index + (j ** 2)) % self._capacity
                j += 1

        return False

    def remove(self, key: str) -> None:
        """
        Removes the entry with the matching key from the table.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        c_index = index
        j = 1
        while self._buckets[c_index] is not None:
            if self._buckets[c_index].key == key:
                if not self._buckets[c_index].is_tombstone:
                    self._buckets[c_index].is_tombstone = True
                    self._size -= 1
                return
            else:
                c_index = (index + (j ** 2)) % self._capacity
                j += 1

        return

    def clear(self) -> None:
        """
        Clears the contents of the hash map. Does not change capacity.
        """
        for _ in range(self._capacity):
            self._buckets[_] = None
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array filled with tuples of the key value pairs in the hash table.
        """
        out_arr = DynamicArray()
        for i in range(self._capacity):
            if self._buckets[i] is not None and not self._buckets[i].is_tombstone:
                out_arr.append((self._buckets[i].key, self._buckets[i].value))

        return out_arr

    def __iter__(self):
        """
        Enables iteration across the hash map, creating a variable for progress.
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Returns the next valid item in the hash map, based off its location.
        """
        try:
            value = self._buckets[self._index]
            while value is None or value.is_tombstone:
                self._index += 1
                value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value