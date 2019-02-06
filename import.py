#!/usr/bin/env python

import datetime
import sqlalchemy
import sys
from database import Engine
from database import enums
from database import init_tables
from database.models import Airport
from database.models import Runway
from database.models import RunwayEnd
from dateutil import parser as dateparser
from sqlalchemy.orm import sessionmaker

#nasr_txt_file = "/tmp/FAA_NASR/2019-01-03/APT.txt"
nasr_txt_file = sys.argv[1]

init_tables()

def get_field(record, start, length, var_type="str"):
    s = start - 1
    e = start + length - 1
    field = record[s:e].strip()
    if field == "":
        return None
    else:
        if var_type == "int":
            return int(field)
        elif var_type == "float":
            return float(field)
        elif var_type == "bool":
            if field in ["Y", "y", "T", "t"]:
                return True
            else:
                return False
        elif var_type == "date":
            return dateparser.parse(field)
        elif var_type == "mdydate":
            return datetime.datetime.strptime(field, "%m%d%Y").date()
        elif var_type == "AirportInspectionMethodEnum":
            # Literals like 1 or 2 can't be members of an enum, so translate them
            if field == "1":
                return "O"
            elif field == "2":
                return "T"
            else:
                return field
        elif var_type == "SegmentedCircleEnum":
            # Y-L is an invalid member of an enum, so translate to YL
            if field == "Y-L":
                return "YL"
            else:
                return field
        else:
            return field

Session = sessionmaker(bind=Engine)
session = Session()

