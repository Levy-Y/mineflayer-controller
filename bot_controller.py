import streamlit as st
from st_on_hover_tabs import on_hover_tabs
import  streamlit_toggle as tog
from streamlit_extras.add_vertical_space import add_vertical_space
from javascript import require, On
import asyncio
import time
import json

# TODO: settings tab save to .json file, healt detection quit, hostile mob near quit, night quit,
# TODO: pathfinder implementation, json datastructure for saving infos, ip, port and bot name in settings,
# TODO: that is saved into the json, if no ip and botname -> disable dashboard, connect bot on add to queue button press

st.set_page_config(
    page_title="Bot controller",
    page_icon="🕹",
    layout="centered",
    initial_sidebar_state="auto",
)

mineflayer = require("mineflayer")
pathfinder = require("mineflayer-pathfinder")
armorManager = require("mineflayer-armor-manager")

RANGE_GOAL = 0

with open('data\data.json', 'r') as f:
    data = json.load(f)

class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def abort_queue():
    print("TODO 1")


def pause_queue():
    print("TODO 2")

botHealth = 20

def makeBot(x, y, z):
    bot = mineflayer.createBot({
        "host": data['server_ip'],
        "port": data['server_port'],
        "username": data['bot_name'],
    })
    
    bot.loadPlugin(pathfinder.pathfinder)
    bot.loadPlugin(armorManager)
    
    if data["quit_on_low_health"] == True:
        @On(bot, "health")
        def health(this):
            global botHealth
            if bot.health >= botHealth:
                botHealth = bot.health
                return
            
            botHealth = bot.health
            if botHealth < data["low_health_threashold"]:
                bot.quit()

    if data['armor_equip'] == True:
        bot.armorManager.equipAll()
            
    global pos
    pos = Vec3(float(x), float(y), float(z))
    bot.loadPlugin(pathfinder.pathfinder)
    mcData = require('minecraft-data')(bot.version)
    movements = pathfinder.Movements(bot, mcData)
    
    bot.pathfinder.setMovements(movements)
    bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, RANGE_GOAL))
    
    @On(bot, "goal_reached")
    def handleGaolReached(_, result):
        if data["drop_items_on_arrival"] == True:
            inventoryItemCount = bot.inventory.items()
            print(inventoryItemCount)
            # if inventoryItemCount == 0:
            #     return
            
            # while inventoryItemCount > 0:
            #     item = bot.inventory.items()[0]
            #     bot.tossStack(item)
            #     inventoryItemCount -= 1
        
        if data["disconnect_on_arrival"] == True:
            bot.quit()
            st.info(f"Arrived at x: {float(x)}, y: {float(y)}, z: {float(z)}, leaving server..")
        else:
            return

def main():
    st.markdown(
        "<style>"
        + open(
            "frontend\styles.css"
        ).read()
        + "</style>",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        tabs = on_hover_tabs(
            tabName=["Settings", "Dashboard"],
            iconName=["dashboard", "economy"],
            styles={
                "navtab": {
                    "background-color": "#111",
                    "color": "#818181",
                    "font-size": "18px",
                    "transition": ".3s",
                    "white-space": "nowrap",
                    "text-transform": "uppercase",
                },
                "tabOptionsStyle": {
                    ":hover :hover": {"color": "red", "cursor": "pointer"}
                },
                "iconStyle": {
                    "position": "fixed",
                    "left": "7.5px",
                    "text-align": "left",
                },
                "tabStyle": {
                    "list-style-type": "none",
                    "margin-bottom": "30px",
                    "padding-left": "30px",
                },
            },
            key="1",
        )

    if tabs == "Dashboard":
        st.title("Bot controller")

        col1, col2, col3, col4 = st.columns([3, 3, 3, 1.5])

        with col1:
            x = st.text_input("x", label_visibility="collapsed", placeholder="x")
            drop_items_toggle = tog.st_toggle_switch(label="Drop-off items", 
                        key="Key10", 
                        default_value=data["drop_items_on_arrival"], 
                        label_after = False, 
                        inactive_color = '#D3D3D3', 
                        active_color="#11567f", 
                        track_color="#29B5E8",
                        )
            
            def saveDropToggle():
                with open('data\data.json', 'r') as file:
                    data = json.load(file)
                
                data['drop_items_on_arrival'] = drop_items_toggle
                
                with open('data\data.json', 'w') as file:
                    json.dump(data, file, indent=4)
            
            if drop_items_toggle == True or drop_items_toggle == False:
                saveDropToggle()
                
        with col2:
            y = st.text_input("y", label_visibility="collapsed", placeholder="y")
            should_disconnect = tog.st_toggle_switch(label="Disconnect", 
                        key="Key5", 
                        default_value=data["disconnect_on_arrival"], 
                        label_after = False, 
                        inactive_color = '#D3D3D3', 
                        active_color="#11567f", 
                        track_color="#29B5E8",
                        )
            
            def saveDisconnectToggle():
                with open('data\data.json', 'r') as file:
                    data = json.load(file)
                
                data['disconnect_on_arrival'] = should_disconnect
                
                with open('data\data.json', 'w') as file:
                    json.dump(data, file, indent=4)
            
            if drop_items_toggle == True or drop_items_toggle == False:
                saveDisconnectToggle()
            
        with col3:
            z = st.text_input("z", label_visibility="collapsed", placeholder="z")
        with col4:
            start_dropoff_bot = st.button("Start bot")
        
        if start_dropoff_bot:
            try:
                makeBot(x, y, z)
                st.toast("Bot started!", icon="✅")

            except ValueError:
                st.toast("Please enter a valid float number", icon="🚨")
        
        st.markdown("""---""")
        
    if tabs == "Settings":
        st.title("Bot settings")
        bot_name = st.text_input(label="Bot name", placeholder="BOT", value=data["bot_name"])

        col1, col2 = st.columns((2, 5))
        
            
        with col1:
            server_ip = st.text_input(label="Server ip", placeholder="127.0.0.1", value=data["server_ip"])
            healt_toggle = tog.st_toggle_switch(label="Quit on low health", 
                        key="Key1", 
                        default_value=data["quit_on_low_health"], 
                        label_after = False, 
                        inactive_color = '#D3D3D3', 
                        active_color="#11567f", 
                        track_color="#29B5E8",
                        )
            
            auto_equip_switch = tog.st_toggle_switch(label="Auto equip armor", 
                        key="Key2", 
                        default_value=data["armor_equip"], 
                        label_after = False, 
                        inactive_color = '#D3D3D3', 
                        active_color="#11567f", 
                        track_color="#29B5E8",
                        )
                        
            def save_changes():
                with open('data\data.json', 'r') as file:
                    data = json.load(file)
                
                data['server_ip'] = server_ip
                data['server_port'] = server_port
                data['bot_name'] = bot_name
                data['quit_on_low_health'] = healt_toggle
                data['low_health_threshold'] = range_slider
                data['armor_equip'] = auto_equip_switch
                
                with open('data\data.json', 'w') as file:
                    json.dump(data, file, indent=4)
            
            
        with col2:
            server_port = st.text_input(label="Server port", placeholder="25565", value=data["server_port"])
            
            range_slider = st.slider(label=" ", label_visibility="collapsed" , min_value=1, max_value=19, value=data["low_health_threshold"], disabled=not healt_toggle)

        save_button = st.button(label="Save changes")
        
        if save_button:
            save_changes()
            st.toast("Saved changes!")

main()
