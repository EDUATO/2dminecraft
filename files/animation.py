# Animation engine 1.0 : Made by Eduardo Delfante

class Animation:
	def __init__(self):
		self.Animations = {} # {"(animation_name):[value, limit, add_value, [*settings]]"}
		print("Initializing animation engine")

	def new_animation(self, animation_name, initial_value, limit, add_value=1, force_when_reached=False):
		# Create a new animation or overwrite one
		if animation_name in self.Animations:
			print(animation_name + " was overwritten.")
		else:
			print(animation_name + " created.")

		self.Animations[animation_name] = [initial_value, limit, add_value, 
										[force_when_reached, # See if it has to force the animation when the limit has been already reached
										0] # Count how many times the limit was reached
										] 

	def delete_animation(self, animation_name):
		del self.Animations[animation_name]

	def update(self, deltaTime=1, exceptions=[]):

		self.i = 0

		self.keys = list(self.Animations.keys())

		for self.i in range(len(self.Animations)):

			self.Animation_key = self.keys[self.i]

			if not self.Animation_key in exceptions:

				# Initial vars
				self.Value = self.Animations[self.Animation_key][0]

				self.Limit = self.Animations[self.Animation_key][1]

				self.Add_Value = self.Animations[self.Animation_key][2]

				self.Animation_settings = self.Animations[self.Animation_key][3]


				self.add_formula = (self.Add_Value * deltaTime)
				
				if not self.Add_Value == 0:
					if not (self.get_in_settings(self.Animation_key, 1) > 0 and self.get_in_settings(self.Animation_key, 0) == True):
						if (self.Limit - self.Value) > 0: # If the limit minus the value its positive
							# It ADDS the value

							if not (self.Animations[self.Animation_key][0] + self.add_formula) >= self.Limit:
								self.Animations[self.Animation_key][0] += self.add_formula # Add Add_Value to the animation value
							else:
								self.set_value(self.Animation_key, self.Limit)
								self.set_in_settings(self.Animation_key, 1, self.get_in_settings(self.Animation_key, 1) + 1) # Add 1 to the limit counter

						elif (self.Limit - self.Value) < 0:  # If the limit minus the value its negative
							# It SUBSTRACTS the value
							if not (self.Animations[self.Animation_key][0] - self.add_formula) <= self.Limit:
								self.Animations[self.Animation_key][0] -= self.add_formula # Substracts Add_Value to the animation value
							else:
								self.set_value(self.Animation_key, self.Limit)
								self.set_in_settings(self.Animation_key, 1, self.get_in_settings(self.Animation_key, 1) + 1) # Add 1 to the limit counter

					else: # Because the limit has been already reached
						self.set_value(self.Animation_key, self.Limit)
						self.set_in_settings(self.Animation_key, 1, self.get_in_settings(self.Animation_key, 1) + 1) # Add 1 to the limit counter

	# Getters
	def get_value(self, animation_name):
		return self.Animations[animation_name][0] # Get Value

	def get_limit(self, animation_name):
		return self.Animations[animation_name][1] # Get Limit

	def get_valueToAdd(self, animation_name):
		return self.Animations[animation_name][2] # Get Add_value

	def get_in_settings(self, animation_name, index):
		return self.Animations[animation_name][3][index] # Get an specific setting in settings

	def get_Animations(self):
		return self.Animations

	# Setters
	def set_value(self, animation_name, value):
		self.Animations[animation_name][0] = value # Set Value

	def set_limit(self, animation_name, limit, reset_limit_counter=False):
		self.Animations[animation_name][1] = limit # Set Limit
		if reset_limit_counter:
			self.set_in_settings(animation_name, 1, 0) # Reset limit count

	def set_valueToAdd(self, animation_name, value_to_add):
		self.Animations[animation_name][2] = value_to_add # Set Add_value

	def set_in_settings(self, animation_name, index, value):
		self.Animations[animation_name][3][index] = value # Set an specific setting in settings


if __name__ == "__main__":
	Animation_handler = Animation()

	# Creates two new animations
	Animation_handler.new_animation("Cow", 0, 10, 1)

	Animation_handler.new_animation("Ball", 0, -25, 1)

	# Delete an animation
	Animation_handler.delete_animation("Ball")

	# Updates the animations
	for i in range(9):
		Animation_handler.update()

	# Prints the animation
	print(Animation_handler.get_value("Cow"))

	Animation_handler.new_animation("Cow", 0, 10, 1) # If the animation already exsists it overwrites it

	print(Animation_handler.get_value("Cow"))
