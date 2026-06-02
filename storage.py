


def construct_isolines(config: type[Config], AS: type[CoolPropAbstractState_v2], isoline_metadata: dict[str, np.ndarray]) -> np.ndarray:
    # To make thdy property extraction determinate, we need
    # for TS, the horizontal axis
    # for PH, the vertical axis
    if config.thermoplot_settings["diagram_type"] == "TS":
        iv_type = config.thermoplot_settings["diagram_type"][-1]
        dv_type = config.thermoplot_settings["diagram_type"][0]
        axes_flip = False
    elif config.thermoplot_settings["diagram_type"] == "PH":
        iv_type = config.thermoplot_settings["diagram_type"][0]
        dv_type = config.thermoplot_settings["diagram_type"][-1]
        axes_flip = True

    # Extract isoline type and values from metadata
    isoline_type = isoline_metadata["isoline_type"]
    isoline_vals = isoline_metadata["isoline_values"]

    # Currently, evaluating the total iv range would also evaluate thdy properties way outside of the visible domain. This is both 
    # inefficient and can lead to coolprop errors since the thdy property is not specified. Cut the iv range according to the dv range.
    # If isoline is constant in dome, construct isoline in three segments. use knoweledge that this is the case for P and T
    if isoline_type in ['P', 'T']:
        #instantiate isolines list
        isolines_data = []

        for isoline_val in isoline_vals:
            # Extract plotting ranges
            iv_range = copy.deepcopy(config.thermoplot_settings[f"{iv_type}_range"])
            dv_range = copy.deepcopy(config.thermoplot_settings[f"{dv_type}_range"])
            try:
                iv_at_dv_lo = AS.PropsSI(iv_type, dv_type, dv_range[0], isoline_type, isoline_val)
                if isoline_type in ['P', 'T']:
                    iv_range[0] = max(iv_range[0], iv_at_dv_lo)
                else:
                    iv_range[1] = min(iv_range[1], iv_at_dv_lo)
            except:
                pass
            try:
                iv_at_dv_hi = AS.PropsSI(iv_type, dv_type, dv_range[1], isoline_type, isoline_val)
                if isoline_type in ['P', 'T']:
                    iv_range[1] = min(iv_range[1], iv_at_dv_hi)
                else:
                    iv_range[0] = max(iv_range[0], iv_at_dv_hi)
            except:
                pass

            # construct iv_cp according to new range
            iv_cp = np.linspace(iv_range[0], iv_range[1], config.thermoplot_settings["n_cp"])
            
            print(isoline_val, iv_range, dv_range)
            # get critical point value for isoline type
            isoline_type_crit_val = AS.PropsSI(f'{isoline_type}crit')

            # if isoline value is below critical value, split isoline evaluation into three segments
            if isoline_val < isoline_type_crit_val:
                # compute iv_vals at saturation dome for Q = 0 and Q = 1 to get the bounds of the three segments.
                iv_val_Q_0 = AS.PropsSI(iv_type, isoline_type, isoline_val, "Q", 0)
                iv_val_Q_1 = AS.PropsSI(iv_type, isoline_type, isoline_val, "Q", 1)

                # split iv_cp into three segments according to these bounds.
                iv_cp_1 = np.append(iv_cp[iv_cp <= iv_val_Q_0], iv_val_Q_0)
                iv_cp_2 = np.append(np.append(iv_cp[(iv_cp > iv_val_Q_0) & (iv_cp < iv_val_Q_1)], iv_val_Q_0), iv_val_Q_1)
                iv_cp_3 = iv_cp[iv_cp >= iv_val_Q_1]

                # segment 1: from lower bound of visible domain to saturation dome (Q = 0)
                isoline_arr_1 = np.ones(iv_cp_1.shape) * isoline_val
                # print(iv_type, isoline_type, iv_cp_1, isoline_arr_1)
                dv_vals_1 = AS.PropsSI(dv_type, iv_type, iv_cp_1, isoline_type, isoline_arr_1)
                isoline_coords_1 = np.column_stack((iv_cp_1, dv_vals_1))

                # segment 2: from saturation dome (Q = 0) to saturation dome (Q = 1)
                isoline_arr_2 = np.ones(iv_cp_2.shape) * isoline_val
                dv_vals_2 = AS.PropsSI(dv_type, iv_type, iv_cp_2, isoline_type, isoline_arr_2)
                isoline_coords_2 = np.column_stack((iv_cp_2, dv_vals_2))

                # segment 3: from saturation dome (Q = 1) to upper bound of visible domain
                isoline_arr_3 = np.ones(iv_cp_3.shape) * isoline_val
                dv_vals_3 = AS.PropsSI(dv_type, iv_type, iv_cp_3, isoline_type, isoline_arr_3)
                isoline_coords_3 = np.column_stack((iv_cp_3, dv_vals_3))

                # combine isoline coords into one
                isoline_coords = np.concatenate([isoline_coords_1, isoline_coords_2, isoline_coords_3])

                # if axes flip, flip cols of isoline coords
                if axes_flip:
                    isoline_coords = isoline_coords[:, ::-1]
                # store data
                isolines_data.append({"isoline_val": isoline_val, "coords": isoline_coords})
                
                

            # if isoline value is above critical value, simple evaluation at the control point is in order
            if isoline_val > isoline_type_crit_val:
                isoline_arr = np.ones(iv_cp.shape) * isoline_val
                dv_vals = AS.PropsSI(dv_type, iv_type, iv_cp, isoline_type, isoline_arr)
                isoline_coords = np.column_stack((iv_cp, dv_vals))
                print(isoline_coords)
                # if axes flip, flip cols of isoline coords
                if axes_flip:
                    isoline_coords = isoline_coords[:, ::-1]
                isolines_data.append({"isoline_val": isoline_val, "coords": isoline_coords})

    if isoline_type in ['S', 'H']:
        # instantiate isolines list
        isolines_data = []

        for isoline_val in isoline_vals:
            # extract plotting ranges
            iv_range = copy.deepcopy(config.thermoplot_settings[f"{iv_type}_range"])
            dv_range = copy.deepcopy(config.thermoplot_settings[f"{dv_type}_range"])
            try:
                iv_at_dv_lo = AS.PropsSI(iv_type, dv_type, dv_range[0], isoline_type, isoline_val)
                iv_range[0] = max(iv_range[0], iv_at_dv_lo)
            except:
                pass
            try:
                iv_at_dv_hi = AS.PropsSI(iv_type, dv_type, dv_range[1], isoline_type, isoline_val)
                iv_range[1] = min(iv_range[1], iv_at_dv_hi)
            except:
                pass

            # construct iv_cp according to new range
            iv_cp = np.linspace(iv_range[0], iv_range[1], config.thermoplot_settings["n_cp"])
            isoline_arr = np.ones(iv_cp.shape) * isoline_val
            dv_vals = AS.PropsSI(dv_type, iv_type, iv_cp, isoline_type, isoline_arr)
            isoline_coords = np.column_stack((iv_cp, dv_vals))
            # if axes flip, flip cols of isoline coords
            if axes_flip:
                isoline_coords = isoline_coords[:, ::-1]
            isolines_data.append({"isoline_val": isoline_val, "coords": isoline_coords})

    return isolines_data




