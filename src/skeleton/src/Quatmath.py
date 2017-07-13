import math
class addition:
	def __init__(self):
		pass
	def add(self,q1, q2):
		w1, x1, y1, z1 = q1
		w2, x2, y2, z2 = q2
		w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
		x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
		y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
		z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
		return w, x, y, z
add = addition()
class subtract:
	def __init__(self):
		pass
	def inverse(self,q):
		mag = math.sqrt(q[0]**2+q[1]**2+q[2]**2+q[3]**2)			
		return [q[0]/mag,-q[1]/mag,-q[2]/mag,-q[3]/mag]
	def sub(self,q1,q2):
		#print(self.inverse(q1))
		#print(self.q_mult(q2,self.inverse(q1)))
		return self.q_mult(self.inverse(q2),q1)
	def rotate(self,q1,q2):
		q=self.sub(q1,q2)
                self.q_mult(q1,q)
	def q_mult(self,q1, q2):
		w1, x1, y1, z1 = q1
		w2, x2, y2, z2 = q2
		w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
		x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
		y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
		z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
		return w, x, y, z
sub = subtract()
