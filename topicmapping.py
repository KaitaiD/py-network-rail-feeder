"""
Set up the topic mapping for the convenience of downloading the data feeds. It contains the following four data feeds:

1. MVT - train movement
2. PPM - public performance measure
3. VSTP - very short term planning
4. TD - train describer
"""

# data feeds schema
mv_schema = {
    "event_type": "TEXT", 
    "gbtt_timestamp": "TEXT",
    "original_loc_stanox": "TEXT",
    "planned_timestamp": "INTEGER",
    "timetable_variation": "TEXT",
    "current_train_id": "INTEGER",
    "next_report_run_time": "INTEGER",
    "reporting_stanox": "INTEGER",
    "actual_timestamp": "INTEGER",
    "correction_ind": "TEXT",
    "event_source": "TEXT",
    "platform": "TEXT",
    "division_code": "TEXT",
    "train_terminated": "TEXT",
    "train_id": "INTEGER",
    "variation_status": "TEXT",
    "train_service_code": "INTEGER",
    "toc_id": "INTEGER",
    "loc_stanox": "INTEGER",
    "auto_expected": "TEXT",
    "direction_ind": "TEXT",
    "route": "TEXT",
    "planned_event_type": "TEXT",
    "next_report_stanox": "INTEGER",
}

ppm_schema = {
    "code": "INTEGER", 
    "keySymbol": "TEXT",
    "name": "TEXT",
    "Total": "INTEGER",
    "OnTime": "INTEGER",
    "Late": "INTEGER",
    "CancelVeryLate": "INTEGER",
    "PPM_rag": "TEXT",
    "PPM_text": "INTEGER",
    "RollingPPM_trendInd": "TEXT",
    "RollingPPM_displayFlag": "TEXT",
    "RollingPPM_rag": "TEXT",
    "RollingPPM_text": "INTEGER"
}


vstp_schema = {
    "schedule_id": "INTEGER", 
    "transaction_type": "TEXT",
    "schedule_start_date": "TEXT",
    "schedule_end_date": "TEXT",
    "schedule_days_runs": "TEXT",
    "applicable_timetable": "TEXT",
    "CIF_bank_holiday_running": "TEXT",
    "CIF_train_uid": "INTEGER",
    "train_status": "INTEGER",
    "CIF_stp_indicator": "TEXT"
}

td_schema = {
    "MSG": "TEXT",
    "time": "TEXT", 
    "area_id": "TEXT",
    "msg_type": "TEXT",
    "address": "INTEGER",
    "data": "INTEGER",
    "descr": "TEXT"
}

# data feeds channel
mv_channel = "TRAIN_MVT_ALL_TOC"
ppm_channel = "RTPPM_ALL"
vstp_channel = "VSTP_ALL"
td_channel = "TD_ALL_SIG_AREA"

# data feeds saving name
mv_db = "train_mv_all_toc.db"
ppm_db = "train_ppm_all_toc.db"
vstp_db = "train_vstp_all_toc.db"
td_db = "train_td_all_toc.db"

# complete topic mapping 
TopicMapping = {'MVT': [mv_schema, mv_channel, mv_db], 
                 'PPM': [ppm_schema, ppm_channel, ppm_db],
                 'VSTP':[vstp_schema, vstp_channel, vstp_db],
                 'TD':[td_schema, td_channel, td_db]
}