with open(nasr_txt_file, "r", errors='replace') as f:
    for line in f:
        record_type = get_field(line, 1, 3)

        if record_type == "APT":
            airport = Airport()
            # L A N D I N G   F A C I L I T Y   D A T A
            airport.facility_site_number = get_field(line, 4, 11)
            airport.facility_type = get_field(line, 15, 13)
            airport.faa_id = get_field(line, 28, 4)
            airport.effective_date = get_field(line, 32, 10, "date")
            # DEMOGRAPHIC DATA
            airport.region = get_field(line, 42, 3)
            airport.field_office = get_field(line, 45, 4)
            airport.state_code = get_field(line, 49, 2)
            airport.state_name = get_field(line, 51, 20)
            airport.county = get_field(line, 71, 21)
            airport.countys_state = get_field(line, 92, 2)
            airport.city = get_field(line, 94, 40)
            airport.name = get_field(line, 134, 50)
            # OWNERSHIP DATA
            airport.ownership_type = get_field(line, 184, 2)
            airport.facility_use = get_field(line, 186, 2)
            airport.owners_name = get_field(line, 188, 35)
            airport.owners_address = get_field(line, 223, 72)
            airport.owners_city_state_zip = get_field(line, 295, 45)
            airport.owners_phone = get_field(line, 340, 16)
            airport.managers_name = get_field(line, 356, 35)
            airport.managers_address = get_field(line, 391, 72)
            airport.managers_city_state_zip = get_field(line, 463, 45)
            airport.managers_phone = get_field(line, 508, 16)
            # GEOGRAPHIC DATA
            airport.latitude_dms = get_field(line, 524, 15)
            airport.latitude_secs = get_field(line, 539, 12)
            airport.longitude_dms = get_field(line, 551, 15)
            airport.longitude_secs = get_field(line, 566, 12)
            airport.coords_method = get_field(line, 578, 1)
            airport.elevation = get_field(line, 579, 7, "float")
            airport.elevation_method = get_field(line, 586, 1)
            airport.mag_variation = get_field(line, 587, 3)
            airport.mag_variation_year = get_field(line, 590, 4, "int")
            airport.pattern_alt = get_field(line, 594, 4, "int")
            airport.sectional = get_field(line, 598, 30)
            airport.distance_from_city = get_field(line, 628, 2, "int")
            airport.direction_from_city = get_field(line, 630, 3)
            airport.land_area = get_field(line, 633, 5, "int")
            # FAA SERVICES
            airport.boundary_artcc_id = get_field(line, 638, 4)
            airport.boundary_artcc_computer_id = get_field(line, 642, 3)
            airport.boundary_artcc_name = get_field(line, 645, 30)
            airport.responsible_artcc_id = get_field(line, 675, 4)
            airport.responsible_artcc_computer_id = get_field(line, 679, 3)
            airport.responsible_artcc_name = get_field(line, 682, 30)
            airport.tie_in_fss_local = get_field(line, 712, 1, "bool")
            airport.tie_in_fss_id = get_field(line, 713, 4)
            airport.tie_in_fss_name = get_field(line, 717, 30)
            airport.fss_local_phone = get_field(line, 747, 16)
            airport.fss_toll_free_phone = get_field(line, 763, 16)
            airport.alternate_fss_id = get_field(line, 779, 4)
            airport.alternate_fss_name = get_field(line, 783, 30)
            airport.alternate_fss_toll_free_phone = get_field(line, 813, 16)
            airport.notam_facility = get_field(line, 829, 4)
            airport.notam_d_available = get_field(line, 833, 1, "bool")
            # FEDERAL STATUS
            airport.activation_date = get_field(line, 834, 7, "date")
            airport.status = get_field(line, 841, 2)
            airport.arff_certification = get_field(line, 843, 15)
            airport.npias_federal_agreements = get_field(line, 858, 7)
            airport.airspace_analysis = get_field(line, 865, 13)
            airport.airport_of_entry = get_field(line, 878, 1, "bool")
            airport.customs_landing_rights = get_field(line, 879, 1, "bool")
            airport.military_civil_join_use = get_field(line, 880, 1, "bool")
            airport.military_landing_rights = get_field(line, 881, 1, "bool")
            # AIRPORT INSPECTION DATA
            airport.inspection_method = get_field(line, 882, 2, "AirportInspectionMethodEnum")
            airport.agency_performing_inspection = get_field(line, 884, 1)
            airport.last_inspection_date = get_field(line, 885, 8, "mdydate")
            airport.last_information_request_complete_date = get_field(line, 893, 8, "mdydate")
            # AIRPORT SERVICES
            airport.fuel_available = get_field(line, 901, 40)
            airport.airframe_repair_service = get_field(line, 941, 5)
            airport.power_plant_repair_service = get_field(line, 946, 5)
            airport.bottled_oxygen = get_field(line, 951, 8)
            airport.bulk_oxygen = get_field(line, 959, 8)
            # AIRPORT FACILITIES
            airport.lighting_schedule = get_field(line, 967, 7)
            airport.beacon_schedule = get_field(line, 974, 7)
            airport.towered_airport = get_field(line, 981, 1, "bool")
            airport.unicom = get_field(line, 982, 7)
            airport.ctaf = get_field(line, 989, 7)
            airport.segmented_circle_available = get_field(line, 996, 4, "SegmentedCircleEnum")
            airport.beacon_color = get_field(line, 1000, 3)
            airport.noncommerical_landing_fee = get_field(line, 1003, 1, "bool")
            airport.landing_facility_used_for_medical_purposes = get_field(line, 1004, 1, "bool")
            # BASED AIRCRAFT
            # ANNUAL OPERATIONS
            # ADDITIONAL AIRPORT DATA
            airport.icao_id = get_field(line, 1211, 7)

            session.merge(airport)

        if record_type == "RWY":
            runway = Runway()
            # F A C I L I T Y   R U N W A Y   D A T A
            runway.facility_site_number = get_field(line, 4, 11)
            runway.name = get_field(line, 17, 7)
            # COMMON RUNWAY DATA
            runway.length = get_field(line, 24, 5, "int")
            runway.width = get_field(line, 29, 4, "int")
            runway.surface_type_condition = get_field(line, 33, 12)
            runway.surface_treatment = get_field(line, 45, 5)
            runway.pavement_classification_number = get_field(line, 50, 11)
            runway.edge_light_intensity = get_field(line, 61, 5)
            # ADDITIONAL COMMON RUNWAY DATA
            runway.length_source = get_field(line, 510, 16)
            runway.length_source_date = get_field(line, 526, 10, "date")
            runway.weight_bearing_capacity_single_wheel = get_field(line, 536, 6)
            runway.weight_bearing_capacity_dual_wheels = get_field(line, 542, 6)
            runway.weight_bearing_capacity_two_dual_wheels_tandem = get_field(line, 548, 6)
            runway.weight_bearing_capacity_two_dual_wheels_double_tandem = get_field(line, 554, 6)
            # BASE END INFORMATION
            base_end = None
            base_end_id = get_field(line, 66, 3)
            if base_end_id:
                base_end = RunwayEnd()
                base_end.facility_site_number = runway.facility_site_number
                base_end.runway_name = runway.name
                base_end.id = base_end_id
                base_end.true_alignment = get_field(line, 69, 3, "int")
                base_end.approach_type = get_field(line, 72, 10)
                base_end.right_traffic = get_field(line, 82, 1, "bool")
                base_end.markings_type = get_field(line, 83, 5)
                base_end.markings_condition = get_field(line, 88, 1)
                # BASE END GEOGRAPHIC DATA
                base_end.latitude_dms = get_field(line, 89, 15)
                base_end.latitude_secs = get_field(line, 104, 12)
                base_end.longitude_dms = get_field(line, 116, 15)
                base_end.longitude_secs = get_field(line, 131, 12)
                base_end.elevation = get_field(line, 143, 7, "float")
                base_end.threshold_crossing_height = get_field(line, 150, 3, "int")
                base_end.visual_glide_path_angle = get_field(line, 153, 4, "float")
                base_end.displaced_threshold_latitude_dms = get_field(line, 157, 15)
                base_end.displaced_threshold_latitude_secs = get_field(line, 172, 12)
                base_end.displaced_threshold_longitude_dms = get_field(line, 184, 15)
                base_end.displaced_threshold_longitude_secs = get_field(line, 199, 12)
                base_end.displaced_threshold_elevation = get_field(line, 211, 7, "float")
                base_end.displaced_threshold_length = get_field(line, 218, 4, "int")
                base_end.touchdown_zone_elevation = get_field(line, 222, 7, "float")
                # BASE END LIGHTING DATA
                base_end.visual_glide_slope_indicators = get_field(line, 229, 5)
                base_end.rvr_equipment = get_field(line, 234, 3)
                base_end.rvv_equipment = get_field(line, 237, 1, "bool")
                base_end.approach_light_system = get_field(line, 238, 8)
                base_end.reil_availability = get_field(line, 246, 1, "bool")
                base_end.centerline_light_availability = get_field(line, 247, 1, "bool")
                base_end.touchdown_lights_availability = get_field(line, 248, 1, "bool")
                # BASE END OBJECT DATA
                base_end.controlling_object_description = get_field(line, 249, 11)
                base_end.controlling_object_marking = get_field(line, 260, 4)
                base_end.part77_category = get_field(line, 264, 5)
                base_end.controlling_object_clearance_slope = get_field(line, 269, 2, "int")
                base_end.controlling_object_height_above_runway = get_field(line, 271, 5, "int")
                base_end.controlling_object_distance_from_runway = get_field(line, 276, 5, "int")
                base_end.controlling_object_centerline_offset = get_field(line, 281, 7)
                # ADDITIONAL BASE END DATA
                base_end.gradient = get_field(line, 560, 5)
                base_end.gradient_direction = get_field(line, 565, 4)
                base_end.position_source = get_field(line, 569, 16)
                base_end.position_date = get_field(line, 585, 10, "date")
                base_end.elevation_source = get_field(line, 595, 16)
                base_end.elevation_date = get_field(line, 611, 10, "date")
                base_end.displaced_threshold_position_source = get_field(line, 621, 16)
                base_end.displaced_threshold_position_date = get_field(line, 637, 10, "date")
                base_end.displaced_threshold_elevation_source = get_field(line, 647, 16)
                base_end.displaced_threshold_elevation_date = get_field(line, 663, 10, "date")
                base_end.touchdown_zone_elevation_source = get_field(line, 673, 16)
                base_end.touchdown_zone_elevation_date = get_field(line, 689, 10, "date")
                base_end.takeoff_run_available = get_field(line, 699, 5, "int")
                base_end.takeoff_distance_available = get_field(line, 704, 5, "int")
                base_end.accelerate_stop_distance_available = get_field(line, 709, 5, "int")
                base_end.landing_distance_available = get_field(line, 714, 5, "int")
                base_end.lahso_distance_available = get_field(line, 719, 5, "int")
                base_end.id_of_lahso_intersecting_runway = get_field(line, 724, 7)
                base_end.description_of_lahso_entity = get_field(line, 731, 40)
                base_end.lahso_latitude_dms = get_field(line, 771, 15)
                base_end.lahso_latitude_secs = get_field(line, 786, 12)
                base_end.lahso_longitude_dms = get_field(line, 798, 15)
                base_end.lahso_longitude_secs = get_field(line, 813, 12)
                base_end.lahso_coords_source = get_field(line, 825, 16)
                base_end.lahso_coords_date = get_field(line, 841, 10, "date")
            # RECIPROCAL END INFORMATION
            recip_end = None
            recip_end_id = get_field(line, 288, 3)
            if recip_end_id:
                recip_end = RunwayEnd()
                recip_end.facility_site_number = runway.facility_site_number
                recip_end.runway_name = runway.name
                recip_end.id = recip_end_id
                recip_end.true_alignment = get_field(line, 291, 3, "int")
                recip_end.approach_type = get_field(line, 294, 10)
                recip_end.right_traffic = get_field(line, 304, 1, "bool")
                recip_end.markings_type = get_field(line, 305, 5)
                recip_end.markings_condition = get_field(line, 310, 1)
                # RECIPROCAL END GEOGRAPHIC DATA
                recip_end.latitude_dms = get_field(line, 311, 15)
                recip_end.latitude_secs = get_field(line, 326, 12)
                recip_end.longitude_dms = get_field(line, 338, 15)
                recip_end.longitude_secs = get_field(line, 353, 12)
                recip_end.elevation = get_field(line, 365, 7, "float")
                recip_end.threshold_crossing_height = get_field(line, 372, 3, "int")
                recip_end.visual_glide_path_angle = get_field(line, 375, 4, "float")
                recip_end.displaced_threshold_latitude_dms = get_field(line, 379, 15)
                recip_end.displaced_threshold_latitude_secs = get_field(line, 394, 12)
                recip_end.displaced_threshold_longitude_dms = get_field(line, 406, 15)
                recip_end.displaced_threshold_longitude_secs = get_field(line, 421, 12)
                recip_end.displaced_threshold_elevation = get_field(line, 433, 7, "float")
                recip_end.displaced_threshold_length = get_field(line, 440, 4, "int")
                recip_end.touchdown_zone_elevation = get_field(line, 444, 7, "float")
                # RECIPROCAL END LIGHTING DATA
                recip_end.visual_glide_slope_indicators = get_field(line, 451, 5)
                recip_end.rvr_equipment = get_field(line, 456, 3)
                recip_end.rvv_equipment = get_field(line, 459, 1, "bool")
                recip_end.approach_light_system = get_field(line, 460, 8)
                recip_end.reil_availability = get_field(line, 468, 1, "bool")
                recip_end.centerline_light_availability = get_field(line, 469, 1, "bool")
                recip_end.touchdown_lights_availability = get_field(line, 470, 1, "bool")
                # RECIPROCAL END OBJECT DATA
                recip_end.controlling_object_description = get_field(line, 471, 11)
                recip_end.controlling_object_marking = get_field(line, 482, 4)
                recip_end.part77_category = get_field(line, 486, 5)
                recip_end.controlling_object_clearance_slope = get_field(line, 491, 2, "int")
                recip_end.controlling_object_height_above_runway = get_field(line, 493, 5, "int")
                recip_end.controlling_object_distance_from_runway = get_field(line, 498, 5, "int")
                recip_end.controlling_object_centerline_offset = get_field(line, 503, 7)
                # ADDITIONAL RECIPROCAL END DATA
                recip_end.gradient = get_field(line, 851, 5)
                recip_end.gradient_direction = get_field(line, 856, 4)
                recip_end.position_source = get_field(line, 860, 16)
                recip_end.position_date = get_field(line, 876, 10, "date")
                recip_end.elevation_source = get_field(line, 886, 16)
                recip_end.elevation_date = get_field(line, 902, 10, "date")
                recip_end.displaced_threshold_position_source = get_field(line, 912, 16)
                recip_end.displaced_threshold_position_date = get_field(line, 928, 10, "date")
                recip_end.displaced_threshold_elevation_source = get_field(line, 938, 16)
                recip_end.displaced_threshold_elevation_date = get_field(line, 954, 10, "date")
                recip_end.touchdown_zone_elevation_source = get_field(line, 964, 16)
                recip_end.touchdown_zone_elevation_date = get_field(line, 980, 10, "date")
                recip_end.takeoff_run_available = get_field(line, 990, 5, "int")
                recip_end.takeoff_distance_available = get_field(line, 995, 5, "int")
                recip_end.accelerate_stop_distance_available = get_field(line, 1000, 5, "int")
                recip_end.landing_distance_available = get_field(line, 1005, 5, "int")
                recip_end.lahso_distance_available = get_field(line, 1010, 5, "int")
                recip_end.id_of_lahso_intersecting_runway = get_field(line, 1015, 7)
                recip_end.description_of_lahso_entity = get_field(line, 1022, 40)
                recip_end.lahso_latitude_dms = get_field(line, 1062, 15)
                recip_end.lahso_latitude_secs = get_field(line, 1077, 12)
                recip_end.lahso_longitude_dms = get_field(line, 1089, 15)
                recip_end.lahso_longitude_secs = get_field(line, 1104, 12)
                recip_end.lahso_coords_source = get_field(line, 1116, 16)
                recip_end.lahso_coords_date = get_field(line, 1132, 10, "date")

            session.merge(runway)
            if base_end:
                session.merge(base_end)
            if recip_end:
                session.merge(recip_end)


session.commit()
