class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def make_sound(self):
        return "Some generic sound"
    
    def info(self):
        return f"{self.name} is a {self.species}"


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, species="Dog")
        self.breed = breed
    
    def make_sound(self):
        return "Woof!"
    
    def fetch(self):
        return f"{self.name} is fetching the ball!"


class Cat(Animal):
    def __init__(self, name, indoor=True):
        super().__init__(name, species="Cat")
        self.indoor = indoor
    
    def make_sound(self):
        return "Meow!"
    
    def scratch(self):
        return f"{self.name} is scratching!"


# Create instances
dog = Dog("Buddy", "Golden Retriever")
cat = Cat("Whiskers")

# Use inheritance and polymorphism
print(dog.info())          # Buddy is a Dog
print(cat.info())          # Whiskers is a Cat

# Use overridden methods (polymorphism)
print(dog.make_sound())    # Woof!
print(cat.make_sound())    # Meow!

# Use class-specific methods
print(dog.fetch())         # Buddy is fetching the ball!
print(cat.scratch())       # Whiskers is scratching!

# Create a list of animals and iterate (polymorphism)
animals = [dog, cat]
for animal in animals:
    print(f"{animal.name} says {animal.make_sound()}")