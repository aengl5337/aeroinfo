#!/usr/bin/env python3

import pprint
import logging

# Set up logging
log_level = "warning"  # Default log level
log_level_map = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

# logging.basicConfig(level=log_level_map[log_level])
logging.basicConfig(
    level=log_level_map[log_level],
    filename="app.log",  # Specify the log file name
    filemode="a",        # Append to the file (use "w" to overwrite)
    format="%(asctime)s - %(levelname)s - %(message)s"
)

from database import find_airport, find_navaid, find_runway, find_runway_end
# from sqlalchemy import create_engine # ***this is not used here, and is now imported in the database module

pp = pprint.PrettyPrinter()


# include = ["demographic"]
# include = None # Same as "demographic"?
include = ["all"]

# print("#  NMM ###############################")
# airport = find_airport("NMM", include=include)
# pp.pprint(airport.to_dict(include=include))
# """
# 	{'activation_date': None,
# 	 'agency_performing_inspection': 'OWNER',
# 	 'agency_performing_inspection_remark': None,
# 	 'airframe_repair_service': None,
# 	 'airframe_repair_service_remark': None,
# 	 'airport_of_entry': None,
# 	 'airport_of_entry_remark': None,
# 	 'airspace_analysis': None,
# 	 'airspace_analysis_remark': None,
# 	 'alternate_fss_id': None,
# 	 'alternate_fss_name': None,
# 	 'alternate_fss_toll_free_phone': None,
# 	 'annual_ops_air_taxi': None,
# 	 'annual_ops_commercial': None,
# 	 'annual_ops_commercial_remark': None,
# 	 'annual_ops_commuter': None,
# 	 'annual_ops_end_of_measurement_period': None,
# 	 'annual_ops_general_aviation_itinerant': None,
# 	 'annual_ops_general_aviation_itinerant_remark': None,
# 	 'annual_ops_general_aviation_local': None,
# 	 'annual_ops_general_aviation_local_remark': None,
# 	 'annual_ops_military': None,
# 	 'annual_ops_military_remark': None,
# 	 'arff_certification': None,
# 	 'arff_certification_remark': None,
# 	 'attendance': ['ALL/MON-THUR/1300-0400++', 'ALL/FRI/1200-2200Z++'],
# 	 'based_general_aviation_helicopters': None,
# 	 'based_general_aviation_helicopters_remark': None,
# 	 'based_general_aviation_jet_engine_airplanes': None,
# 	 'based_general_aviation_jet_engine_airplanes_remark': None,
# 	 'based_general_aviation_multi_engine_airplanes': None,
# 	 'based_general_aviation_multi_engine_airplanes_remark': None,
# 	 'based_general_aviation_single_engine_airplanes': None,
# 	 'based_general_aviation_single_engine_airplanes_remark': None,
# 	 'based_gliders': None,
# 	 'based_gliders_remark': None,
# 	 'based_military_aircraft': None,
# 	 'based_military_aircraft_remark': None,
# 	 'based_ultralight_aircraft': None,
# 	 'based_ultralight_aircraft_remark': None,
# 	 'beacon_color': 'SPLIT-WHITE-GREEN (LIGHTED MILITARY AIRPORT)',
# 	 'beacon_color_remark': None,
# 	 'beacon_schedule': 'SS-SR',
# 	 'beacon_schedule_remark': None,
# 	 'bottled_oxygen': 'NONE',
# 	 'bottled_oxygen_remark': None,
# 	 'boundary_artcc_computer_id': 'ZCM',
# 	 'boundary_artcc_id': 'ZME',
# 	 'boundary_artcc_name': 'MEMPHIS',
# 	 'bulk_oxygen': 'NONE',
# 	 'bulk_oxygen_remark': None,
# 	 'city': 'MERIDIAN',
# 	 'city_remark': None,
# 	 'contract_fuel_available': None,
# 	 'coords_method': 'ESTIMATED',
# 	 'coords_method_remark': None,
# 	 'county': 'LAUDERDALE',
# 	 'county_remark': None,
# 	 'countys_state': 'MS',
# 	 'ctaf': None,
# 	 'ctaf_remark': None,
# 	 'customs_landing_rights': None,
# 	 'customs_landing_rights_remark': None,
# 	 'direction_from_city': 'NE',
# 	 'distance_from_city': 11,
# 	 'distance_from_city_remark': None,
# 	 'effective_date': '2025-04-17',
# 	 'elevation': 315.8,
# 	 'elevation_date': '2009-04-01',
# 	 'elevation_method': 'ESTIMATED',
# 	 'elevation_remark': None,
# 	 'elevation_source': 'MILITARY',
# 	 'faa_id': 'NMM',
# 	 'facility_type': 'AIRPORT',
# 	 'facility_use': 'PRIVATE',
# 	 'facility_use_remark': None,
# 	 'field_office': 'JAN',
# 	 'fss_local_phone': None,
# 	 'fss_toll_free_phone': '1-800-WX-BRIEF',
# 	 'fuel_available': '100LLA++  J8',
# 	 'fuel_available_remark': None,
# 	 'icao_id': 'KNMM',
# 	 'inspection_method': None,
# 	 'land_area': None,
# 	 'land_area_remark': None,
# 	 'landing_facility_used_for_medical_purposes': None,
# 	 'last_information_request_complete_date': '1976-08-13',
# 	 'last_inspection_date': None,
# 	 'last_inspection_date_remark': None,
# 	 'latitude_dms': '32-33-12.5300N',
# 	 'latitude_dms_remark': None,
# 	 'latitude_secs': '117192.5300N',
# 	 'lighting_schedule': 'SEE RMK',
# 	 'lighting_schedule_remark': 'AVBL ONLY DURING HRS OF OPERATION.',
# 	 'longitude_dms': '088-33-18.9500W',
# 	 'longitude_dms_remark': None,
# 	 'longitude_secs': '318798.9500W',
# 	 'mag_variation': '02W',
# 	 'mag_variation_year': 2015,
# 	 'managers_address': 'NAVAL AIR STATION',
# 	 'managers_address_remark': None,
# 	 'managers_city_state_zip': 'MERIDIAN, MS 39301',
# 	 'managers_city_state_zip_remark': None,
# 	 'managers_name': 'COMMANDING OFFICER',
# 	 'managers_name_remark': None,
# 	 'managers_phone': '601 6792470/2505',
# 	 'managers_phone_remark': 'OPNS DUTY OFF (ODO) ON AUTOVON 446-2470.',
# 	 'military_civil_join_use': None,
# 	 'military_civil_join_use_remark': None,
# 	 'military_landing_rights': False,
# 	 'military_landing_rights_remark': None,
# 	 'minimum_operational_network': 'N',
# 	 'name': 'MERIDIAN NAS (MC CAIN FLD)',
# 	 'name_remark': None,
# 	 'noncommerical_landing_fee': None,
# 	 'noncommerical_landing_fee_remark': None,
# 	 'notam_d_available': True,
# 	 'notam_facility': 'NMM',
# 	 'npias_federal_agreements': None,
# 	 'npias_federal_agreements_remark': None,
# 	 'other_services_available': None,
# 	 'other_services_available_remark': None,
# 	 'owners_address': 'OCEANOGRAPHIC OFC-CODE 3142',
# 	 'owners_address_remark': None,
# 	 'owners_city_state_zip': 'WASHINGTON, DC 20373',
# 	 'owners_city_state_zip_remark': None,
# 	 'owners_name': 'US NAVY',
# 	 'owners_name_remark': None,
# 	 'owners_phone': None,
# 	 'owners_phone_remark': None,
# 	 'ownership_type': 'NAVY OWNED',
# 	 'ownership_type_remark': None,
# 	 'pattern_alt': 900,
# 	 'pattern_alt_remark': None,
# 	 'position_date': '2009-04-01',
# 	 'position_source': 'MILITARY',
# 	 'power_plant_repair_service': None,
# 	 'power_plant_repair_service_remark': None,
# 	 'region': 'SOUTHERN',
# 	 'remarks': ['LGT: PORTABLE OLS AVBL RWY 01L, 01R, 19L, 19R AND 28.',
# 	             'JASU: 2(NC-8A) (GTC-85) 1(NCPP-105)',
# 	             'TRAN ALERT: SVC AVBL 1300-0500Z++ MON-THU, 1300-2300Z++ FRI. '
# 	             'DRAG CHUTE REPACK UNAVBL.',
# 	             'RSTD: ALL ACFT RQR PPR, CTC BASE OPS DSN 637-2470/2505, '
# 	             'C601-679-2470/2505. PPR GOOD FOR +/- 1 HR PPR TIME. FOR CALP '
# 	             'PROCESSING CTC AFM VIA BASE OPS.',
# 	             'CAUTION: RWY 19L & 19R HAVE 1 PERCENT DOWN GRAD FIRST 6000 '
# 	             'FT.WILDLIFE IN VCNTY ALL RWY. MAT AND TWY S OF HGR NOT VIS FR '
# 	             'TWR. INTS STU JET TRNG DUR FLD OPR HR.',
# 	             'TFC PAT: BRK ALT 1400 FT MSL. TRAN ACFT EXPC VISUAL APCH. VFR '
# 	             'ACFT CTC MERIDIAN APP WITHIN 25 NM.',
# 	             'MISC: RAMP ELEV 283 FT. EXP ARR/DEP DLY EXTSV STU TRNG. NO '
# 	             'CLASSIFIED MATERIALS AVBL.',
# 	             'BASE OPS 1300-0500Z MON-THUR; 1300-2300Z FRI, CLSD SAT, SUN & '
# 	             'HOLS EXCP BY NOTAM.  .',
# 	             'SCHEDULING POINT: 187 FW, AL ANG. LOCATION: MONTGOMERY, AL. DSN: '
# 	             '358-9255 C334-394-7255.',
# 	             'TRANS ALERT: LTD AIRSTART CAPABILITIES FOR TRAN ACFT. CTC '
# 	             '601-679-2342 TO VERIFY STATUS PRIOR TO REQ PPR.',
# 	             'SERVICE: A-GEAR NORMALLY RIGGED ON ALL RWYS.',
# 	             'FOR CD WHEN UNA VIA FREQ CTC MERIDIAN APCH 601-679-3691, WHEN '
# 	             'MERIDIAN APCH CLSD CTC MEMPHIS ARTCC AT 901-368-8453/8449.',
# 	             'CLSD SAT, SUN AND HOL EXC BY NOTAM.',
# 	             'L SVC AVBL DURING AIRFIELD HRS OF OPS. EXPECT 1 HR REFUEL '
# 	             'DELAYS.',
# 	             "HOOK E28(B) (1750')",
# 	             "HOOK E28(B) (1250')",
# 	             "HOOK E28(B) (1250')",
# 	             "HOOK E28(B) (1748')",
# 	             "HOOK E28(B) (1251')",
# 	             "HOOK E28(B) (1250')"],
# 	 'responsible_artcc_computer_id': 'ZCM',
# 	 'responsible_artcc_id': 'ZME',
# 	 'responsible_artcc_id_remark': None,
# 	 'responsible_artcc_name': 'MEMPHIS',
# 	 'runways': [{'edge_light_intensity': 'HIGH',
# 	              'edge_light_intensity_remark': None,
# 	              'length': 8003,
# 	              'length_remark': None,
# 	              'name': '01L/19R',
# 	              'name_remark': None,
# 	              'pavement_classification_number': '65 /R/C/W/T',
# 	              'pavement_classification_number_remark': None,
# 	              'surface_treatment': 'NONE',
# 	              'surface_treatment_remark': None,
# 	              'surface_type_condition': 'CONC',
# 	              'surface_type_condition_remark': None,
# 	              'width': 200,
# 	              'width_remark': None},
# 	             {'edge_light_intensity': 'HIGH',
# 	              'edge_light_intensity_remark': None,
# 	              'length': 8000,
# 	              'length_remark': None,
# 	              'name': '01R/19L',
# 	              'name_remark': None,
# 	              'pavement_classification_number': '71 /R/C/W/T',
# 	              'pavement_classification_number_remark': None,
# 	              'surface_treatment': 'NONE',
# 	              'surface_treatment_remark': None,
# 	              'surface_type_condition': 'CONC',
# 	              'surface_type_condition_remark': None,
# 	              'width': 200,
# 	              'width_remark': None},
# 	             {'edge_light_intensity': 'HIGH',
# 	              'edge_light_intensity_remark': None,
# 	              'length': 6402,
# 	              'length_remark': None,
# 	              'name': '10/28',
# 	              'name_remark': None,
# 	              'pavement_classification_number': '29 /R/C/W/T',
# 	              'pavement_classification_number_remark': None,
# 	              'surface_treatment': 'NONE',
# 	              'surface_treatment_remark': None,
# 	              'surface_type_condition': 'CONC',
# 	              'surface_type_condition_remark': None,
# 	              'width': 200,
# 	              'width_remark': None}],
# 	 'sectional': 'MEMPHIS',
# 	 'sectional_remark': None,
# 	 'segmented_circle_available': 'NO',
# 	 'segmented_circle_available_remark': None,
# 	 'state_code': 'MS',
# 	 'state_name': 'MISSISSIPPI',
# 	 'status': 'OPERATIONAL',
# 	 'tie_in_fss_id': 'GWO',
# 	 'tie_in_fss_local': False,
# 	 'tie_in_fss_name': 'GREENWOOD',
# 	 'tie_in_fss_remark': None,
# 	 'towered_airport': True,
# 	 'transient_storage_facilities': None,
# 	 'transient_storage_facilities_remark': None,
# 	 'unicom': None,
# 	 'unicom_remark': None,
# 	 'wind_indicator': None,
# 	 'wind_indicator_remark': None}

