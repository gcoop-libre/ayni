from gettext import gettext as _

import sys
import gtk
import pygame

import sugar.activity.activity
import sugar.graphics.toolbutton

import sugargame.canvas

import ayni

class AyniActivity(sugar.activity.activity.Activity):

    def __init__(self, handle):
        super(AyniActivity, self).__init__(handle)
        
        self.paused = False

        # Create the game instance.
        #self.game = world.World(in_sugar=True, update_function=self.update_gtk_events)

        # Build the activity toolbar.
        self.build_toolbar()

        # Build the Pygame canvas.
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)

        # Note that set_canvas implicitly calls read_file when resuming from the Journal.
        self.set_canvas(self._pygamecanvas)
        
        #new_scene = presents.Presents(self.game)
        #self.game.change_scene(new_scene)

        # Start the game running (self.game.run is called when the activity constructor returns).
        self._pygamecanvas.run_pygame(ayni.run_in_sugar)

    def build_toolbar(self):        
        stop_play = sugar.graphics.toolbutton.ToolButton('media-playback-stop')
        stop_play.set_tooltip(_("Stop"))
        stop_play.set_accelerator(_('<ctrl>space'))
        stop_play.connect('clicked', self._stop_play_cb)

        toolbar = gtk.Toolbar()
        toolbar.insert(stop_play, 0)
        
        toolbox = sugar.activity.activity.ActivityToolbox(self)
        toolbox.add_toolbar(_("Pygame"), toolbar)
        
        toolbox.show_all()
        self.set_toolbox(toolbox)

    def _stop_play_cb(self, button):
        # Pause or unpause the game.
        self.paused = not self.paused
        #self.game.set_paused(self.paused)
        
        # Update the button to show the next action.
        if self.paused:
            button.set_icon('media-playback-start')
            button.set_tooltip(_("Start"))
        else:
            button.set_icon('media-playback-stop')
            button.set_tooltip(_("Stop"))

    def read_file(self, file_path):
        #self.game.read_file(file_path)
        pass
        
    def write_file(self, file_path):
        #self.game.write_file(file_path)
        pass
