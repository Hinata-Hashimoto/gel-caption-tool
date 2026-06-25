import copy
from dataclasses import dataclass, field


@dataclass
class LadderAnnotation:
    y_img: float
    size: float
    unit: str
    skipped: bool = False


@dataclass
class SampleAnnotation:
    x_img: float
    name: str


@dataclass
class RegionAnnotation:
    x_start: float
    x_end: float
    name: str


class AppState:
    def __init__(self):
        self.image_visible = None      # PIL Image
        self.image_lumi = None         # PIL Image (WB mode only)
        self.wb_mode = False
        self.show_lumi = False
        self.ladder_type = "100bp DNA"
        self.ladder_annotations: list[LadderAnnotation] = []
        self.sample_annotations: list[SampleAnnotation] = []
        self.band_markers: list[tuple[float, float]] = []  # (x_img, y_img)
        self.region_annotations: list[RegionAnnotation] = []
        self.ladder_line_style: str = "short"  # "full" | "short"
        self.sample_font_size: int = 10      # pt / canvas-px base size
        self.undo_history: list[dict] = []  # {'type': str, 'data': any}
        self.redo_history: list[dict] = []

    def current_image(self):
        if self.wb_mode and self.show_lumi and self.image_lumi is not None:
            return self.image_lumi
        return self.image_visible

    def push_undo(self, action_type: str):
        """Record a reversible action before performing it."""
        self.redo_history.clear()
        if action_type in ('crop', 'rotate'):
            self.undo_history.append({
                'type': action_type,
                'data': {
                    'image_visible': self.image_visible.copy() if self.image_visible else None,
                    'image_lumi': self.image_lumi.copy() if self.image_lumi else None,
                    'ladder_annotations': copy.deepcopy(self.ladder_annotations),
                    'sample_annotations': copy.deepcopy(self.sample_annotations),
                    'band_markers': list(self.band_markers),
                    'region_annotations': copy.deepcopy(self.region_annotations),
                }
            })
        else:
            self.undo_history.append({'type': action_type, 'data': None})

    def undo(self) -> str:
        """Undo the last action. Returns a description or empty string."""
        if not self.undo_history:
            return ""
        action = self.undo_history.pop()
        tp = action['type']
        if tp == 'ladder' and self.ladder_annotations:
            removed = self.ladder_annotations.pop()
            self.redo_history.append({'type': 'ladder', 'data': removed})
            return "Ladder annotation removed"
        elif tp == 'band' and self.band_markers:
            removed = self.band_markers.pop()
            self.redo_history.append({'type': 'band', 'data': removed})
            return "Band marker removed"
        elif tp == 'region' and self.region_annotations:
            removed = self.region_annotations.pop()
            self.redo_history.append({'type': 'region', 'data': removed})
            return "Region annotation removed"
        elif tp == 'band_delete' and action['data'] is not None:
            idx, marker = action['data']
            self.band_markers.insert(idx, marker)
            self.redo_history.append({'type': 'band_delete', 'data': (idx, marker)})
            return "Band marker restored"
        elif tp in ('crop', 'rotate') and action['data']:
            redo_data = {
                'image_visible': self.image_visible.copy() if self.image_visible else None,
                'image_lumi': self.image_lumi.copy() if self.image_lumi else None,
                'ladder_annotations': copy.deepcopy(self.ladder_annotations),
                'sample_annotations': copy.deepcopy(self.sample_annotations),
                'band_markers': list(self.band_markers),
                'region_annotations': copy.deepcopy(self.region_annotations),
            }
            self.redo_history.append({'type': tp, 'data': redo_data})
            d = action['data']
            self.image_visible = d['image_visible']
            self.image_lumi = d['image_lumi']
            self.ladder_annotations = d['ladder_annotations']
            self.sample_annotations = d['sample_annotations']
            self.band_markers = d['band_markers']
            self.region_annotations = d.get('region_annotations', [])
            return "Crop undone" if tp == 'crop' else "Rotation undone"
        return ""

    def redo(self) -> str:
        """Redo the last undone action. Returns a description or empty string."""
        if not self.redo_history:
            return ""
        action = self.redo_history.pop()
        tp = action['type']
        if tp == 'ladder':
            self.undo_history.append({'type': 'ladder', 'data': None})
            self.ladder_annotations.append(action['data'])
            return "Ladder annotation redone"
        elif tp == 'band':
            self.undo_history.append({'type': 'band', 'data': None})
            self.band_markers.append(action['data'])
            return "Band marker redone"
        elif tp == 'region':
            self.undo_history.append({'type': 'region', 'data': None})
            self.region_annotations.append(action['data'])
            return "Region annotation redone"
        elif tp == 'band_delete':
            idx, marker = action['data']
            self.undo_history.append({'type': 'band_delete', 'data': (idx, marker)})
            self.band_markers.pop(idx)
            return "Band marker re-deleted"
        elif tp in ('crop', 'rotate') and action['data']:
            undo_data = {
                'image_visible': self.image_visible.copy() if self.image_visible else None,
                'image_lumi': self.image_lumi.copy() if self.image_lumi else None,
                'ladder_annotations': copy.deepcopy(self.ladder_annotations),
                'sample_annotations': copy.deepcopy(self.sample_annotations),
                'band_markers': list(self.band_markers),
                'region_annotations': copy.deepcopy(self.region_annotations),
            }
            self.undo_history.append({'type': tp, 'data': undo_data})
            d = action['data']
            self.image_visible = d['image_visible']
            self.image_lumi = d['image_lumi']
            self.ladder_annotations = d['ladder_annotations']
            self.sample_annotations = d['sample_annotations']
            self.band_markers = d['band_markers']
            self.region_annotations = d.get('region_annotations', [])
            return "Crop redone" if tp == 'crop' else "Rotation redone"
        return ""
