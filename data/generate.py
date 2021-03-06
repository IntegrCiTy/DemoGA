import json

param = {
    "t_set": 273.15 + 22,           # [K]
    "t_lake": 273.15 + 12,          # [K]
    "t_heat": 273.15 + 60,          # [K]
    "t_heat_ret": 273.15 + 30,      # [K]
    "t_cool": 273.15 + 2,           # [K]
    "t_cool_ret": 273.15 + 12,      # [K]
    "mflow_heat": 8,                # [kg/s]
    "mflow_heat_src": 8,            # [kg/s]
    "mflow_cool": 4,                # [kg/s]
    "mflow_cool_src": 4,            # [kg/s]
    "mflow_lake": 4,                # [kg/s]
    "mflow_lake_src": 10,           # [kg/s]
    "p_heating": 75000,				# [W]
    "p_cooling": 10000				# [W]
}

with open('par.json', 'w') as outfile:
    json.dump(param, outfile)

step = 60
nbr_step = 60*24

data = {"schedule":
            [["HeatPumpCooling", "HeatPumpHeating", "HeatPumpCentral"],
             ["ThermalNetwork", "PowerNetwork"],
             ["ConsumerHeating", "ConsumerCooling"]],
        "steps": [step] * nbr_step
        }

with open('run.json', 'w') as outfile:
    json.dump(data, outfile)
