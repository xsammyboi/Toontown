from pandac.PandaModules import *
from direct.gui.DirectGui import *
import Globals
import os.path
import json
from direct.actor.Actor import Actor

POSITIONS = (Vec3(-0.860167, 0, 0.359333),
 Vec3(0, 0, 0.346533),
 Vec3(0.848, 0, 0.3293),
 Vec3(-0.863554, 0, -0.445659),
 Vec3(0.00799999, 0, -0.5481),
 Vec3(0.894907, 0, -0.445659))

NAME_POSITIONS = ((0, 0, 0.16),
 (0, 0, 0.3),
 (0, 0, 0.27),
 (0, 0, 0.25),
 (0, 0, 0.26),
 (0, 0, 0.26))

ButtonNames = (
    "red", "green", "purple", "blue", "pink", "yellow"
)


class StartMenu:

    def __init__(self):
        pass

    def enter(self):
        base.disableMouse()
        self.title.reparentTo(aspect2d)
        self.quitButton.show()
        self.logoutButton.show()
        self.pickAToonBG.setBin('background', 1)
        self.pickAToonBG.reparentTo(aspect2d)
        base.setBackgroundColor(Vec4(0.145, 0.368, 0.78, 1))

    def enterMakeAToon(self, *args):
        buttonName = ""
        for arg in args:
            buttonName += arg
        base.buttonPressed = buttonName
        messenger.send('enterMAT')
        self.exit()

    def enterGame(self, *args):
        self.exit()
        messenger.send('enterGameFromStart')

    def quit(self):
        self.exit()
        messenger.send('exit')

    def exit(self):
        self.title.reparentTo(hidden)
        self.quitButton.hide()
        self.logoutButton.hide()
        self.pickAToonBG.reparentTo(hidden)
        base.setBackgroundColor(0.3, 0.3, 0.3, 1)
        self.unloadStartMenu()

    def loadStartMenu(self):
        buttonsFilled = []
        if os.path.isfile("data/ToonData.json"):
            dataExists = True
            with open('data/ToonData.json') as jsonFile:
                data = json.load(jsonFile)
                for button in ButtonNames:
                    for p in data[button]:
                        headStyle = p['head']
                        if headStyle == None:
                            pass
                        else:
                            buttonsFilled.append(button)
        else:
            dataExists = False
        self.ac = AvatarChoice()
        gui = loader.loadModel('phase_3/models/gui/pick_a_toon_gui')
        gui.flattenMedium()
        gui2 = loader.loadModel('phase_3/models/gui/quit_button')
        gui2.flattenMedium()
        newGui = loader.loadModel('phase_3/models/gui/tt_m_gui_pat_mainGui')
        newGui.flattenMedium()
        self.pickAToonBG = newGui.find('**/tt_t_gui_pat_background')
        self.pickAToonBG.flattenStrong()
        self.pickAToonBG.setPos(0.0, 2.73, 0.0)
        self.pickAToonBG.setScale(1.5, 1, 2)
        self.title = OnscreenText("Pick A Toon To Play", scale=0.15, parent=hidden,
                                  font=Globals.getSignFont(), fg=(1, 0.9, 0.1, 1), pos=(0.0, 0.82))
        self.title.flattenStrong()
        quitHover = gui.find('**/QuitBtn_RLVR')
        self.quitButton = DirectButton(image=(quitHover, quitHover, quitHover), relief=None,
                                       text="Quit", text_font=Globals.getSignFont(),
                                       text_fg=(0.977, 0.816, 0.133, 1), text_pos=(0, -0.035),
                                       text_scale=0.1, image_scale=1, image1_scale=1.05,
                                       image2_scale=1.05, scale=1.05, pos=(-0.25, 0, 0.075), command=self.quit)
        self.quitButton.flattenMedium()
        self.quitButton.reparentTo(base.a2dBottomRight)
        self.logoutButton = DirectButton(relief=None, image=(quitHover, quitHover, quitHover),
                                         text="Logout", text_font=Globals.getSignFont(),
                                         text_fg=(0.977, 0.816, 0.133, 1), text_scale=0.1,
                                         text_pos=(0, -0.035), pos=(0.15, 0, 0.05), image_scale=1.15, image1_scale=1.15,
                                         image2_scale=1.18, scale=0.5, command=self.quit)
        self.logoutButton.reparentTo(base.a2dBottomLeft)
        self.logoutButton.flattenMedium()
        self.logoutButton.hide()
        print buttonsFilled
        if dataExists:
            self.ac.createButtons(buttonsFilled[0])
        else:
            self.ac.createButtons()
        for button in self.ac.buttonList:
            if "-" in button.getName():
                button['command'] = self.enterGame
            else:
                button['command'] = self.enterMakeAToon
        gui.removeNode()
        gui2.removeNode()
        newGui.removeNode()
        self.enter()

    def unloadStartMenu(self):
        for button in self.ac.buttonList:
            button.destroy()
            del button
        self.title.removeNode()
        del self.title
        self.quitButton.destroy()
        del self.quitButton
        self.logoutButton.destroy()
        del self.logoutButton
        self.pickAToonBG.removeNode()
        del self.pickAToonBG


