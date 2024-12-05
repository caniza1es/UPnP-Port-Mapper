import miniupnpc
import dearpygui.dearpygui as dpg


upnp = miniupnpc.UPnP()
upnp.discover()
upnp.selectigd()


def add_port_mapping(sender, app_data):
    external_port = int(dpg.get_value("External Port"))
    internal_port = int(dpg.get_value("Internal Port"))
    protocol = dpg.get_value("Protocol")
    description = dpg.get_value("Description")
    internal_ip = upnp.lanaddr


    existing_mapping = upnp.getspecificportmapping(external_port, protocol)
    if existing_mapping:
        dpg.add_text(f"Port {external_port}/{protocol} is already assigned.", parent="Log Window", color=(255, 165, 0))
        return


    try:
        upnp.addportmapping(
            external_port,
            protocol,
            internal_ip,
            internal_port,
            description,
            ""
        )
        dpg.add_text(f"Successfully mapped {protocol} port {external_port} to {internal_ip}:{internal_port}",
                     parent="Log Window", color=(0, 255, 0))
    except Exception as e:
        dpg.add_text(f"Failed to map port {external_port}/{protocol}: {e}", parent="Log Window", color=(255, 0, 0))

# Create the GUI
dpg.create_context()
dpg.create_viewport(title="UPnP Port Mapper", width=800, height=400)

with dpg.window(label="UPnP Port Mapper", width=800, height=400, no_close=True):
    with dpg.group(horizontal=True):
        # Log Window
        with dpg.child_window(label="Log Window", width=400, height=300, tag="Log Window", border=True):
            dpg.add_text("Logs will appear here...", color=(200, 200, 200))

        # Input Area
        with dpg.group():
            dpg.add_text("Enter Port Mapping Details")
            dpg.add_input_int(label="External Port", tag="External Port", default_value=25565, width=200)
            dpg.add_input_int(label="Internal Port", tag="Internal Port", default_value=25565, width=200)
            dpg.add_combo(label="Protocol", tag="Protocol", items=["TCP", "UDP"], default_value="UDP", width=200)
            dpg.add_input_text(label="Description", tag="Description", default_value="Python UPnP Test", width=200)
            dpg.add_button(label="Add Port Mapping", callback=add_port_mapping, width=200)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