# def draw_quality_isolines(config: type[Config], AS: type[CoolPropAbstractState_v2], ax: type[plt.Axes], 
#     quality_isoline_data: list[dict[str, float | np.ndarray]], iso_quality_color: str) -> None:
#     if not config.thermoplot_settings["show_isolines"]:
#         return

#     for isoline in quality_isoline_data:
#         q = isoline["isoline_val"]
#         isoline_coords = isoline["coords"]
#         draw_isoline_labeled(ax, [(isoline_coords[:, 0], isoline_coords[:, 1], q)],
#             color=iso_quality_color, frac=0.2,
#             fmt_short=lambda v: rf"${v:.2f}$",
#             fmt_named =lambda v: rf"$x={v:.2f}$",
#             yscale='linear',
#             flip_q1 = (config.thermoplot_settings["fluid_name"] == "R1234ze(Z)")
#             ) 
    






# def _quality_isolines_ts(config, AS, n_lines=9, n_pts=200):
#     # Extract plot limits from config 
#     T_lo, T_hi = config.thermoplot_settings["T_range"]

#     # extract ...
#     T_crit = AS.PropsSI("Tcrit")
#     T_trip = AS.PropsSI("Ttriple")
#     T_arr  = np.linspace(max(T_lo, T_trip*1.001), min(T_hi, T_crit*0.9999), n_pts)
    
