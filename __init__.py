import pcbnew
from pcbnew import ActionPlugin

class MirrorBottomToTopPlugin(ActionPlugin):
    def defaults(self):
        self.name = "Mirror Bottom to Top (with Filled Shapes)"
        self.category = "Modify"
        self.description = "Mirrors bottom copper tracks and filled shapes to top across horizontal Aux Origin"
        self.show_toolbar_button = True
        self.icon_file_name = ""  # Optional: path to a 32x32 icon

    def Run(self):
        board = pcbnew.GetBoard()
        origin_y = board.GetDesignSettings().GetAuxOrigin().y

        top_layer = board.GetLayerID("F.Cu")
        bottom_layer = board.GetLayerID("B.Cu")

        # --- Remove all tracks and shapes from the top copper layer ---
        to_remove = []
        for item in board.GetTracks():
            if (
                isinstance(item, pcbnew.PCB_TRACK)
                and not isinstance(item, pcbnew.PCB_VIA)
                and item.GetLayer() == top_layer
            ):
                to_remove.append(item)
        for item in board.GetDrawings():
            if (
                isinstance(item, pcbnew.PCB_SHAPE)
                and item.GetLayer() == top_layer
                and item.GetShape() in [
                    pcbnew.SHAPE_T_CIRCLE,
                    pcbnew.SHAPE_T_RECT,
                    pcbnew.SHAPE_T_SEGMENT,
                    pcbnew.SHAPE_T_ARC,
                    pcbnew.SHAPE_T_POLY,
                ]
            ):
                to_remove.append(item)

        if len(to_remove) > 0:
            for item in to_remove:
                board.Remove(item)
        else:
            # --- Mirror bottom layer tracks ---
            for item in board.GetTracks():
                if (
                    isinstance(item, pcbnew.PCB_TRACK)
                    and not isinstance(item, pcbnew.PCB_VIA)
                    and item.GetLayer() == bottom_layer
                ):
                    start = item.GetStart()
                    end = item.GetEnd()
    
                    mirrored_start = pcbnew.VECTOR2I(start.x, 2 * origin_y - start.y)
                    mirrored_end = pcbnew.VECTOR2I(end.x, 2 * origin_y - end.y)
    
                    new_track = pcbnew.PCB_TRACK(board)
                    new_track.SetStart(mirrored_start)
                    new_track.SetEnd(mirrored_end)
                    new_track.SetWidth(item.GetWidth())
                    new_track.SetLayer(top_layer)
                    board.Add(new_track)
    
            # --- Mirror filled shapes (like circles, rects, polys) ---
            for item in board.GetDrawings():
                if (
                    isinstance(item, pcbnew.PCB_SHAPE)
                    and item.GetLayer() == bottom_layer
                    and item.GetShape() in [
                        pcbnew.SHAPE_T_CIRCLE,
                        pcbnew.SHAPE_T_RECT,
                        pcbnew.SHAPE_T_SEGMENT,
                        pcbnew.SHAPE_T_ARC,
                        pcbnew.SHAPE_T_POLY,
                    ]
                ):
                    shape_type = item.GetShape()
                    new_shape = pcbnew.PCB_SHAPE(board)
                    new_shape.SetShape(shape_type)
                    new_shape.SetLayer(top_layer)
                    new_shape.SetWidth(item.GetWidth())
                    if hasattr(new_shape, "SetFilled") and item.IsFilled():
                        new_shape.SetFilled(True)
    
                    # Mirror Start/End
                    p1 = item.GetStart()
                    p2 = item.GetEnd()
                    mirrored_p1 = pcbnew.VECTOR2I(p1.x, 2 * origin_y - p1.y)
                    mirrored_p2 = pcbnew.VECTOR2I(p2.x, 2 * origin_y - p2.y)
                    new_shape.SetStart(mirrored_p1)
                    new_shape.SetEnd(mirrored_p2)
    
                    # Mirror polygon if it's a filled shape
                    if shape_type == pcbnew.SHAPE_T_POLY:
                        original_poly = item.GetPolyShape()
                        mirrored_poly = pcbnew.SHAPE_POLY_SET()
                        for contour_idx in range(original_poly.OutlineCount()):
                            mirrored_poly.NewOutline()
                            for pt_idx in range(original_poly.Outline(contour_idx).PointCount()):
                                pt = original_poly.Outline(contour_idx).GetPoint(pt_idx)
                                mirrored_pt = pcbnew.VECTOR2I(pt.x, 2 * origin_y - pt.y)
                                mirrored_poly.Append(mirrored_pt)
                        new_shape.SetPolyShape(mirrored_poly)
    
                    board.Add(new_shape)

        pcbnew.Refresh()

MirrorBottomToTopPlugin().register()
