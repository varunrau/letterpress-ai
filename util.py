import heapq
import inspect

class SimpleVector(dict):
	"""
	A vector object. This is a wrapper class for the
	standard python dictionary.
	"""

	def __getitem__(self, index):
		self.setdefault(index, 0)
		return dict.__getitem__(self, index)

	def normalize(self):
		"""
		Standard normalization function.
		@return the vector normalized.
		"""
		total = float(self.totalCount())
		if total == 0: return
		for key in self.keys():
			self[key] = self[key]/total
		return self

	def __mul__(self, other):
		"""
		Multiplying two vectors is defined as the
		dot product.
		@param other - the vector to dot.
		@return the dot product of the two vectors.
		"""
		sum = 0
		if len(self) > len(other):
			self, other = other, self
		for key in self:
			if key not in other:
				continue
			sum += self[key] * other[key]
		return sum

	def totalCount(self):
		"""
		The sum of all the vector components.
		@return the sum
		"""
		return sum(self.values())



class PriorityQueue():
	"""
	A priority queue datastructure. A wrapper
	for the standard python heapqueue object.
	"""

	def __init__(self):
		self.heap = []

	def push(self, item, priority):
		"""
		Pushes an object onto the queue.
		@param item - the item to push.
		@param priority - the priority of the object.
		"""
		entry = (priority, item)
		heapq.heappush(self.heap, entry)

	def pop(self):
		"""
		Pops the object off of the queue.
		@return the highest priority object
		"""
		(_, item) = heapq.heappop(self.heap)
		return item

	def get(self):
		return self.heap[0][1]

	def __len__(self):
		return len(self.heap)

	def isEmpty(self):
		return len(self.heap) == 0

class PriorityQueueWithFunction(PriorityQueue):
	"""
	A PriorityQueue that accepts a function
	"""

	def __init__(self, function):
		"""
		Creates a PriorityQueueWithFunction object.
		@param function - the function used to evaluate the priority of the object.
		"""
		self.fn = function
		PriorityQueue.__init__(self)

	def push(self, *params):
		"""
		Push the object onto the queue.
		@param params - The arguments to the priority function. Note: the
		object to be added to the queue must be index 1 (for whatever reason).
		"""
		PriorityQueue.push(self, params[1], self.fn(params))


def raiseNotDefined():
    print "*** Method not implemented: %s" % inspect.stack()[1][3]
    sys.exit(1)