#     # instantiate 


#     for Q in np.linspace(0, 1, n_lines):
#         s_arr = np.array([AS.PropsSI("S", "T", T, "Q", Q) for T in T_arr])
#         v = np.isfinite(s_arr)
#         if v.sum() > 3:
#             lines.append((s_arr[v], T_arr[v], Q))
#     return lines


# def _quality_isolines_ph(p_lo, p_hi, cycle_config, n_lines=9, n_pts=200):
#     p_crit = AS.PropsSI("Pcrit")
#     T_trip = AS.PropsSI("Ttriple")
#     p_trip = AS.PropsSI("P", "T", T_trip*1.001, "Q", 0)
#     p_arr  = np.geomspace(max(p_lo*0.5, p_trip*1.01), min(p_hi, p_crit*0.9999), n_pts)
#     lines  = []
#     for Q in np.linspace(0, 1, n_lines):
#         h_arr = np.array([AS.PropsSI("H", "P", p, "Q", Q) for p in p_arr])
#         v = np.isfinite(h_arr)
#         if v.sum() > 3:
#             lines.append((h_arr[v], p_arr[v], Q))
#     return lines













# ### Old code functionality

# def _make_empty_plot_ts(cycle_config, show_spinodal=False):
#     warnings.filterwarnings("ignore")
#     refrigerant = cycle_config["refrigerant"]
#     n_pts = 200

#     s_dome, T_dome = _saturation_dome_ts(cycle_config, n=n_pts*2)
#     valid_dome = np.isfinite(s_dome) & np.isfinite(T_dome)
#     s_dome = s_dome[valid_dome]
#     T_dome = T_dome[valid_dome]
#     if len(s_dome) < 5 or len(T_dome) < 5:
#         raise ValueError(f"Unable to build TS saturation dome for {refrigerant}.")

#     s_lo_raw = np.min(s_dome)
#     s_hi_raw = np.max(s_dome)
#     T_lo_raw = np.min(T_dome)
#     T_hi_raw = np.max(T_dome)
#     ds = max(s_hi_raw - s_lo_raw, 1e-6)
#     dT = max(T_hi_raw - T_lo_raw, 1e-6)

#     p_crit = _q("Pcrit", "T", 300, "Q", 1, cycle_config=cycle_config)
#     T_crit = _q("Tcrit", "T", 300, "Q", 1, cycle_config=cycle_config)

#     # Expand the computational and visible domain beyond the saturation dome.
#     s_lo = s_lo_raw - 0.12 * ds
#     s_hi = s_hi_raw + 0.18 * ds
#     T_lo = T_lo_raw
#     T_hi = max(T_hi_raw + 0.11 * dT, T_crit * 1.175 if np.isfinite(T_crit) else T_hi_raw + 0.11 * dT)

#     fig, ax = plt.subplots(figsize=(10, 7))
#     ax.set_xlim(s_lo, s_hi)
#     ax.set_ylim(T_lo, T_hi)
#     ax.plot(s_dome, T_dome, color='black', lw=1.0, zorder=3)
#     ax.scatter(1203.6835821063594 ,312.2138484973677, s = 0.1)
#     ax.scatter(1203.6515242080186 ,312.504148610755, s = 0.1)

#     _draw_isolines_labeled(
#         ax, _quality_isolines_ts(T_lo, T_hi, cycle_config, n_pts=n_pts),
#         COL_QUALITY, 0.3,
#         fmt_short=lambda v: rf"${v:.2f}$",
#         fmt_named =lambda v: rf"$x={v:.2f}$",
#         flip_q1=(refrigerant == "R1234ze(Z)"))