# """

# print("# NMM runway 19L/01R ##################")
# runway = find_runway("19L", airport, include=include)
# pp.pprint(runway.to_dict(include=include))

# """
# 	{'edge_light_intensity': 'HIGH',
# 	 'edge_light_intensity_remark': None,
# 	 'length': 8000,
# 	 'length_remark': None,
# 	 'length_source': 'MILITARY',
# 	 'length_source_date': '2009-04-01',
# 	 'name': '01R/19L',
# 	 'name_remark': None,
# 	 'pavement_classification_number': '71 /R/C/W/T',
# 	 'pavement_classification_number_remark': None,
# 	 'surface_treatment': 'NONE',
# 	 'surface_treatment_remark': None,
# 	 'surface_type_condition': 'CONC',
# 	 'surface_type_condition_remark': None,
# 	 'weight_bearing_capacity_dual_wheels': None,
# 	 'weight_bearing_capacity_dual_wheels_remark': None,
# 	 'weight_bearing_capacity_single_wheel': None,
# 	 'weight_bearing_capacity_single_wheel_remark': None,
# 	 'weight_bearing_capacity_two_dual_wheels_double_tandem': None,
# 	 'weight_bearing_capacity_two_dual_wheels_double_tandem_remark': None,
# 	 'weight_bearing_capacity_two_dual_wheels_tandem': None,
# 	 'weight_bearing_capacity_two_dual_wheels_tandem_remark': None,
# 	 'width': 200,
# 	 'width_remark': None}
# """

