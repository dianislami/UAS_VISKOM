import cv2
import numpy as np
import time
import random
import pygame

from pose_estimation import PoseEstimator, ROISelector

# ================= CONFIG =================
W, H = 640, 480
LANES = 4
LANE_W = W // LANES
TRIGGER_Y = H - 90
TILE_H = 80

SPEED = 160      # KECEPATAN TILE (lebih kecil = lebih lambat)

SONGS = [
    ("Ariana Grande - Bloodline", "ARIANA GRANDE - BLOODLINE.wav", 40),
    ("Bruno Mars - Die With A Smile", "BRUNO MARS - Die With A Smile.wav", 60),
    ("Cortis - Go", "CORTIS - GO.wav", 80),
]

# ================= AUDIO =================
pygame.mixer.init()

# ================= TILE =================
class Tile:
    def __init__(self, lane):
        self.lane = lane
        self.y = -TILE_H
        self.hit = False
        self.color = (0, 0, 0)

    def update(self, dt):
        self.y += SPEED * dt

# ================= GAME =================
class PianoTilesTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, W)
        self.cap.set(4, H)

        self.frame = None
        self.tracker = PoseEstimator()

        cv2.namedWindow("Piano Tiles")
        self.roi_selector = ROISelector("Piano Tiles", self.on_roi)

        self.tiles = []
        self.last_spawn = time.time()
        self.prev_time = time.time()

        self.score = 0
        self.active_lane = None

        self.state = "MENU"   # MENU → SELECT → PLAY → END
        self.song_index = 0
        self.BEAT = 0.6

    # ---------- DRAW LANE ----------
    def draw_lanes(self, img):
        for i in range(1, LANES):
            cv2.line(img, (i * LANE_W, 0), (i * LANE_W, H), (180,180,180), 1)
        cv2.line(img, (0, TRIGGER_Y), (W, TRIGGER_Y), (0,0,255), 2)

    # ---------- RESET ----------
    def reset_game(self):
        self.tiles = []
        self.score = 0
        self.active_lane = None
        self.last_spawn = time.time()
        self.prev_time = time.time()

    # ---------- ROI ----------
    def on_roi(self, rect):
        self.tracker.add_target(self.frame, rect)
        print("🎯 Object selected")

    # ---------- MAIN LOOP ----------
    def start(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            self.frame = frame.copy()
            img = frame.copy()

            now = time.time()
            dt = now - self.prev_time
            self.prev_time = now

            self.draw_lanes(img)
            key = cv2.waitKey(1)

            # ================= MENU =================
            if self.state == "MENU":
                cv2.putText(img, "SELECT SONG", (220, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 3)

                for i, (name, _, _) in enumerate(SONGS):
                    color = (0,255,0) if i == self.song_index else (200,200,200)
                    cv2.putText(img, name, (160, 150 + i*40),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

                cv2.putText(img, "UP/DOWN or W/S  |  ENTER",
                            (120, 380),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (255,255,255), 2)

                if key in [2490368, ord('w'), ord('W')]:
                    self.song_index = (self.song_index - 1) % len(SONGS)

                elif key in [2621440, ord('s'), ord('S')]:
                    self.song_index = (self.song_index + 1) % len(SONGS)

                elif key in [13, 10]:
                    name, file, bpm = SONGS[self.song_index]
                    pygame.mixer.music.load(file)
                    self.BEAT = 60 / bpm
                    self.tracker.clear_targets()
                    self.reset_game()
                    self.state = "SELECT"

            # ================= SELECT =================
            elif self.state == "SELECT":

                if not self.tracker.tracking_targets:
                    cv2.putText(img, "DRAG OBJECT TO TRACK",
                                (150, 240),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.9, (0,255,255), 2)
                else:
                    cv2.putText(img, "PRESS SPACE TO START",
                                (150, 240),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.9, (0,255,0), 2)

                    if key == 32:
                        pygame.mixer.music.play()
                        self.state = "PLAY"
                        self.last_spawn = time.time()

            # ================= PLAY =================
            elif self.state == "PLAY":
                tracked = self.tracker.track_target(self.frame)
                if tracked:
                    quad = np.int32(tracked[0].quad)
                    cx = int(np.mean(quad[:,0]))
                    self.active_lane = max(0, min(LANES-1, cx // LANE_W))
                    cv2.polylines(img, [quad], True, (0,255,255), 2)

                if now - self.last_spawn >= self.BEAT:
                    self.tiles.append(Tile(random.randint(0, LANES-1)))
                    self.last_spawn = now

                for tile in self.tiles:
                    tile.update(dt)
                    tx = tile.lane * LANE_W
                    ty = int(tile.y)

                    if (not tile.hit and
                        self.active_lane == tile.lane and
                        abs(ty - TRIGGER_Y) < 30):
                        tile.hit = True
                        tile.color = (0,255,0)
                        self.score += 100

                    if not tile.hit and ty > TRIGGER_Y + 30:
                        tile.hit = True
                        tile.color = (0,0,255)

                    cv2.rectangle(img,
                                  (tx, ty),
                                  (tx + LANE_W, ty + TILE_H),
                                  tile.color, -1)

                self.tiles = [t for t in self.tiles if t.y < H]

                cv2.putText(img, f"Score: {self.score}",
                            (20,40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255,255,255), 2)

                if not pygame.mixer.music.get_busy():
                    self.state = "END"

            # ================= END =================
            elif self.state == "END":
                cv2.putText(img, "SONG FINISHED",
                            (190, 200),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0,255,255), 3)

                cv2.putText(img, f"FINAL SCORE: {self.score}",
                            (170, 260),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, (0,255,0), 2)

                cv2.putText(img, "ESC to Exit",
                            (230, 320),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (255,255,255), 2)

            self.roi_selector.draw_rect(img)
            cv2.imshow("Piano Tiles", img)

            if key == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()

# ================= RUN =================
if __name__ == "__main__":
    print("======================================")
    print("      OBJECT TRACKING PIANO TILES ")
    print("======================================")
    print("UP/DOWN or W/S  : Select song")
    print("ENTER           : Confirm")
    print("Drag mouse      : Select object")
    print("SPACE           : Start")
    print("ESC             : Exit")
    print("======================================")

    PianoTilesTracker().start()