#     _draw_isolines_labeled(
#         ax, _isobar_lines_ts(s_lo, s_hi, T_lo, T_hi, cycle_config, n_pts=n_pts),
#         COL_ISOBAR_ISO, 0.85,
#         fmt_short=lambda v: rf"${v/1e3:.0f}$",
#         fmt_named =lambda v: rf"$p={v/1e3:.0f}\,\mathrm{{kPa}}$")

#     _draw_isolines_labeled(
#         ax, _isenthalp_lines_ts(s_lo, s_hi, T_lo, T_hi, cycle_config, n_pts=n_pts),
#         COL_ISENTH_ISO, 0.90,
#         fmt_short=lambda v: rf"${v/1e3:.0f}$",
#         fmt_named =lambda v: rf"$h={v/1e3:.0f}\,\mathrm{{kJ/kg}}$")

#     sc, Tc = _isobar_segment(s_lo, s_hi, p_crit, cycle_config, general_config)
#     sc = np.array(sc); Tc = np.array(Tc)
#     valid = (Tc > T_lo) & (Tc <= T_hi * 1.05) & np.isfinite(Tc) & (Tc > 1.0)
#     if valid.any():
#         ax.plot(sc[valid], Tc[valid], color='black', ls=':', lw=1.0, zorder=1)

#     s_crit = _q("S", "P", p_crit, "T", T_crit, cycle_config=cycle_config)
#     if np.isfinite(s_crit) and np.isfinite(T_crit):
#         ax.plot(s_crit, T_crit, marker='o', markerfacecolor='yellow',
#                 markersize=5, markeredgecolor='black', zorder=9)

#     # Optional: true spinodal lines computed via dP/drho|T = 0
#     if show_spinodal:
#         try:
#             liq_s, liq_T, vap_s, vap_T = _get_spinodal_ts(refrigerant, T_lo=T_lo, T_hi=T_hi)
#             if liq_s is not None and len(liq_s) > 2:
#                 ax.plot(liq_s, liq_T, color='#8B0000', ls='--', lw=1.2, zorder=2,
#                         label='Spinodal (liquid)')
#             if vap_s is not None and len(vap_s) > 2:
#                 ax.plot(vap_s, vap_T, color='#DC143C', ls='--', lw=1.2, zorder=2,
#                         label='Spinodal (vapour)')
#         except Exception:
#             pass

#     ax.set_xlabel(r"$s\ [\mathrm{J/kg/K}]$")
#     ax.set_ylabel(r"$T\ [\mathrm{K}]$")
#     fig.tight_layout()
#     return fig





# def make_empty_thdy_plot(diagram_type, cycle_config, output_dir="substance_thermodynamic_diagrams", show_diagrams=True, show_spinodal=None, verbose=True):
#     refrigerant = cycle_config["refrigerant"]
    
#     if show_spinodal is None:
#         show_spinodal = general_config.get("show_spinodal", False)
#     fig = (_make_empty_plot_ts(cycle_config, show_spinodal=show_spinodal) if diagram_type == "TS" 
#            else _make_empty_plot_ph(cycle_config, show_spinodal=show_spinodal))
#     output_root = Path(output_dir)
#     output_path = output_root / refrigerant / f"Thermodynamic Diagram - {refrigerant} - {diagram_type}.pdf"
#     output_path.parent.mkdir(parents=True, exist_ok=True)
#     fig.savefig(output_path, dpi=1000, bbox_inches="tight")
#     if show_diagrams:
#         plt.show()
#     if verbose:
#         logger.info(f"Saved: {output_path}")
#     return fig