# print("# NMM runway end 19L #####################")
# rwend = find_runway_end("19L", runway, include=include)
# pp.pprint(rwend.to_dict(include=include))
# """
# {'accelerate_stop_distance_available': None,
# 	 'approach_light_system': 'MALSR',
# 	 'approach_light_system_remark': None,
# 	 'approach_type': 'ILS/DME',
# 	 'arresting_gear': 'E28',
# 	 'centerline_light_availability': True,
# 	 'centerline_light_availability_remark': None,
# 	 'controlling_object_centerline_offset': None,
# 	 'controlling_object_centerline_offset_remark': None,
# 	 'controlling_object_clearance_slope': None,
# 	 'controlling_object_clearance_slope_remark': None,
# 	 'controlling_object_description': None,
# 	 'controlling_object_description_remark': None,
# 	 'controlling_object_distance_from_runway': None,
# 	 'controlling_object_distance_from_runway_remark': None,
# 	 'controlling_object_height_above_runway': None,
# 	 'controlling_object_height_above_runway_remark': None,
# 	 'controlling_object_marking': None,
# 	 'controlling_object_marking_remark': None,
# 	 'description_of_lahso_entity': None,
# 	 'displaced_threshold_elevation': None,
# 	 'displaced_threshold_elevation_date': None,
# 	 'displaced_threshold_elevation_source': None,
# 	 'displaced_threshold_latitude_dms': None,
# 	 'displaced_threshold_latitude_dms_remark': None,
# 	 'displaced_threshold_latitude_secs': None,
# 	 'displaced_threshold_length': None,
# 	 'displaced_threshold_length_remark': None,
# 	 'displaced_threshold_longitude_dms': None,
# 	 'displaced_threshold_longitude_dms_remark': None,
# 	 'displaced_threshold_longitude_secs': None,
# 	 'displaced_threshold_position_date': None,
# 	 'displaced_threshold_position_source': None,
# 	 'elevation': 315.7,
# 	 'elevation_date': '2009-04-01',
# 	 'elevation_remark': None,
# 	 'elevation_source': 'MILITARY',
# 	 'gradient': None,
# 	 'gradient_direction': None,
# 	 'gradient_remark': None,
# 	 'id': '19L',
# 	 'id_of_lahso_intersecting_runway': None,
# 	 'id_remark': None,
# 	 'lahso_coords_date': None,
# 	 'lahso_coords_source': None,
# 	 'lahso_distance_available': None,
# 	 'lahso_latitude_dms': None,
# 	 'lahso_latitude_secs': None,
# 	 'lahso_longitude_dms': None,
# 	 'lahso_longitude_secs': None,
# 	 'landing_distance_available': None,
# 	 'latitude_dms': '32-34-53.0400N',
# 	 'latitude_dms_remark': None,
# 	 'latitude_secs': '117293.0400N',
# 	 'longitude_dms': '088-32-54.0100W',
# 	 'longitude_dms_remark': None,
# 	 'longitude_secs': '318774.0100W',
# 	 'markings_condition': 'FAIR',
# 	 'markings_remark': None,
# 	 'markings_type': None,
# 	 'part77_category': None,
# 	 'part77_category_remark': None,
# 	 'position_date': '2009-04-01',
# 	 'position_source': 'MILITARY',
# 	 'reil_availability': None,
# 	 'reil_availability_remark': None,
# 	 'right_traffic': None,
# 	 'right_traffic_remark': None,
# 	 'rvr_equipment': 'TOUCHDOWN',
# 	 'rvr_equipment_remark': None,
# 	 'rvv_equipment': None,
# 	 'takeoff_distance_available': None,
# 	 'takeoff_run_available': None,
# 	 'takeoff_run_available_remark': None,
# 	 'threshold_crossing_height': None,
# 	 'threshold_crossing_height_remark': None,
# 	 'touchdown_lights_availability': None,
# 	 'touchdown_lights_availability_remark': None,
# 	 'touchdown_zone_elevation': 315.8,
# 	 'touchdown_zone_elevation_date': '2009-04-01',
# 	 'touchdown_zone_elevation_source': 'MILITARY',
# 	 'true_alignment': 189,
# 	 'true_alignment_remark': None,
# 	 'visual_glide_path_angle': None,
# 	 'visual_glide_path_angle_remark': None,
# 	 'visual_glide_slope_indicators': 'NONSTANDARD VASI SYSTEM',
# 	 'visual_glide_slope_indicators_remark': 'OPTICAL LANDING SYSTEM & WAVE-OFF.'}
# """
print("#  MEI VORTAC ###########################")
navaid = find_navaid("MEI", "VORTAC")
pp.pprint(navaid)


