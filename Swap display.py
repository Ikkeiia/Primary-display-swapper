import win32api
import win32con

def toggle_primary_keep_layout():
    # Get all monitor handles
    monitors = win32api.EnumDisplayMonitors()
    if len(monitors) < 2:
        return

    # Get detailed info for both monitors
    m1_info = win32api.GetMonitorInfo(monitors[0][0])
    m2_info = win32api.GetMonitorInfo(monitors[1][0])
    print(f"M1 info {m1_info}")
    print(f"M2 info {m2_info}")


    # Identify which one is currently Primary (at 0,0)
    if m1_info['Flags'] & win32con.MONITORINFOF_PRIMARY:
        primary_dev = m1_info['Device']
        secondary_dev = m2_info['Device']
    else:
        primary_dev = m2_info['Device']
        secondary_dev = m1_info['Device']

    # Get the current resolution of the primary to know how far to shift
    prim_settings = win32api.EnumDisplaySettings(primary_dev, win32con.ENUM_CURRENT_SETTINGS)
    sec_settings = win32api.EnumDisplaySettings(secondary_dev, win32con.ENUM_CURRENT_SETTINGS)

    # SWAP LOGIC:
    # We move the secondary to (0,0) to make it primary
    # We move the old primary to where the secondary used to be (the inverse)
    
    old_sec_x = sec_settings.Position_x
    old_sec_y = sec_settings.Position_y

    # 1. Prepare Secondary to become Primary at (0,0)
    sec_settings.Position_x = 0
    sec_settings.Position_y = 0
    win32api.ChangeDisplaySettingsEx(secondary_dev, sec_settings, win32con.CDS_SET_PRIMARY | win32con.CDS_UPDATEREGISTRY | win32con.CDS_NORESET)

    # 2. Prepare Old Primary to move to the Secondary's old spot
    prim_settings.Position_x = -old_sec_x
    prim_settings.Position_y = -old_sec_y
    win32api.ChangeDisplaySettingsEx(primary_dev, prim_settings, win32con.CDS_UPDATEREGISTRY | win32con.CDS_NORESET)

    # 3. Apply all changes
    win32api.ChangeDisplaySettingsEx(None, None, 0)
    print("Swapped Primary without breaking the layout.")

if __name__ == "__main__":
    toggle_primary_keep_layout()