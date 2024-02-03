import obspython as obs
import math, time

class GlobCycler:
    def __init__(self):
        self.timer_on = False                
        obs.timer_add(self.ticker, 1000)
        self.task = ''
    
    def start_pressed(self):
        if not self.timer_on:
            self.timer_on = True
            self.task = 'Start'
    
    def pause_pressed(self):
        if not self.timer_on:
            self.timer_on = True
            self.task = 'Pause'
            
    
    def stop_pressed(self):
        if not self.timer_on:
            self.timer_on = True
            self.task = 'Stop'

    def ticker(self):        
        if self.timer_on and self.task != '':         
            for scene in obs.obs_frontend_get_scenes():                            
                scene_name = obs.obs_source_get_name(scene)
                current_scene = obs.obs_scene_from_source(scene)
                #print(scene_name)                            
                for sour in obs.obs_scene_enum_items(current_scene):
                    source = obs.obs_sceneitem_get_source(sour)
                    source_name = obs.obs_source_get_name(source)
                    #print(source_name)
                    if self.task == 'Stop':
                        obs.obs_source_media_stop(source)
                    elif self.task == 'Start':
                        obs.obs_source_media_play_pause(source,False)
                    elif self.task == 'Pause':
                        obs.obs_source_media_play_pause(source,True)                    

                    #For future implementation of disabling restart on activate
                    #settings = obs.obs_data_create()
                    #obs.obs_data_set_string(settings,"restart_on_activate",'false')
                    #obs.obs_source_update(source,settings)
                    #obs.obs_data_release(settings)                    

            self.timer_on = False

glob_cycler = GlobCycler()

# Description displayed in the Scripts dialog window
def script_description():
  return """Stop, Pause and Start all video sources"""

def script_properties():  # ui
    props = obs.obs_properties_create()
    obs.obs_properties_add_button(props, "stopButton", "Stop All", lambda x,y: GlobCycler.stop_pressed(glob_cycler))
    obs.obs_properties_add_button(props, "pauseButton", "Pause All", lambda x,y: GlobCycler.pause_pressed(glob_cycler))
    obs.obs_properties_add_button(props, "startButton", "Start All", lambda x,y: GlobCycler.start_pressed(glob_cycler))   
    
    return props
 
