#ticketing_admin.py
import tkinter as tk
from tkinter import messagebox
from random import randrange
from collections.abc import MutableMapping

class Empty(Exception):
    pass

class PriorityQueueBase:
    """Abstract base class for a priority queue."""
    
    class _Item:
        """Lightweight composite to store priority queue items."""
        __slots__='_key', '_value'
        
        def __init__(self, k, v):
            self._key=k
            self._value=v
            
        def __lt__(self, other):
            return self._key < other._key   # compare items based on their keys
        
    def is_empty(self):                 # concrete method assuming abstract len
        """Return True if the priority queue is empty."""
        return len(self)==0
        
class HeapPriorityQueue(PriorityQueueBase): # base class defines _Item
    """ A min-oriented priority queue implemented with a binary heap."""
    #---------------------------nonpublic behaviors-----------------------
    def _parent(self, j):
        return (j-1) //2
    
    def _left(self, j):
        return 2*j + 1
    
    def _right(self, j):
        return 2*j +2
    
    def _has_left(self, j):
        return self._left(j) < len(self._data)      # index beyond end of list?
    
    def _has_right(self, j):
        return self._right(j) < len(self._data)     # indes beyond end of list?
    
    def _swap(self, i, j):
        """Swap the elements at indices i and j of array."""
        self._data[i], self._data[j] = self._data[j], self._data[i]
        
    def _upheap(self, j):
        parent = self._parent(j)
        if j > 0 and self._data[j] < self._data[parent]:
            self._swap(j, parent)
            self._upheap(parent)                     # recur at position of parent
            
    def _downheap(self, j):
        if self._has_left(j):
            left = self._left(j)
            small_child = left                      # although right may be smaller
            if self._has_right(j):
                right = self._right(j)
                if self._data[right] < self._data[left]:
                    small_child = right
            if self._data[small_child] < self._data[j]:
                self._swap(j, small_child)
                self._downheap(small_child)         # recur at position of small child
                
    #---------------------------public behaviors-----------------------
    def __init__(self):
        """Create a new empty Priority Queue."""
        self._data=[]
        
    def __len__(self):
        """Return the number of items in the priority queue."""
        return len(self._data)
    
    def add(self, key, value):
        self._data.append(self._Item(key, value))
        self._upheap(len(self._data) - 1)           # upheap newly added position
        
    def min(self):
        """Return but do not remove (k,v) tuple with minimum key.
        
        Raise Empty exception if empty.
        """
        if self.is_empty():
            raise Empty("Priority queue is empty.")
        item = self._data[0]
        return (item._key, item._value)
    
    def remove_min(self):
        """Remove and return (k,v) tuple with minimum key.
        
        Raise Empty exception if empty."""
        if self.is_empty():
            raise Empty("Priority queue is empty.")
        self._swap(0, len(self._data) - 1)      # put minimum item at the end
        item = self._data.pop()                 # and remove it from the list;
        self._downheap(0)                       # then fix new root
        return (item._key, item._value)
    
    def __iter__(self):
        """Generate an iteration of all elements in the heap."""
        for item in self._data:
            yield (item._key, item._value)
    
    
    

class MapBase(MutableMapping):
    
    class _Item:
        """Lightweight composite to store key-value pairs."""
        __slots__ = '_key', '_value'
        
        def __init__(self, k, v):
            self._key = k
            self._value = v
        
        def __eq__(self, other):
            return self._key == other._key  # compare items based on their keys
        
        def __ne__(self, other):
            return not (self == other)      # opposite of __eq__
        
        def __lt__(self, other):
            return self._key < other._key   # compare items based on their keys

class UnsortedTableMap(MapBase):
    
    def __init__(self):  
        self._table = []
        
    def __getitem__(self, k):
        for item in self._table:
            if k == item._key:
                return item._value
        raise KeyError('Key Error: ' + repr(k))
    
    def __setitem__(self, k, v):
        for item in self._table:
            if k == item._key:
                item._value = v
                return
        self._table.append(self._Item(k,v))
    
    def __delitem__(self, k):
        for j in range(len(self._table)):
            if k == self._table[j]._key:
                self._table.pop(j)
                return
        raise KeyError('Key Error: ' + repr(k))
    
    def __len__(self):
        return len(self._table)
    
    def __iter__(self):
        for item in self._table:
            yield item._key
            
class HashMapBase(MapBase):
    """Abstract base class for map using hash-table with MAD compression. """
        
    def __init__(self, cap=11, p=109345121):
        """Create an empty hash-table map."""
        self._table = cap * [None]
        self._n = 0                             # number of entries in the map
        self._prime = p                         # prime for MAD compression
        self._scale = 1 + randrange(p-1)        # scale from 1 to p-1 for MAD
        self._shift = randrange(p)              # shift from 0 to p-1 for MAD
    
    def _hash_function(self, k):
        return (hash(k)*self._scale + self._shift) % self._prime % len(self._table)
    
    def __len__(self):
        return self._n
    
    def __getitem__(self, k):
        j = self._hash_function(k)
        return self._bucket_getitem(j, k)            # may raise KeyError
    
    def __setitem__(self, k, v):
        j = self._hash_function(k)
        self._bucket_setitem(j, k, v)                # subroutine maintains self._n
        if self._n > len(self._table) // 2:          # keep load factor <= 0.5
            self._resize(2 * len(self._table) - 1)   # number 2^x - 1 is often prime
            
    def __delitem__(self, k):
        j = self._hash_function(k)
        self._bucket_delitem(j, k)                   # may raise KeyError
        self._n -= 1
        
    def _resize(self, c):
        old = list(self.items())
        self._table = c * [None]
        self._n = 0
        for (k,v) in old:
            self[k] = v
                        
