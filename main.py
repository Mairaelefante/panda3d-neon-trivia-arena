from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton
from direct.gui.OnscreenText import OnscreenText

from panda3d.core import (
    AmbientLight,
    PointLight,
    CardMaker,
    TextNode,
    TransparencyAttrib,
    Vec4,
    WindowProperties
)

from data.question import QUESTIONS


class NeonTriviaArena(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.current_question_index = 0
        self.answer_panels = []

        self.setup_window()
        self.setup_input()

        self.menu_root = None
        self.arena_root = None
        self.ui_root = None

        self.show_main_menu()

    def setup_window(self):
        props = WindowProperties()
        props.setTitle("Neon Trivia Arena")
        props.setSize(1280, 720)
        self.win.requestProperties(props)

        self.setBackgroundColor(0.02, 0.01, 0.08, 1)

    def setup_input(self):
        self.accept("escape", self.show_main_menu)
        self.accept("space", self.next_question)
        self.accept("1", self.highlight_answer, [0])
        self.accept("2", self.highlight_answer, [1])
        self.accept("3", self.highlight_answer, [2])
        self.accept("4", self.highlight_answer, [3])

    def clear_scene(self):
        if self.menu_root:
            self.menu_root.removeNode()
            self.menu_root = None

        if self.arena_root:
            self.arena_root.removeNode()
            self.arena_root = None

        if self.ui_root:
            self.ui_root.removeNode()
            self.ui_root = None

    def show_main_menu(self):
        self.clear_scene()

        self.menu_root = aspect2d.attachNewNode("menu_root")

        title = OnscreenText(
            text="NEON TRIVIA ARENA",
            parent=self.menu_root,
            pos=(0, 0.35),
            scale=0.12,
            fg=(0.2, 1.0, 1.0, 1),
            align=TextNode.ACenter,
            mayChange=False
        )

        subtitle = OnscreenText(
            text="A futuristic trivia arena prototype",
            parent=self.menu_root,
            pos=(0, 0.18),
            scale=0.045,
            fg=(1.0, 0.4, 1.0, 1),
            align=TextNode.ACenter,
            mayChange=False
        )

        hint = OnscreenText(
            text="Press START to enter the arena",
            parent=self.menu_root,
            pos=(0, -0.05),
            scale=0.04,
            fg=(0.9, 0.9, 1.0, 1),
            align=TextNode.ACenter,
            mayChange=False
        )

        start_button = DirectButton(
            text="START",
            parent=self.menu_root,
            scale=0.08,
            pos=(0, 0, -0.28),
            command=self.enter_arena
        )

    def enter_arena(self):
        self.clear_scene()

        self.arena_root = render.attachNewNode("arena_root")
        self.ui_root = aspect2d.attachNewNode("ui_root")

        self.setup_camera()
        self.setup_lighting()
        self.build_arena()
        self.build_game_ui()
        self.load_question()

    def setup_camera(self):
        self.disableMouse()

        self.camera.setPos(0, -18, 10)
        self.camera.lookAt(0, 0, 1.5)

    def setup_lighting(self):
        ambient = AmbientLight("soft_neon_ambient")
        ambient.setColor(Vec4(0.18, 0.12, 0.35, 1))
        ambient_np = self.arena_root.attachNewNode(ambient)
        self.arena_root.setLight(ambient_np)

        cyan_light = PointLight("cyan_stage_light")
        cyan_light.setColor(Vec4(0.0, 1.0, 1.0, 1))
        cyan_np = self.arena_root.attachNewNode(cyan_light)
        cyan_np.setPos(-5, -3, 6)
        self.arena_root.setLight(cyan_np)

        magenta_light = PointLight("magenta_stage_light")
        magenta_light.setColor(Vec4(1.0, 0.1, 0.8, 1))
        magenta_np = self.arena_root.attachNewNode(magenta_light)
        magenta_np.setPos(5, 3, 6)
        self.arena_root.setLight(magenta_np)

    def make_card(self, name, parent, frame, pos, hpr, color):
        maker = CardMaker(name)
        maker.setFrame(frame[0], frame[1], frame[2], frame[3])

        card = parent.attachNewNode(maker.generate())
        card.setPos(pos)
        card.setHpr(hpr)
        card.setColor(color)
        card.setTransparency(TransparencyAttrib.MAlpha)
        card.setTwoSided(True)

        return card

    def build_arena(self):
        self.make_card(
            name="arena_floor",
            parent=self.arena_root,
            frame=(-8, 8, -8, 8),
            pos=(0, 0, 0),
            hpr=(0, -90, 0),
            color=(0.03, 0.03, 0.10, 1)
        )

        self.make_card(
            name="center_question_hologram",
            parent=self.arena_root,
            frame=(-3.2, 3.2, -1.2, 1.2),
            pos=(0, 1.4, 2.2),
            hpr=(0, 0, 0),
            color=(0.0, 0.8, 1.0, 0.28)
        )

        self.create_neon_ring()
        self.create_player_podiums()
        self.create_wall_details()

    def create_neon_ring(self):
        ring_positions = [
            (0, -5, 0.03),
            (0, 5, 0.03),
            (-5, 0, 0.03),
            (5, 0, 0.03)
        ]

        ring_frames = [
            (-4, 4, -0.08, 0.08),
            (-4, 4, -0.08, 0.08),
            (-4, 4, -0.08, 0.08),
            (-4, 4, -0.08, 0.08)
        ]

        ring_hprs = [
            (0, -90, 0),
            (0, -90, 0),
            (90, -90, 0),
            (90, -90, 0)
        ]

        colors = [
            (0.0, 1.0, 1.0, 1),
            (1.0, 0.0, 0.8, 1),
            (0.5, 0.2, 1.0, 1),
            (0.0, 1.0, 0.5, 1)
        ]

        for i in range(4):
            self.make_card(
                name=f"neon_floor_strip_{i}",
                parent=self.arena_root,
                frame=ring_frames[i],
                pos=ring_positions[i],
                hpr=ring_hprs[i],
                color=colors[i]
            )

    def create_player_podiums(self):
        podium_data = [
            {
                "name": "Player 1",
                "pos": (-4.8, -2.8, 0.15),
                "color": (0.0, 1.0, 1.0, 1)
            },
            {
                "name": "Player 2",
                "pos": (4.8, -2.8, 0.15),
                "color": (1.0, 0.1, 0.8, 1)
            },
            {
                "name": "Player 3",
                "pos": (-4.8, 3.2, 0.15),
                "color": (0.4, 0.2, 1.0, 1)
            },
            {
                "name": "Player 4",
                "pos": (4.8, 3.2, 0.15),
                "color": (0.0, 1.0, 0.4, 1)
            }
        ]

        for data in podium_data:
            x, y, z = data["pos"]

            self.make_card(
                name=data["name"] + "_base",
                parent=self.arena_root,
                frame=(-1.1, 1.1, -0.7, 0.7),
                pos=(x, y, z),
                hpr=(0, -90, 0),
                color=(data["color"][0], data["color"][1], data["color"][2], 0.45)
            )

            self.make_card(
                name=data["name"] + "_front_panel",
                parent=self.arena_root,
                frame=(-1.0, 1.0, -0.45, 0.45),
                pos=(x, y - 0.45, 0.8),
                hpr=(0, 0, 0),
                color=data["color"]
            )

            label = TextNode(data["name"] + "_label")
            label.setText(data["name"])
            label.setAlign(TextNode.ACenter)
            label.setTextColor(1, 1, 1, 1)

            label_np = self.arena_root.attachNewNode(label)
            label_np.setPos(x, y - 0.52, 1.05)
            label_np.setScale(0.28)
            label_np.setHpr(0, 0, 0)

    def create_wall_details(self):
        for i, x in enumerate([-7, -5, -3, 3, 5, 7]):
            self.make_card(
                name=f"back_wall_light_{i}",
                parent=self.arena_root,
                frame=(-0.08, 0.08, -1.2, 1.2),
                pos=(x, 5.8, 1.5),
                hpr=(0, 0, 0),
                color=(0.2, 0.8, 1.0, 0.8)
            )

        self.make_card(
            name="back_wall_panel",
            parent=self.arena_root,
            frame=(-8, 8, -2.2, 2.2),
            pos=(0, 6.0, 2.0),
            hpr=(0, 0, 0),
            color=(0.05, 0.02, 0.16, 0.9)
        )

    def build_game_ui(self):
        self.question_text = OnscreenText(
            text="Question appears here",
            parent=self.ui_root,
            pos=(0, 0.82),
            scale=0.045,
            fg=(0.9, 1.0, 1.0, 1),
            align=TextNode.ACenter,
            mayChange=True
        )

        self.score_text = OnscreenText(
            text="P1: 0   P2: 0   P3: 0   P4: 0",
            parent=self.ui_root,
            pos=(-1.28, 0.92),
            scale=0.04,
            fg=(0.2, 1.0, 1.0, 1),
            align=TextNode.ALeft,
            mayChange=True
        )

        self.message_text = OnscreenText(
            text="SPACE: next placeholder question | 1-4: highlight answer | ESC: menu",
            parent=self.ui_root,
            pos=(0, -0.92),
            scale=0.035,
            fg=(1.0, 0.7, 1.0, 1),
            align=TextNode.ACenter,
            mayChange=True
        )

        answer_positions = [
            (-0.55, 0.55),
            (0.55, 0.55),
            (-0.55, 0.38),
            (0.55, 0.38)
        ]

        for i in range(4):
            answer = DirectButton(
                text=f"Answer {i + 1}",
                parent=self.ui_root,
                scale=0.055,
                pos=(answer_positions[i][0], 0, answer_positions[i][1]),
                command=self.highlight_answer,
                extraArgs=[i]
            )

            self.answer_panels.append(answer)

    def load_question(self):
        question = QUESTIONS[self.current_question_index]

        self.question_text.setText(question["question"])

        for i in range(4):
            self.answer_panels[i]["text"] = question["answers"][i]
            self.answer_panels[i]["frameColor"] = (0.08, 0.08, 0.18, 0.85)
            self.answer_panels[i]["text_fg"] = (1, 1, 1, 1)

        self.message_text.setText(
            "Question system placeholder. No scoring or validation yet."
        )

    def next_question(self):
        if not self.ui_root:
            return

        self.current_question_index += 1

        if self.current_question_index >= len(QUESTIONS):
            self.current_question_index = 0

        self.load_question()

    def highlight_answer(self, answer_index):
        if not self.ui_root:
            return

        for i in range(4):
            self.answer_panels[i]["frameColor"] = (0.08, 0.08, 0.18, 0.85)

        self.answer_panels[answer_index]["frameColor"] = (0.0, 0.9, 1.0, 1)

        self.message_text.setText(
            f"Answer {answer_index + 1} highlighted. Validation will be added later."
        )


game = NeonTriviaArena()
game.run()