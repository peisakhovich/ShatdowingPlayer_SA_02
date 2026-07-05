import os
import pygame
import pygame_gui


class ControlPanel:

    def __init__(self, manager: pygame_gui.UIManager):

        self.manager = manager
        self.panel = None

        self.status_label = None
        self.speed_label = None
        self.speed_slider = None

        self.btn_play = None
        self.btn_pause = None
        self.btn_stop = None
        self.btn_next = None
        self.btn_prev = None

        # 📁 путь к иконкам
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.IMG_DIR = os.path.join(BASE_DIR, "images")

        self.icons = {}
        self._load_icons()

        self._build_ui()

    # =================================================
    # ICON LOADER
    # =================================================
    def _load_icon(self, name: str):
        path = os.path.join(self.IMG_DIR, name)

        img = pygame.image.load(path)

        if pygame.display.get_surface():
            img = img.convert_alpha()

        return img

    def _load_icons(self):
        self.icons = {
            "play": self._load_icon("play.png"),
            "pause": self._load_icon("pause.png"),
            "stop": self._load_icon("stop.png"),
            "next": self._load_icon("next.png"),
            "prev": self._load_icon("prev.png"),
        }

    # =================================================
    # UI BUILD
    # =================================================
    def _build_ui(self):

        screen_w, screen_h = pygame.display.get_surface().get_size()
        panel_h = 150

        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                0,
                screen_h - panel_h,
                screen_w,
                panel_h
            ),
            manager=self.manager
        )

        panel_w = self.panel.relative_rect.width

        # ---------------- STATUS ----------------
        self.status_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 10, 250, 30),
            text="Status: Ready",
            container=self.panel,
            manager=self.manager
        )

        # ---------------- SPEED ----------------
        self.speed_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(panel_w - 200, 10, 180, 30),
            text="Speed: 1.00x",
            container=self.panel,
            manager=self.manager
        )

        self.speed_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(panel_w - 320, 60, 280, 25),
            start_value=1.0,
            value_range=(0.5, 2.0),
            container=self.panel,
            manager=self.manager
        )

        # ---------------- BUTTONS ----------------
        btn_size = 48
        spacing = 12

        names = ["prev", "play", "pause", "stop", "next"]

        total_width = len(names) * btn_size + (len(names) - 1) * spacing
        start_x = (panel_w - total_width) // 2
        y = 55

        self.btn_prev = self._create_button(start_x + 0 * (btn_size + spacing), y, "prev")
        self.btn_play = self._create_button(start_x + 1 * (btn_size + spacing), y, "play")
        self.btn_pause = self._create_button(start_x + 2 * (btn_size + spacing), y, "pause")
        self.btn_stop = self._create_button(start_x + 3 * (btn_size + spacing), y, "stop")
        self.btn_next = self._create_button(start_x + 4 * (btn_size + spacing), y, "next")

    # =================================================
    # IMAGE BUTTON (UIImage)
    # =================================================
    def _create_button(self, x, y, name):

        img = pygame.transform.smoothscale(
            self.icons[name],
            (48, 48)
        )

        btn = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(x, y, 48, 48),
            image_surface=img,
            container=self.panel,
            manager=self.manager
        )

        btn._name = name  # метка для обработки кликов

        return btn

    # =================================================
    # EVENTS
    # =================================================
    def handle_event(self, event):

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            self.set_speed_label(event.value)

        if event.type == pygame.MOUSEBUTTONDOWN:

            for btn in [self.btn_play, self.btn_pause, self.btn_stop, self.btn_next, self.btn_prev]:

                if btn and btn.get_abs_rect().collidepoint(event.pos):

                    name = getattr(btn, "_name", None)

                    if name:
                        self.set_status(name.capitalize())

    # =================================================
    # HELPERS
    # =================================================
    def set_status(self, text: str):
        self.status_label.set_text(f"Status: {text}")

    def set_speed_label(self, speed: float):
        self.speed_label.set_text(f"Speed: {speed:.2f}x")

    def get_speed(self):
        return self.speed_slider.get_current_value()