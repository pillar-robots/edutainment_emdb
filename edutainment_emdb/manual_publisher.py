import threading
import tkinter as tk
from tkinter import ttk
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Int32, Bool

# ── Topic configuration ──────────────────────────────────────────────────────
# msg_type, key, topic, default, min_val, max_val
TOPICS = [
    (Float32,   "teacher_present_perception", "/teacher/is_present", 0.0, 0.0, 1.0),
    (Float32,   "teacher_type_perception", "/teacher/type", 0.0, 0.0, 1.0),
    (Float32,   "student_type_perception", "/student/type", 0.0, 0.0, 1.0),
    (Float32,   "challenge_completion_perception", "/student/challenge_completion", 0.0, 0.0, 1.0),
    (Float32,   "python_error_streak_perception", "/student/metrics/python_error_streak", 0.0, 0.0, 1.0),
    (Float32,   "evaluation_error_streak_perception", "/student/metrics/evaluation_error_streak", 0.0, 0.0, 1.0),
    (Float32,   "bored_perception", "/student/bored", 0.0, 0.0, 1.0),
    (Float32,   "standing_perception", "/student/standing", 0.0, 0.0, 1.0)
    ]

# ── ROS2 Node ────────────────────────────────────────────────────────────────
class ManualPublisher(Node):
    def __init__(self):
        super().__init__("manual_edutainment_publisher")
        self.publishers_ = {}
        self.values = {}
        self.topic_types = {}
        for msg_type, key, topic, default, min_val, max_val in TOPICS:
            self.publishers_[key] = self.create_publisher(msg_type, topic, 2)
            self.values[key] = default
            self.topic_types[key] = msg_type
        self.create_timer(1.0, self._publish)

    def _publish(self):
        for key, pub in self.publishers_.items():
            msg_type = self.topic_types[key]
            if msg_type is Bool:
                msg = Bool()
                msg.data = bool(self.values[key])
            elif msg_type is Float32:
                msg = Float32()
                msg.data = float(self.values[key])
            else:
                msg = Int32()
                msg.data = int(self.values[key])
            pub.publish(msg)

