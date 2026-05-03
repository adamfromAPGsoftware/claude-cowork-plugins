#!/usr/bin/env python3
"""Shared Cold Orange Builder for Excalidraw diagrams.

Usage in per-project compose_canvas.py:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[N] /
        "content-plugin/skills/2-copywriter/workflows/excalidraw-diagrams/data"))
    from cold_orange_builder import Builder, ORANGE, AMBER, GREEN, BODY, DIM
"""
import base64
import hashlib
import json
import time
from pathlib import Path

NOW = int(time.time() * 1000)

# ─── Cold Orange Palette ─────────────────────────────────────────────────────
ORANGE    = "#E8590C";  ORANGE_F  = "#FFF4E6"   # Primary cold orange
AMBER     = "#F08C00";  AMBER_F   = "#FFF9DB"   # Secondary warm amber
GREEN     = "#2F9E44";  GREEN_F   = "#EBFBEE"   # green highlight
PURPLE    = "#7048e8";  PURPLE_F  = "#F3F0FF"   # Tool/service boxes
HEADING   = "#1A1A1A"                            # Near-black headings
BODY      = "#495057"                            # Dark grey body text
ARROW_CLR = "#E8590C"                            # Orange flow arrows
DIM       = "#CED4DA";  DIM_F     = "#F8F9FA"   # Dimmed/inactive
BG        = "#FAFAFA"                            # Canvas background

CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