# def construct_saturation_dome(config: type[Config]):
#     p_crit = _q("Pcrit", "T", 300, "Q", 1, cycle_config=cycle_config)
#     T_crit = _q("Tcrit", "T", 300, "Q", 1, cycle_config=cycle_config)
#     T_trip = _q("Ttriple", "T", 300, "Q", 1, cycle_config=cycle_config)
#     T_arr  = np.linspace(T_trip*1.001, T_crit*0.9999, n)
#     s_liq  = np.array([_q("S", "T", T, "Q", 0, cycle_config=cycle_config) for T in T_arr])
#     s_vap  = np.array([_q("S", "T", T, "Q", 1, cycle_config=cycle_config) for T in T_arr])
#     s_crit = _q("S", "P", p_crit, "T", T_crit, cycle_config=cycle_config)
#     return (np.concatenate([s_liq, [s_crit], s_vap[::-1]]),
#             np.concatenate([T_arr, [T_crit], T_arr[::-1]]))



#     p_crit = _q("Pcrit", "T", 300, "Q", 1, cycle_config=cycle_config)
#     T_trip = _q("Ttriple", "T", 300, "Q", 1, cycle_config=cycle_config)
#     p_trip = _q("P", "T", T_trip*1.001, "Q", 0, cycle_config=cycle_config)
#     p_arr  = np.geomspace(p_trip*1.01, p_crit*0.9999, n)
#     h_liq  = np.array([_q("H", "P", p, "Q", 0, cycle_config=cycle_config) for p in p_arr])
#     h_vap  = np.array([_q("H", "P", p, "Q", 1, cycle_config=cycle_config) for p in p_arr])
#     h_crit = _q("H", "P", p_crit, "Q", 0.5, cycle_config=cycle_config)
#     return (np.concatenate([h_liq, [h_crit], h_vap[::-1]]),
#             np.concatenate([p_arr, [p_crit], p_arr[::-1]]))



















# dome_metadata_Q_0 = {"isoline_type": "Q", "isoline_value": 0}
#     dome_metadata_Q_1 = {"isoline_type": "Q", "isoline_value": 1}
#     dome_coords_Q_0 = construct_isoline(config, dome_metadata_Q_0, AS) # Q = 0 isoline
#     dome_coords_Q_1 = construct_isoline(config, dome_metadata_Q_1, AS) # Q = 1 isoline
#     dome_coords = np.concatenate([dome_coords_Q_0, crit_coords, dome_coords_Q_1[::-1]]) # combine into single array of coordinates for saturation dome
#     dome_coords = dome_coords[(dome_coords[:, 1] <= dv_hi) & (dome_coords[:, 1] >= dv_lo)] # filter out points outside visible domain

#     # extract independent and dependent variable types
#     if isoline_metadata["isoline_type"] in supported:
#         iv_type = config.thermoplot_settings["diagram_type"][-1]
#         dv_type = config.thermoplot_settings["diagram_type"][0]
#     else:
#         iv_type = config.thermoplot_settings["diagram_type"][0]
#         dv_type = config.thermoplot_settings["diagram_type"][-1]

#     # extract independent variable range and get contol points of iv at which to evaluate isoline.
#     iv_range = config.thermoplot_settings[f"{iv_type}_range"]
#     iv_cp = np.linspace(iv_range[0], iv_range[1], config.thermoplot_settings["n_cp"])
    
#     # Evaluate isoline at said control points. 
#     isoline_vals = np.ones(iv_cp.shape) * isoline_metadata["isoline_value"]
#     dv_vals = AS.PropsSI(dv_type, iv_type, iv_cp, isoline_metadata["isoline_type"], isoline_vals)