class AvatarChoice:

    def __init__(self):
        self.buttonList = []
        from toon import Toon
        self.toon = Toon.Toon()

    def createButtons(self, *args):
        num = 0
        while num < 6:
            button = DirectButton(image=None, relief=None, text_font=Globals.getSignFont(), text="Make A\nToon",
                                       text0_scale=0.1, text1_scale=0.12, text2_scale=0.12, text_pos=(0, 0), scale=1.01,
                                       pressEffect=1, rolloverSound=Globals.getRolloverSound(),
                                       clickSound=Globals.getClickSound(), pos=(POSITIONS[num]),
                                       text0_fg=(0, 1, 0.8, 0.5), text1_fg=(0, 1, 0.8, 1), text2_fg=(0.3, 1, 0.9, 1),
                                  extraArgs=ButtonNames[num])
            button.setName(ButtonNames[num])

            toonExists = None
            try:
                value = args.index(button.getName())
                with open('data/ToonData.json') as jsonFile:
                    data = json.load(jsonFile)
                    for p in data[button.getName()]:
                        headStyle = p['head']
                        if headStyle == None:
                            pass
                        else:
                            toonExists = 1
            except:
                value = None

            if value != None:
                if toonExists:
                    with open('data/ToonData.json') as jsonFile:
                        data = json.load(jsonFile)
                        for p in data[button.getName()]:
                            headStyle = p['head']
                            headColor = p['headColor']
                            species = p['species']
                            legs = p['legs']
                            legColor = p['legColor']
                            torso = p['torso']
                            torsoColor = p['torsoColor']
                            shirt = p['shirt']
                            bottom = p['shorts']
                            name = p['name']
                    button['text'] = ("", 'Play\nThis Toon', 'Play\nThis Toon')
                    button['text_scale'] = 0.12
                    button['text_fg'] = (1, 0.9, 0.1, 1)
                    self.toon.createToonWithData(species, headStyle, torso, legs, headColor, torsoColor, legColor, shirt, bottom, name)
                    base.toon = self.toon
                    self.head = hidden.attachNewNode('head')
                    self.head.setPosHprScale(0, 5, -0.1, 180, 0, 0, 0.24, 0.24, 0.24)
                    self.head.reparentTo(button.stateNodePath[0], 20)
                    self.head.instanceTo(button.stateNodePath[1], 20)
                    self.head.instanceTo(button.stateNodePath[2], 20)
                    head = self.toon.getHeadForStart()
                    head.getGeomNode().setDepthWrite(1)
                    head.getGeomNode().setDepthTest(1)
                    head.reparentTo(self.head)
                    head.flattenLight()
                    button.setName(ButtonNames[num] + "-filled")
                    nameText = DirectLabel(parent=button, relief=None, scale=0.08, pos=NAME_POSITIONS[num], text=name,
                                               hpr=(0, 0, 0), text_fg=(1, 1, 1, 1), text_wordwrap=8,
                                               text_font=Globals.getInterfaceFont(), state=DGG.DISABLED)
                    nameText.flattenStrong()
            button.resetFrameSize()
            self.buttonList.append(button)
            del button
            num += 1

    def destroy(self):
        for button in self.buttonList:
            button.destroy()
        del self.buttonList
