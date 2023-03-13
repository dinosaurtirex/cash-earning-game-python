import os
import time 
import msvcrt
import threading 
import random as r


user_coords = [5, 5]

game_size_y = 8
game_size_x = 32

user_score = 0

exit_app = False 

entities = [] 


class Keyboard:

    def getchar_windows(self) -> str:
        return msvcrt.getch().decode()


class Coordinate:

    def __init__(self, x: int, y: int):
        self.x = int(x)
        self.y = int(y)

    def get_coords(self) -> list[int, int]:
        return [self.x, self.y]
    

class Renderer:

    def __init__(self, size_x: int, size_y: int):
        self.size_x = size_x
        self.size_y = size_y

    def update_frame(self, objects_coords: list[Coordinate]):
        print(f"CASH EARNED: {user_score}")
        for y in range(self.size_y):
            for x in range(self.size_x):
                if [x, y] in objects_coords:
                    print("#", end="")
                    continue 
                elif [x, y] in entities:
                    print("$", end="")
                    continue 
                print(".", end="")
            print()


class GameService(Renderer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_global_coordinates(self, index: int, value_to_update: int) -> None:
        global user_coords

        user_coords[index] = value_to_update

    def update_object_coords(self, f_index: int, s_index: int, value_to_update: int, object_coords: list[Coordinate]) -> list[Coordinate]:
        object_coords[f_index][s_index] = value_to_update
        return object_coords
    
    def border_limits_check(self, x, y, i, objects_coords: list[Coordinate]) -> list[Coordinate]:
        if x >= game_size_x:
            update_value = objects_coords[i][0] - 1
            self.update_global_coordinates(0, update_value)
            objects_coords = self.update_object_coords(i, 0, update_value, objects_coords)
        if x < 0:
            update_value = 0
            self.update_global_coordinates(0, update_value)
            objects_coords = self.update_object_coords(i, 0, update_value, objects_coords)
        if y >= game_size_y:
            update_value = objects_coords[i][1] - 1
            self.update_global_coordinates(1, update_value)
            objects_coords = self.update_object_coords(i, 1, update_value, objects_coords)
        if y < 0:
            update_value = 0
            self.update_global_coordinates(1, update_value)
            objects_coords = self.update_object_coords(i, 1, update_value, objects_coords)
        return objects_coords
    
    def generate_new_entities(self) -> None:
        for _ in range(5):
            x = r.randint(0, game_size_x)
            y = r.randint(0, game_size_y)
            entities.append([x, y])
    
    def entity_intersection_check(self, x, y, i, objects_coords: list[Coordinate]) -> list[Coordinate]:
        global user_score
        
        if len(entities) == 0:
            self.generate_new_entities()

        if [x, y] in entities:
            entities.remove([x, y])
            user_score += 1
        return objects_coords

    def update_game_frame(self, objects_coords: list[Coordinate]):
        global user_coords

        if exit_app == True:
            exit(0)
        for i, coord in enumerate(objects_coords):
            updated_coords = self.border_limits_check(coord[0], coord[1], i, objects_coords)
            updated_coords = self.entity_intersection_check(coord[0], coord[1], i, updated_coords)
        self.update_frame(updated_coords)


def renderer():
    global user_coords 
    global entities
    while True:
        coords = Coordinate(
            user_coords[0],
            user_coords[1]
        )
        r = GameService(game_size_x, game_size_y)
        r.update_game_frame([coords.get_coords()])
        time.sleep(0.1)
        os.system("cls")


def key_input():
    global exit_app 

    while True:
        key = Keyboard().getchar_windows()
        if key == "d":
            final_coord = user_coords[0] + 1
            user_coords[0] = final_coord
        if key == "a":
            final_coord = user_coords[0]  - 1
            user_coords[0] = final_coord
        if key == "s":
            final_coord = user_coords[1]  + 1
            user_coords[1] = final_coord
        if key == "w":
            final_coord = user_coords[1]  - 1
            user_coords[1] = final_coord
        if key == "q":
            exit_app = True 
            exit(0)



def main():
    threads = [
        threading.Thread(target=key_input),
        threading.Thread(target=renderer)
    ]
    for th in threads:
        th.start()


if __name__ == '__main__':
    main()