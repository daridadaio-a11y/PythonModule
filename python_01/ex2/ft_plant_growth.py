class Plant:
    def __init__(self,name:str,height:int,age:int):
        self.name = name
        self.height = height
        self.age = age
    def grow_height(self):
        self.height += 1
    def grow_age(self):
        self.age += 1
    def get_info(self):
        print(f'{self.name}: {self.height}cm, {self.age} days old')

def ft_plant_growth() -> None:
    rose = Plant('Rose',25,30)
    start_age = rose.age
    print('=== Day 1 ===')
    rose.get_info()
    print('=== Day 7 ===')
    for i in range(0,6):
        rose.grow_age()
        rose.grow_height()
    rose.get_info()
    print(f'Growth this week: +{rose.age - start_age}cm')

if __name__ == "__main__":
    ft_plant_growth()