class ChainHashMap(HashMapBase):
    """Hash map implemented with separate chaining for collision resolution"""
    
    def _bucket_getitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError("Key Error: " + repr(k))
        return bucket[k]
    
    def _bucket_setitem(self, j, k, v):
        if self._table[j] is None:
            self._table[j] = UnsortedTableMap()
        oldsize = len(self._table[j])
        self._table[j][k] = v
        if len(self._table[j]) > oldsize:
            self._n += 1
            
    def _bucket_delitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError('Key Error: ' + repr(k))
        del bucket[k]
        
    def __iter__(self):
        for bucket in self._table:
            if bucket is not None:
                for key in bucket:
                    yield key
                    
class ConcertReservationSystem:
    def __init__(self):
        self.tickets_map = ChainHashMap()  # Map to store ticket ownership information
        self.concert_dates = ChainHashMap()  # Store dates per user
        
    def add_ticket(self, user_id, concert_date):  # Changed method name from reserve_ticket to add_ticket
        if user_id not in self.tickets_map:
            self.tickets_map[user_id] = HeapPriorityQueue()
        self.tickets_map[user_id].add(concert_date, user_id)  # Store ticket reservation
        self.concert_dates[user_id] = self.tickets_map[user_id]  # Add concert date to priority queue
        
    def has_ticket(self, user_id):
        return user_id in self.tickets_map
        
    def get_sorted_tickets_for_user(self, user_id):
        if user_id in self.tickets_map:
            tickets_heap = self.tickets_map[user_id]
            sorted_tickets = []
            for ticket in tickets_heap:
                sorted_tickets.append(ticket[0])  # Extracting the concert dates
            return sorted_tickets
        else:
            return None
    
    def print_users_with_tickets(self):
        print("Users with reserved tickets:")
        for user_id in self.tickets_map:
            print(user_id)

# Tkinter GUI part
class ConcertReservationSystemGUI:
    def __init__(self, root):
        self.system = ConcertReservationSystem()
        self.root = root
        self.root.title("Reservation Management System")

        # User ID Entry
        self.user_id_label = tk.Label(root, text="User ID:", width=15, height=2)
        self.user_id_label.pack()
        self.user_id_entry = tk.Entry(root,width=20)
        self.user_id_entry.pack()

        # Concert Date Entry
        self.concert_date_label = tk.Label(root, text="Concert Date (YYYY-MM-DD):",width=25, height=2)
        self.concert_date_label.pack()
        self.concert_date_entry = tk.Entry(root, width=20)
        self.concert_date_entry.pack()

        # Reserve Ticket Button
        self.reserve_button = tk.Button(root, text="Add Ticket", command=self.add_ticket,width=20,height=2)  # Changed command to add_ticket
        self.reserve_button.pack()

        # Show Tickets Button
        self.show_tickets_button = tk.Button(root, text="Show Tickets", command=self.show_tickets,width=20,height=2)
        self.show_tickets_button.pack()

        # Show Users with Tickets Button
        self.show_users_button = tk.Button(root, text="Show Users with Tickets", command=self.show_users_with_tickets,width=30,height=2)
        self.show_users_button.pack()

    def add_ticket(self):  # Changed method name from reserve_ticket to add_ticket
        user_id = self.user_id_entry.get()
        concert_date = self.concert_date_entry.get()

        if user_id and concert_date:
            self.system.add_ticket(user_id, concert_date)  # Changed method name from reserve_ticket to add_ticket
            messagebox.showinfo("Success", f"Ticket added for {user_id} on {concert_date}")  # Changed message
        else:
            messagebox.showerror("Error", "Please enter both User ID and Concert Date")

    def show_tickets(self):
        user_id = self.user_id_entry.get()
        if user_id:
            sorted_tickets = self.system.get_sorted_tickets_for_user(user_id)
            if sorted_tickets:
                ticket_list = "\n".join(sorted_tickets)
                messagebox.showinfo("Tickets", f"User {user_id} has tickets on the following dates:\n{ticket_list}")
            else:
                messagebox.showinfo("Tickets", f"User {user_id} has no reserved tickets.")
        else:
            messagebox.showerror("Error", "Please enter a User ID")

    def show_users_with_tickets(self):
        users = list(self.system.tickets_map.keys())
        if users:
            user_list = "\n".join(users)
            messagebox.showinfo("Users with Tickets", f"Users with reserved tickets:\n{user_list}")
        else:
            messagebox.showinfo("Users with Tickets", "No users with reserved tickets.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = ConcertReservationSystemGUI(root)
    root.mainloop()