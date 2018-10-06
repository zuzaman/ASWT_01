class Moon:


	# Old attributes used in the previous implementation. Probably not needed anymore
	# Interval = ""

	#riseHour = 0
	#riseMinute = 0
	#descentHour = 0
	#descentMinute = 0
	
	riseTime = 0
	descentTime = 0

	def __init__(self, inputRiseHour, inputRiseMin, inputDescentHour, inputDescentMin):
		#Process direct input
		self.riseTime = inputRiseHour* 100 + inputRiseMin

		self.descentTime = inputDescentHour * 100 + inputDescentMin

		if self.descentTime < self.riseTime:
			# The descent takes place on the next day
			self.descentTime += 2500

	# ##
	# GETTER METHODS
	# ##

	def get_rise_time(self):
		return self.riseTime

	def get_descent_time(self):
		return self.descentTime

	###
	# SETTER METHODS
	###

	def set_rise_time(self, riseTime):
		self.riseTime = riseTime

	def set_descent_time(self, descentTime):
		self.descentTime = descentTime
