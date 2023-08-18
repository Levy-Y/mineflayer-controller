import streamlit as st
from st_on_hover_tabs import on_hover_tabs
from javascript import require, On

RANGE_GOAL = 0

class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def abort_queue():
    print("TODO 1")

def pause_queue():
    print("TODO 2")
    
def Bot_start(ip, username="Bot"):
  mineflayer = require('mineflayer')
  pathfinder = require('mineflayer-pathfinder')

  bot = mineflayer.createBot({
    'host': ip,
    'port': 25565,
    'username': username
  })

  bot.loadPlugin(pathfinder.pathfinder)
  print("[INFO] Started mineflayer")

  @On(bot, 'spawn')
  def handle(*args):
    print("[INFO] Bot spawned succesfully")
    
    mcData = require('minecraft-data')(bot.version)
    movements = pathfinder.Movements(bot, mcData)

    bot.pathfinder.setMovements(movements)
    bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, RANGE_GOAL))
    
def main():
    st.set_page_config(page_title="Bot controller", page_icon="🕹", layout="centered", initial_sidebar_state="auto")
    
    st.markdown('<style>' + open('C:\\Users\\leven\\Desktop\\mineflayer_bot\\frontend\\styles.css').read() + '</style>', unsafe_allow_html=True)
    
    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Connect', 'Dashboard'], 
                             iconName=['economy', 'dashboard'],
                             styles = {'navtab': {'background-color':'#111',
                                                  'color': '#818181',
                                                  'font-size': '18px',
                                                  'transition': '.3s',
                                                  'white-space': 'nowrap',
                                                  'text-transform': 'uppercase'},
                                       'tabOptionsStyle': {':hover :hover': {'color': 'red',
                                                                      'cursor': 'pointer'}},
                                       'iconStyle':{'position':'fixed',
                                                    'left':'7.5px',
                                                    'text-align': 'left'},
                                       'tabStyle' : {'list-style-type': 'none',
                                                     'margin-bottom': '30px',
                                                     'padding-left': '30px'}},
                             key="1")
    
    
    if tabs == 'Dashboard':
        st.title("Bot controller")

        col1, col2, col3 = st.columns([1.5, 1.5, 1.5])
        
        with col1:
            x = st.text_input("x", value="0")
            queue_button = st.button("Add to queue")
        with col2:
            y = st.text_input("y", value="0")
            abort_button = st.button("Abort")
        with col3:
            z = st.text_input("z", value="0")
            pause_button = st.button("Pause")
    
        try:
            if queue_button:
                global pos
                pos = Vec3(float(x), float(y), float(z))
                st.success('Command succesfully added to queue!')
                Bot_start("127.0.0.1", "test_bot")
            
        except ValueError:
            st.error('Please enter a valid float number', icon="🚨")

        if abort_button:
            abort_queue()
            st.warning('Removed all commands from the queue!')

        if pause_button:
            pause_queue()
            st.info('Succesfully paused the queue!')
    
    if tabs == 'Connect':
        st.title("Connect to server")
        
        col1, col2, col3 = st.columns([1.5, 1.5, 1.5])
        
        with col1:
            ip = st.text_input("IP address")
        with col2:
            connect_button = st.button("Connect")
        with col3:
            connect_button = st.button("Disconnect")
main()