from django.db import models

# Create your models here.


class Moon(models.Model):

	moon_id = models.AutoField(primary_key=True)

	dInterval = models.TextField(default='')
	pInterval = models.TextField(default='')

	dRiseHour = models.PositiveIntegerField(default=12)
	dRiseMinute = models.PositiveIntegerField(default=12)
	dDescentHour = models.PositiveIntegerField(default=12)
	dDescentMinute = models.PositiveIntegerField(default=12)
	
	dRiseTime = models.PositiveIntegerField(null = True)
	dDescentTime = models.PositiveIntegerField(null = True)

	pRiseHour = models.PositiveIntegerField(default=12)
	pRiseMinute = models.PositiveIntegerField(default=12)
	pDescentHour = models.PositiveIntegerField(default=12)
	pDescentMinute = models.PositiveIntegerField(default=12)
	
	pRiseTime = models.PositiveIntegerField(null = True)
	pDescentTime = models.PositiveIntegerField(null = True)

	overlap = models.PositiveIntegerField(null = True)

###
#GETTERS
###

	def get_dRiseHour(self):
		return self.dRiseHour

	def get_dRiseMinute(self):
		return self.dRiseMinute

	def get_dDescentHour(self):
		return self.dDescentHour

	def get_dDescendMinute(self):
		return self.dDescentMinute

	def get_pRiseHour(self):
		return self.pRiseHour

	def get_pRiseMinute(self):
		return self.pRiseMinute

	def get_pDescendHour(self):
		return self.pDescentHour

	def get_pDescendMinute(self):
		return self.pDescentMinute

	def get_overlap(self):
		return self.overlap

###
# SETTERS
###

	def set_dRiseHour(self, riseHour):
		self.dRiseHour = riseHour

	def set_dRiseMinute(self, riseMinute):
		self.dRiseMinute = riseMinute

	def set_dDescentHour(self, descentHour):
		self.dDescentHour = descentHour

	def set_dDescentMinute(self, descentMinute):
		self.dDescentMinute = descentMinute

	def set_pRiseHour(self, riseHour):
		self.pRiseHour = riseHour

	def set_pRiseMinute(self, riseMinute):
		self.pRiseMinute = riseMinute

	def set_pDescentHour(self, descentHour):
		self.pDescentHour = descentHour

	def set_pDescentMinute(self, descentMinute):
		self.pDescentMinute = descentMinute

	def set_overlap(self, overlap):
		self.overlap = overlap
###
# Methods
###


	def process_periods(self):

		(dIntervalRise,dIntervalDescent) = self.dInterval.strip().strip('()').strip('[]').split(',')
		(pIntervalRise,pIntervalDescent) = self.pInterval.strip().strip('()').strip('[]').split(',')

		(dHourRise, dMinuteRise) = dIntervalRise.split(':')

		self.set_dRiseHour(int(dHourRise))
		self.set_dRiseMinute(int(dMinuteRise))

		(dHourDescent, dMinuteDescent) = dIntervalDescent.split(':')

		self.set_dDescentHour(int(dHourDescent))
		self.set_dDescentMinute(int(dMinuteDescent))

		(pHourRise, pMinuteRise) = pIntervalRise.split(':')

		self.set_pRiseHour(int(pHourRise))
		self.set_pRiseMinute(int(pMinuteRise))

		(pHourDescent, pMinuteDescent) = pIntervalDescent.split(':')

		self.set_pDescentHour(int(pHourDescent))
		self.set_pDescentMinute(int(pMinuteDescent))


	def generalise_time(self):
		# For Deimos

		self.dRiseTime = self.dRiseHour * 100 + self.dRiseMinute

		self.dDescentTime = self.dDescentHour * 100 + self.dDescentMinute

		if self.dDescentTime < self.dRiseTime:
			# The descent takes place on the nextday
			self.dDescentTime += 2500

		# For Phobos
		self.pRiseTime = self.pRiseHour * 100 + self.pRiseMinute
		self.pDescentTime = self.pDescentHour * 100 + self.pDescentMinute

		if self.pDescentTime < self.pRiseTime:
			# The descent takes place on the nextday
			self.pDescentTime += 2500

	def calculate_overlap(self):

	# Deimos rises before Phobos

		if self.dRiseTime < self.pRiseTime:

			# Case 1
			# Demios descends before Phobos raises

			if self.dDescentTime < self.pRiseTime:
				self.set_overlap(0)

			# Case 2

			elif self.dDescentTime <= self.pDescentTime:
				self.set_overlap((self.dDescentTime - self.pRiseTime))

			# Case 3

			elif self.pDescentTime <= self.dDescentTime:
				self.set_overlap((self.pDescentTime - self.pRiseTime))

			# Exc. 1
			elif self.dDescentTime == self.pRiseTime:
				self.set_overlap(1)
	
		# Phobos rises before Deimos
		if self.pRiseTime < self.dRiseTime:

			# Case 4
			if self.pDescentTime < self.dRiseTime:
				self.set_overlap(0)
		
			# Case 5
			elif self.pDescentTime <= self.dDescentTime:
				self.set_overlap((self.pDescentTime - self.dRiseTime))
		
			# Case 6
			elif self.dDescentTime <= self.pDescentTime:
				self.set_overlap((self.dDescentTime - self.dRiseTime))

			# Exc. 2
			elif self.pDescentTime == self.dRiseTime:
				self.set_overlap(1)

		# If they rise at the same time
		if self.pRiseTime == self.dRiseTime:

			# If Deimos descends earlier

			if self.dDescentTime < self.pDescentTime:
				self.set_overlap((self.dDescentTime - self.dRiseTime))


			# If Phobos descends earlier or at the same time

			if self.pRiseTime <= self.dRiseTime:
				self.set_overlap((self.pDescentTime - self.pRiseTime))

		return self.overlap