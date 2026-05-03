class Plant:
    def __init__(self,name:str,height:int,age:int):
        self.name = name
        self.height = height
        self.age = age
def ft_garden_data() -> None:
    rose = Plant('Rose',25,30)
    sunflower = Plant('Sunflower',80,45)
    cactus = Plant('Cactus',15,120)
    plants = [rose,sunflower,cactus]
    print('=== Garden Plant Registry ===')
    for i in range(0,3):
        print(f'{plants[i].name}: {plants[i].height}cm, {plants[i].age} days old')
if __name__ == "__main__":
    ft_garden_data()