#     # combine iv and dv into coordinate pairs and return
#     return np.column_stack((iv_cp, dv_vals))




    # 
    # and whether it is constant in said region. 
    


    # extract isoline values for isolines of this type according to user specification. 
    isoline_vals = np.linspace(config.thermoplot_settings[f"{isoline_type}_range"][0], config.thermoplot_settings[f"{isoline_type}_range"][1], n_isolines)

    # construct isolines. 
    isolines_data = []
    for isoline_val in isoline_vals:
        # evaluate isoline at control points. 
        dv_vals = AS.PropsSI(dv_type, iv_type, iv_cp, isoline_type, isoline_val)

        # combine iv and dv into coordinate pairs and return
        isoline_coords = np.column_stack((dv_vals, iv_cp))

        # store isoline value and coordinates in dictionary
        isolines_data.append({"isoline_val": isoline_val, "coords": isoline_coords})

    return isolines_data










   # if len
    #     raise ValueError(f"Unable to build TS saturation dome for {config.thermoplot_settings['fluid_name']}.")

    s_lo_raw = np.min(s_dome)
    s_hi_raw = np.max(s_dome)
    T_lo_raw = np.min(T_dome)
    T_hi_raw = np.max(T_dome)
    ds = max(s_hi_raw - s_lo_raw, 1e-6)
    dT = max(T_hi_raw - T_lo_raw, 1e-6)

    p_crit = _q("Pcrit", "T", 300, "Q", 1, cycle_config=cycle_config)
    T_crit = _q("Tcrit", "T", 300, "Q", 1, cycle_config=cycle_config)

    # Expand the computational and visible domain beyond the saturation dome.
    s_lo = s_lo_raw - 0.12 * ds
    s_hi = s_hi_raw + 0.18 * ds
    T_lo = T_lo_raw
    T_hi = max(T_hi_raw + 0.11 * dT, T_crit * 1.175 if np.isfinite(T_crit) else T_hi_raw + 0.11 * dT)

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(s_lo, s_hi)
    ax.set_ylim(T_lo, T_hi)
    ax.plot(s_dome, T_dome, color='black', lw=1.0, zorder=3)
    ax.scatter(1203.6835821063594 ,312.2138484973677, s = 0.1)
    ax.scatter(1203.6515242080186 ,312.504148610755, s = 0.1)

    _draw_isolines_labeled(
        ax, _quality_isolines_ts(T_lo, T_hi, cycle_config, n_pts=n_pts),
        COL_QUALITY, 0.3,
        fmt_short=lambda v: rf"${v:.2f}$",
        fmt_named =lambda v: rf"$x={v:.2f}$",
        flip_q1=(refrigerant == "R1234ze(Z)"))

    _draw_isolines_labeled(
        ax, _isobar_lines_ts(s_lo, s_hi, T_lo, T_hi, cycle_config, n_pts=n_pts),
        COL_ISOBAR_ISO, 0.85,
        fmt_short=lambda v: rf"${v/1e3:.0f}$",
        fmt_named =lambda v: rf"$p={v/1e3:.0f}\,\mathrm{{kPa}}$")

    _draw_isolines_labeled(
        ax, _isenthalp_lines_ts(s_lo, s_hi, T_lo, T_hi, cycle_config, n_pts=n_pts),
        COL_ISENTH_ISO, 0.90,
        fmt_short=lambda v: rf"${v/1e3:.0f}$",
        fmt_named =lambda v: rf"$h={v/1e3:.0f}\,\mathrm{{kJ/kg}}$")

    sc, Tc = _isobar_segment(s_lo, s_hi, p_crit, cycle_config, general_config)
    sc = np.array(sc); Tc = np.array(Tc)
    valid = (Tc > T_lo) & (Tc <= T_hi * 1.05) & np.isfinite(Tc) & (Tc > 1.0)
    if valid.any():
        ax.plot(sc[valid], Tc[valid], color='black', ls=':', lw=1.0, zorder=1)

    s_crit = _q("S", "P", p_crit, "T", T_crit, cycle_config=cycle_config)
    if np.isfinite(s_crit) and np.isfinite(T_crit):
        ax.plot(s_crit, T_crit, marker='o', markerfacecolor='yellow',
                markersize=5, markeredgecolor='black', zorder=9)

    # Optional: true spinodal lines computed via dP/drho|T = 0
    if show_spinodal:
        try:
            liq_s, liq_T, vap_s, vap_T = _get_spinodal_ts(refrigerant, T_lo=T_lo, T_hi=T_hi)
            if liq_s is not None and len(liq_s) > 2:
                ax.plot(liq_s, liq_T, color='#8B0000', ls='--', lw=1.2, zorder=2,
                        label='Spinodal (liquid)')
            if vap_s is not None and len(vap_s) > 2:
                ax.plot(vap_s, vap_T, color='#DC143C', ls='--', lw=1.2, zorder=2,
                        label='Spinodal (vapour)')
        except Exception:
            pass

    
    return fig