class Builder:
    def __init__(self):
        self.els = []
        self.files = {}
        self._n = 0

    # ── Indexing & ID helpers ─────────────────────────────────────────────────

    def _idx(self):
        n = self._n; self._n += 1
        return "a" + CHARS[(n // 62) % 62] + CHARS[n % 62]

    def _eid(self, seed):
        raw = f"{seed}_{self._n}"
        return hashlib.md5(raw.encode()).hexdigest()[:16]

    def _base(self, eid, kind, x, y, w, h, stroke, fill, extra):
        el = {
            "id": eid, "type": kind,
            "x": x, "y": y, "width": w, "height": h,
            "angle": 0,
            "strokeColor": stroke, "backgroundColor": fill,
            "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
            "roughness": 0, "opacity": 100,
            "groupIds": [], "frameId": None, "index": self._idx(),
            "roundness": None,
            "seed": abs(hash(eid)) % 99999,
            "version": 1, "versionNonce": 1, "isDeleted": False,
            "boundElements": [], "updated": NOW, "link": None, "locked": False,
        }
        el.update(extra)
        return el

    # ── Primitive elements ────────────────────────────────────────────────────

    def rect(self, seed, x, y, w, h, stroke=ORANGE, fill=ORANGE_F, rounded=True):
        eid = self._eid(seed)
        el = self._base(eid, "rectangle", x, y, w, h, stroke, fill, {
            "roundness": {"type": 3} if rounded else None,
        })
        self.els.append(el)
        return eid

    def text(self, seed, x, y, w, label, stroke=HEADING, font_size=18,
             font_family=1, align="center"):
        eid = self._eid(seed)
        el = self._base(eid, "text", x, y, w, font_size * 1.35, stroke, "transparent", {
            "text": label, "fontSize": font_size,
            "fontFamily": font_family,
            "textAlign": align, "verticalAlign": "top",
            "containerId": None, "originalText": label,
            "autoResize": True, "lineHeight": 1.35,
        })
        self.els.append(el)
        return eid

    def title(self, seed, x, y, w, label, font_size=28):
        return self.text(seed, x, y, w, label, HEADING, font_size,
                         font_family=1, align="center")

    # ── Compound elements ─────────────────────────────────────────────────────

    def box(self, seed, x, y, w, h, label, stroke=ORANGE, fill=ORANGE_F,
            sub=None, font_size=17):
        """Rectangle with a centered label. Optional sub-annotation below."""
        self.rect(seed + "_r", x, y, w, h, stroke, fill)
        label_y = y + (h - font_size * 1.35) / 2
        self.text(seed + "_l", x, label_y, w, label, stroke,
                  font_size=font_size, align="center")
        if sub:
            self.text(seed + "_s", x, y + h + 6, w, sub,
                      GREEN, font_size=12, font_family=5, align="center")

    def annotation(self, seed, cx, y, label, color=BODY, font_size=12,
                   width=260, font_family=5):
        self.text(seed, cx - width // 2, y, width, label, color,
                  font_size=font_size, font_family=font_family, align="center")

    def badge(self, seed, x, y, w, h, label, stroke=GREEN, fill=GREEN_F):
        self.rect(seed + "_r", x, y, w, h, stroke, fill)
        self.text(seed + "_l", x, y + (h - 13 * 1.35) / 2, w, label,
                  stroke, font_size=13, font_family=5, align="center")

    # ── Arrow variants ────────────────────────────────────────────────────────

    def arrow_h(self, seed, x_start, y, x_end, color=ARROW_CLR):
        """Horizontal arrow left → right."""
        length = x_end - x_start
        eid = self._eid(seed)
        el = self._base(eid, "arrow", x_start, y, abs(length), 0,
                        color, "transparent", {
            "roughness": 0, "roundness": {"type": 2},
            "points": [[0, 0], [length, 0]],
            "lastCommittedPoint": None,
            "startBinding": None, "endBinding": None,
            "startArrowhead": None, "endArrowhead": "arrow", "elbowed": False,
        })
        self.els.append(el)

    def arrow_v(self, seed, cx, y_start, y_end, color=ARROW_CLR):
        """Vertical arrow top → bottom."""
        length = y_end - y_start
        eid = self._eid(seed)
        el = self._base(eid, "arrow", cx, y_start, 0, abs(length),
                        color, "transparent", {
            "roughness": 0, "roundness": {"type": 2},
            "points": [[0, 0], [0, length]],
            "lastCommittedPoint": None,
            "startBinding": None, "endBinding": None,
            "startArrowhead": None, "endArrowhead": "arrow", "elbowed": False,
        })
        self.els.append(el)

    def arrow_d(self, seed, x1, y1, x2, y2, color=ARROW_CLR):
        """Diagonal arrow from (x1,y1) to (x2,y2)."""
        dx, dy = x2 - x1, y2 - y1
        eid = self._eid(seed)
        el = self._base(eid, "arrow", x1, y1, max(abs(dx), 1), max(abs(dy), 1),
                        color, "transparent", {
            "roughness": 0, "roundness": {"type": 2},
            "points": [[0, 0], [dx, dy]],
            "lastCommittedPoint": None,
            "startBinding": None, "endBinding": None,
            "startArrowhead": None, "endArrowhead": "arrow", "elbowed": False,
        })
        self.els.append(el)

    def arrow_arc(self, seed, x1, y1, x2, y2, sag=120, color=GREEN):
        """Curved arc arrow between two points. sag controls how much it bows."""
        dx, dy = x2 - x1, y2 - y1
        mid_dx = dx / 2
        # Perpendicular direction: for horizontal movement, bow upward (negative y)
        # For a loop going below: use positive sag
        mid_dy = dy / 2 + sag
        eid = self._eid(seed)
        el = self._base(eid, "arrow", x1, y1,
                        max(abs(dx), 1), max(abs(dy) + abs(sag), 1),
                        color, "transparent", {
            "roughness": 0, "roundness": {"type": 2},
            "points": [[0, 0], [mid_dx, mid_dy], [dx, dy]],
            "lastCommittedPoint": None,
            "startBinding": None, "endBinding": None,
            "startArrowhead": None, "endArrowhead": "arrow", "elbowed": False,
        })
        self.els.append(el)

    def arrow_curved(self, seed, x1, y1, x2, y2, bulge_x=200, color=GREEN):
        """Curved arrow that bulges horizontally (original signature preserved)."""
        dx, dy = x2 - x1, y2 - y1
        mid_x = bulge_x
        mid_y = dy / 2
        eid = self._eid(seed)
        el = self._base(eid, "arrow", x1, y1,
                        abs(dx) + abs(bulge_x), abs(dy),
                        color, "transparent", {
            "roughness": 0, "roundness": {"type": 2},
            "points": [[0, 0], [mid_x, mid_y], [dx, dy]],
            "lastCommittedPoint": None,
            "startBinding": None, "endBinding": None,
            "startArrowhead": None, "endArrowhead": "arrow", "elbowed": False,
        })
        self.els.append(el)

    # ── Image / logo embedding ─────────────────────────────────────────────────

    def image(self, seed, x, y, w, h, file_id):
        """Embedded image element referencing a file in self.files."""
        eid = self._eid(seed)
        el = self._base(eid, "image", x, y, w, h, "transparent", "transparent", {
            "fileId": file_id,
            "status": "saved",
            "scale": [1, 1],
        })
        self.els.append(el)
        return eid

    def embed_logo(self, file_path):
        """Read a PNG, base64-encode it, add to self.files. Returns file_id or None."""
        path = Path(file_path)
        if not path.exists():
            return None
        data = path.read_bytes()
        b64 = base64.b64encode(data).decode("ascii")
        file_id = hashlib.md5(data).hexdigest()
        self.files[file_id] = {
            "mimeType": "image/png",
            "id": file_id,
            "dataURL": f"data:image/png;base64,{b64}",
            "created": NOW,
            "lastRetrieved": NOW,
        }
        return file_id

    def logo(self, seed, file_path, x, y, size=40):
        """Embed a logo PNG and place it at (x, y) with given size. No-op if missing."""
        file_id = self.embed_logo(file_path)
        if file_id:
            self.image(seed, x, y, size, size, file_id)
            return True
        return False

    # ── Output ────────────────────────────────────────────────────────────────

    def write(self, filename):
        canvas = {
            "type": "excalidraw", "version": 2,
            "source": "https://excalidraw.com",
            "elements": self.els,
            "appState": {
                "gridSize": None,
                "viewBackgroundColor": BG,
            },
            "files": self.files,
        }
        path = Path(filename)
        path.write_text(json.dumps(canvas, indent=2))
        n_logos = len(self.files)
        print(f"wrote: {filename}  ({len(self.els)} elements"
              + (f", {n_logos} embedded logos" if n_logos else "") + ")")
