"""Validate axes actor serialization."""

import pyvista as pv
from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify
from trame.widgets.vtk import VtkLocalView, VtkRemoteView

server = get_server()
state, ctrl = server.state, server.controller

state.trame__title = "Axes Widget Validation - Subplots"

# -----------------------------------------------------------------------------

mesh = pv.Cone()

plotter = pv.Plotter(off_screen=True, shape=(1, 2))
plotter.subplot(0, 0)
actor = plotter.add_mesh(pv.Cone())
plotter.reset_camera()
plotter.add_axes()
axes_widget_0 = plotter.renderer.axes_widget

plotter.subplot(0, 1)
actor = plotter.add_mesh(pv.Cylinder())
plotter.reset_camera()

plotter.add_axes()
axes_widget_1 = plotter.renderer.axes_widget


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    layout.icon.click = ctrl.view_reset_camera
    layout.title.set_text(state.trame__title)

    with layout.toolbar:
        vuetify.VSpacer()

    with layout.content:
        with vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        ):
            with vuetify.VCol(classes="fill-height"):
                view = VtkLocalView(plotter.ren_win, ref="local")
                ctrl.view_update = view.update
                ctrl.view_reset_camera.add(view.reset_camera)
                view.set_widgets([axes_widget_0, axes_widget_1])  # or at constructor
            with vuetify.VCol(classes="fill-height"):
                view = VtkRemoteView(plotter.ren_win, ref="remote")
                ctrl.view_reset_camera.add(view.reset_camera)

    # hide footer
    layout.footer.hide()

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
