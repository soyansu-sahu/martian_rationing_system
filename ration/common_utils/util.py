class ScheduleInventory:
    max_index = 0
    curr = {}
    best = {}
    target = 0

    def __init__(self, inventory, daily_calories_target=2500, daily_water_target=2):
        self.inventory = inventory
        self.daily_calories_target = daily_calories_target
        self.daily_water_target = daily_water_target

    def solve(self, array, custom_target):
        self.max_index = len(array)
        self.target = custom_target
        self.best = {"sum": float("INF"), "terms": []}
        self.curr = {"sum": 0, "terms": []}
        self.dfs(0, array)
        return self.best["terms"]

    def dfs(self, start, array):
        in_progress = start < self.max_index
        if in_progress:
            for i in range(start, self.max_index):
                self.curr["sum"] = self.curr["sum"] + array[i]
                self.curr["terms"].append(i)
                if self.curr["sum"] < self.target:
                    in_progress = self.dfs(i + 1, array)

                elif self.curr["sum"] < self.best["sum"]:
                    self.best["sum"] = self.curr["sum"]
                    self.best["terms"] = self.curr["terms"][0:]

                self.curr["sum"] = self.curr["sum"] - array[i]
                del self.curr["terms"][-1]

        return in_progress

    def getSchedule(self):
        food = []
        water = []

        for item in self.inventory:
            if item["packet_type"] == "FOOD":
                food.append(item)
            else:
                water.append(item)

        schedule = []
        food.sort(key=lambda x: x["expiry_days"])
        water.sort(key=lambda x: x["water_quantity_litres"], reverse=True)
        day = 1
        response = []
        while True:

            if len(food) == 0 or len(water) == 0:
                break

            daily_items = {}

            calories_exipring_today = 0
            food_packet_expiring_list = []
            i = 0
            while i < len(food) and food[i]["expiry_days"] == 1:
                calories_exipring_today = calories_exipring_today + food[i]["calories"]
                if calories_exipring_today <= self.daily_calories_target:
                    food_packet_expiring_list.append(food[i])
                i = i + 1

            food = food[i:]

            optimum_water_packets = self.solve(
                [i["water_quantity_litres"] for i in water], self.daily_water_target
            )

            if len(optimum_water_packets) == 0:
                break

            optimum_food_packets = []
            if calories_exipring_today > self.daily_calories_target:
                daily_items["FOOD"] = food_packet_expiring_list

            else:
                optimum_food_packets = self.solve(
                    [i["calories"] for i in food],
                    self.daily_calories_target - calories_exipring_today,
                )
                if len(optimum_food_packets) == 0:
                    break

                daily_items["FOOD"] = food_packet_expiring_list + [
                    food[i] for i in optimum_food_packets
                ]

            daily_items["WATER"] = [water[i] for i in optimum_water_packets]

            left_food = []
            left_water = []
            for i in range(len(food)):
                if i not in optimum_food_packets:
                    left_food.append(food[i])

            for i in range(len(water)):
                if i not in optimum_water_packets:
                    left_water.append(water[i])

            food = left_food
            water = left_water
            daily_items["DAY"] = day
            response.append(daily_items)
            day = day + 1

        return response


if __name__ == "__main__":

    inventory = [
        {"id": "F1", "packet_type": "FOOD", "calories": 1000, "expiry_days": 1},
        {"id": "F2", "packet_type": "FOOD", "calories": 1200, "expiry_days": 2},
        {"id": "F3", "packet_type": "FOOD", "calories": 800, "expiry_days": 2},
        {"id": "F4", "packet_type": "FOOD", "calories": 1500, "expiry_days": 3},
        {"id": "F5", "packet_type": "FOOD", "calories": 500, "expiry_days": 4},
        {"id": "F6", "packet_type": "FOOD", "calories": 2500, "expiry_days": 4},
        {"id": "F7", "packet_type": "FOOD", "calories": 2500, "expiry_days": 5},
        {"id": "W1", "packet_type": "WATER", "water_quantity_litres": 2},
        {"id": "W2", "packet_type": "WATER", "water_quantity_litres": 1},
        {"id": "W3", "packet_type": "WATER", "water_quantity_litres": 1},
        {"id": "W4", "packet_type": "WATER", "water_quantity_litres": 0.5},
        {"id": "W5", "packet_type": "WATER", "water_quantity_litres": 1.5},
        {"id": "W6", "packet_type": "WATER", "water_quantity_litres": 2},
    ]

    si = ScheduleInventory(inventory=inventory)

    print(si.getSchedule())
