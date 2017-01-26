
class Field:
	index = 0
	name = "undefined"
	field_type = "undefined"
	length = 0
	nullable = True
	isPrimaryKey = False
	isForeignKey = False
	isUnique = False
	to_table = "undefined"
	default = None


	def __init__(self, name, field_type, length, nullable, index, default):
		self.name = name
		self.field_type = field_type
		self.length = length
		self.nullable = nullable
		self.index = index
		self.default = default

	def __str__(self):
		return str(self.index) +": "+ self.name +", "+self.field_type+", "+str(self.length) + ", Nullable: "+str(self.nullable) + ", Default: "+str(self.default) + ", isUnique: "+str(self.isUnique) + ", isPrimaryKey: "+ str(self.isPrimaryKey)+", isForeignKey: " + str(self.isForeignKey) + " to " + self.to_table