# print("#  DPA ###############################")
# airport = find_airport("DPA", include=include)
# pp.pprint(airport.to_dict(include=include))

# print("#  dpa ###############################")
# airport = find_airport("dpa", include=include)
# pp.pprint(airport.to_dict(include=include))

# print("# KDPA ###############################")
# airport = find_airport("KDPA", include=include)
# pp.pprint(airport.to_dict(include=include))

# print("#  3CK ###############################")
# airport = find_airport("3CK", include=include)
# pp.pprint(airport.to_dict(include=include))

# print("#  SSI ###############################")
# airport = find_airport("SSI")
# pp.pprint(airport.to_dict())

# include = ["demographic", "runways"]
# print("# LL10 ###############################")
# airport = find_airport("LL10", include=include)
# pp.pprint(airport.to_dict(include=include))

# include = ["additional", "runway_ends"]
# print("# LL10 runway 18/36 ##################")
# runway = find_runway("18", airport, include=include)
# pp.pprint(runway.to_dict(include=include))

# include = ["geographic", "lighting"]
# print("# LL10 runway 36 #####################")
# rwend = find_runway_end("36", runway, include=include)
# pp.pprint(rwend.to_dict(include=include))

# print("#  JOT VOR ###########################")
# navaid = find_navaid("JOT", "VOR/DME")
# pp.pprint(navaid)
