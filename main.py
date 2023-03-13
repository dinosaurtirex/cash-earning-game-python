import os
import time 
import msvcrt
import threading 
import random as r


user_coords = [5, 5]
ai_coords = [6, 6]

game_size_y = 10
game_size_x = 32

money_each_row = 32

tick = 0.1

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


class AIService:

    def find_path_to_object(
        self, 
        position_x: int, 
        position_y: int, 
    ) -> list[str]:
        global entities

        positions = []

        if len(entities) > 0:
            for i in entities:
                # Get target coordinates
                try:
                    target_x = i[0]
                    target_y = i[1]
                except Exception as exc:
                    return  
                
                y_go = target_y - position_y
                x_go = target_x - position_x

            positions.append([y_go, x_go])

            best_position = sorted(positions)[0]

            y_go = best_position[0]
            x_go = best_position[1]

            if y_go < 0:
                return ("w")
            if y_go > 0:
                return ("s")
        
            if x_go < 0:
                return "a"
            if x_go > 0:
                return "d"
        

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
        global money_each_row

        for _ in range(money_each_row):
            x = r.randint(0, game_size_x-1)
            y = r.randint(0, game_size_y-1)
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
    global user_coords, ai_coords
    global entities
    global tick 

    while True:
        coords = Coordinate(
            user_coords[0],
            user_coords[1]
        )
        ai_coord = Coordinate(
            ai_coords[0],
            ai_coords[1]
        )
        r = GameService(game_size_x, game_size_y)
        r.update_game_frame([coords.get_coords(), ai_coord.get_coords()])
        time.sleep(tick)
        os.system("cls")


def ai_controller():
    global tick, ai_coords

    while True:
        
        if exit_app == True:
            exit(0)

        # Get player coordinates 
        x, y = ai_coords[0], ai_coords[1]

        # Calculate path to target coordinates

        key = AIService().find_path_to_object(
            x, y
        )

        # Do action 
        
        if key == "d":
            ai_coords[0] = ai_coords[0] + 1
        if key == "a":
            ai_coords[0] = ai_coords[0] - 1
        if key == "s":
            ai_coords[1] = ai_coords[1] + 1
        if key == "w":
            ai_coords[1] = ai_coords[1] - 1

        time.sleep(tick)


def key_input():
    global exit_app, tick 

    while True:
        user_key_input = Keyboard().getchar_windows()

        if user_key_input == "d":
            final_coord = user_coords[0] + 1
            user_coords[0] = final_coord
        if user_key_input == "a":
            final_coord = user_coords[0] - 1
            user_coords[0] = final_coord
        if user_key_input == "s":
            final_coord = user_coords[1] + 1
            user_coords[1] = final_coord
        if user_key_input == "w":
            final_coord = user_coords[1] - 1
            user_coords[1] = final_coord

        if user_key_input == "q":
            exit_app = True 
            exit(0)

        time.sleep(tick)


def main():
    threads = [
        threading.Thread(target=key_input),
        threading.Thread(target=renderer),
        threading.Thread(target=ai_controller)
    ]
    for th in threads:
        th.start()


if __name__ == '__main__':
    main()