import heapq

class SimpleVector(dict):

	def __getitem__(self, index):
		self.setdefault(index, 0)
		return dict.__getitem__(self, index)

	def normalize(self):
		total = float(self.totalCount())
		if total == 0: return
		for key in self.keys():
			self[key] = self[key]/total
		return self

	def __mul__(self, other):
		sum = 0
		if len(self) > len(other):
			self, other = other, self
		for key in self:
			if key not in other:
				continue
			sum += self[key] * other[key]
		return sum

	def totalCount(self):
		return sum(self.values())



class PriorityQueue():

	def __init__(self):
		self.heap = []

	def push(self, item, priority):
		entry = (priority, item)
		heapq.heappush(self.heap, entry)

	def pop(self):
		(_, item) = heapq.heappop(self.heap)
		return item

	def get(self):
		return self.heap[0][1]

	def __len__(self):
		return len(self.heap)

	def isEmpty(self):
		return len(self.heap) == 0

class PriorityQueueWithFunction(PriorityQueue):

	def __init__(self, function):
		self.fn = function
		PriorityQueue.__init__(self)

	def push(self, *params):
		PriorityQueue.push(self, params[1], self.fn(params))