# ── Tkinter GUI ──────────────────────────────────────────────────────────────
class SliderApp:
    # Palette
    BG        = "#0d0d0f"
    PANEL     = "#16161a"
    ACCENT    = "#00e5ff"
    ACCENT2   = "#ff4081"
    TEXT      = "#e8eaf6"
    SUBTEXT   = "#6c7a93"
    TRACK_BG  = "#1e2030"
    FONT_MONO = ("Courier New", 10)
    FONT_LABEL= ("Courier New", 11, "bold")
    FONT_TITLE= ("Courier New", 18, "bold")

    def __init__(self, root: tk.Tk, node: ManualPublisher):
        self.root = root
        self.node = node
        root.title("ROS2 Manual Publisher")
        root.configure(bg=self.BG)
        root.resizable(False, False)
        self._build_ui()

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Header ──
        header = tk.Frame(self.root, bg=self.BG)
        header.pack(fill="x", padx=24, pady=(20, 4))
        tk.Label(
            header,
            text="Topic Publisher",
            font=self.FONT_TITLE,
            fg=self.ACCENT,
            bg=self.BG,
        ).pack(side="left")
        self._status_dot = tk.Label(
            header, text="●", font=("Courier New", 14), fg="#444", bg=self.BG
        )
        self._status_dot.pack(side="right", padx=(0, 4))
        tk.Label(header, text="publishing", font=self.FONT_MONO,
                 fg=self.SUBTEXT, bg=self.BG).pack(side="right")
        # separator
        tk.Frame(self.root, bg=self.ACCENT, height=1).pack(fill="x", padx=24, pady=(0, 16))
        # ── Slider rows ──
        container = tk.Frame(self.root, bg=self.BG)
        container.pack(padx=24, pady=(0, 20))
        self._vars: dict[str, tk.DoubleVar] = {}
        for i, (msg_type, key, topic, default, min_val, max_val) in enumerate(TOPICS):
            self._add_row(
                container,
                i,
                msg_type,
                key,
                topic,
                default,
                min_val,
                max_val,
            )
        # ── Footer ──
        tk.Frame(self.root, bg="#222", height=1).pack(fill="x", padx=24)
        footer = tk.Frame(self.root, bg=self.BG)
        footer.pack(fill="x", padx=24, pady=(8, 16))
        tk.Label(
            footer,
            text="Values published every 1 s  ·  drag sliders to update",
            font=("Courier New", 9),
            fg=self.SUBTEXT,
            bg=self.BG,
        ).pack(side="left")
        # Blink the status dot
        self._blink()

    def _add_row(
        self,
        parent,
        row,
        msg_type,
        key,
        topic,
        default,
        min_val,
        max_val,
    ):
        row_bg = self.PANEL if row % 2 == 0 else self.BG
        frame = tk.Frame(parent, bg=row_bg, padx=10, pady=6)
        frame.pack(fill="x", pady=1)
        tk.Label(
            frame,
            text=f"{topic:<35}",
            font=self.FONT_MONO,
            fg=self.TEXT,
            bg=row_bg,
            anchor="w",
            width=35,
        ).pack(side="left")
        # -------------------------
        # Bool -> checkbox
        # -------------------------
        if key == "teacher_present_perception":
            var = tk.BooleanVar(value=bool(default))
            self._vars[key] = var
            cb = ttk.Checkbutton(
                frame,
                variable=var,
                command=lambda k=key, v=var: self._on_bool_change(k, v),
            )
            cb.pack(side="left", padx=(12, 8))
            val_label = tk.Label(
                frame,
                text=str(bool(default)),
                font=self.FONT_LABEL,
                fg=self.ACCENT,
                bg=row_bg,
                width=6,
                anchor="e",
            )
            val_label.pack(side="left")
            var.trace_add(
                "write",
                lambda *_, k=key, lbl=val_label: self._update_label(k, lbl),
            )
            return

        # -------------------------
        # Int / Float sliders
        # -------------------------
        if msg_type is Float32:
            var = tk.DoubleVar(value=float(default))
        else:
            var = tk.IntVar(value=int(default))
        self._vars[key] = var
        style_name = f"Accent{row}.Horizontal.TScale"
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            style_name,
            background=row_bg,
            troughcolor=self.TRACK_BG,
            sliderthickness=16,
            sliderrelief="flat",
        )
        slider = ttk.Scale(
            frame,
            from_=min_val,
            to=max_val,
            orient="horizontal",
            variable=var,
            length=320,
            style=style_name,
            command=lambda val, k=key: self._on_change(k, val),
        )
        slider.pack(side="left", padx=(12, 8))
        val_label = tk.Label(
            frame,
            text=f"{default}",
            font=self.FONT_LABEL,
            fg=self.ACCENT,
            bg=row_bg,
            width=8,
            anchor="e",
        )
        val_label.pack(side="left")
        var.trace_add(
            "write",
            lambda *_, k=key, lbl=val_label: self._update_label(k, lbl),
        )
    # ── Callbacks ────────────────────────────────────────────────────────────
    def _on_change(self, key: str, val: str):
        self.node.values[key] = float(val)
    
    def _on_bool_change(self, key: str, var: tk.BooleanVar):
        self.node.values[key] = float(bool(var.get()))

    def _update_label(self, key: str, label: tk.Label):
        v = self._vars[key].get()
        if self.node.topic_types[key] is Float32:
            label.config(text=f"{float(v):.2f}")
        else:
            label.config(text=str(v))

    def _blink(self):
        current = self._status_dot.cget("fg")
        next_color = self.ACCENT if current != self.ACCENT else "#444"
        self._status_dot.config(fg=next_color)
        self.root.after(800, self._blink)

# ── Entry-point ──────────────────────────────────────────────────────────────
def main(args=None):
    rclpy.init(args=args)
    node = ManualPublisher()
    # Spin ROS2 in a background daemon thread
    ros_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    ros_thread.start()
    # Run tkinter on the main thread (required on most platforms)
    root = tk.Tk()
    SliderApp(root, node)
    try:
        root.mainloop()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()