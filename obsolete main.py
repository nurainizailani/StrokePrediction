#initialise libraries and packages
import os
import sklearn
import pandas as pd
import matplotlib.pyplot as plt
#control exports
export_data = False
export_img = False
#initialise variables
variable_type = {
    'metadata_var': ['randhosp_id', 'randpat_id', 'pretrialexp', 'country', 'trialphase', 'phase',
                     'gender', 'weight', 'glucose', 'agecat', 'ageimp', 'age_true', 'UKextra'],
    'randomisation_var': ['age', 'randyear', 'randmonth', 'randhour', 'randmin', 'randdelay', 'livealone_rand', 'indepinadl_rand', 'nobleed_rand', 'infarct', 'antiplat_rand', 'atrialfib_rand', 'sbprand', 'dbprand', 'gcs_eye_rand', 'gcs_motor_rand', 'gcs_verbal_rand', 'gcs_score_rand', 'nihss', 'liftarms_rand', 'ablewalk_rand', 'weakface_rand', 'weakarm_rand', 'weakleg_rand', 'dysphasia_rand', 'hemianopia_rand', 'visuospat_rand', 'brainstemsigns_rand', 'otherdeficit_rand', 'stroketype', 'pred_nihss', 'randvioltype', 'sbpstart', 'sbp30min', 'sbp60min', 'sbp24h', 'dbpstart',
                          'dbp30min', 'dbp60min', 'dbp24h', 'treatdelay'],
    'treatment_var': ['itt_treat', 'recinfus', 'gotbolus', 'infus_start', 'infus_halt', 'totdose',
                      'nostartcode', 'treatment', 'haltcode'],
    'seven_day_var': ['other_antiplat_pre', 'anticoag_pre', 'asl', 'rec7', 'consent_type', 'aspirin_pre',
                      'dipyridamole_pre', 'clopidogrel_pre', 'lowdose_heparin_pre',
                      'fulldose_heparin_pre', 'warfarin_pre', 'antithromb_pre', 'hypertension_pre',
                      'diabetes_pre', 'stroke_pre', 'aspirin_day1', 'antiplatelet_day1',
                      'lowdose_heparin_day1', 'full_anticoag_day1', 'lowerBP_day1',
                      'nontrial_thromb_day1', 'iv_fluids_day1', 'insulin_day1', 'aspirin_days2to7',
                      'antiplatelet_days2to7', 'lowdose_heparin_days2to7', 'full_anticoag_days2to7',
                      'lowerBP_days2to7', 'nontrial_thromb_days2to7', 'nasogastric_days2to7',
                      'antibiotics_days2to7', 'findiag7', 'brainsite7', 'haem_type7', 'nonstroke_type7',
                      'med_adno', 'critcareno', 'strk_unitno', 'genwardno', 'adjudicated', 'sevendaycase',
                      'final_status', 'sich7', 'dead7', 'myocard_infarct', 'extracranial_bleed',
                      'allergic_reaction', 'other_effect', 'adverse_reaction', 'gcs_eye_7',
                      'gcs_motor_7', 'gcs_verbal_7', 'liftarms_7', 'ablewalk_7', 'indepinadl_7',
                      'destination', 'other_effect_code', 'event_days'],
    'six_months_var': ['konprob', 'recsix', 'sixmonthform', 'sixcompleted_by', 'ohs6', 'ordinal6',
                       'aliveind6', 'alivefav6', 'dead6mo', 'imputed6', 'aspirin6', 'bloodthin6',
                       'clotbust6', 'stocking6', 'gotprobs6', 'needhelp6', 'walkhelp6', 'speakprob6',
                       'mobility6', 'selfcare6', 'activities6', 'pain6', 'anxiety6', 'wherelive6',
                       'howlive6', 'euroqol6', 'deadordep6', 'missing6', 'surv6', 'censor6',
                       'disab_unknown6', 'vital_and_disabunknown6'],
    'eighteen_months_var': ['receighteen', 'eighteenmonthform', 'eighteencompleted_by', 'aspirin18',
                            'bloodthin18', 'clotbust18', 'stocking18', 'gotprobs18', 'needhelp18',
                            'walkhelp18', 'speakprob18', 'mobility18', 'selfcare18', 'activities18',
                            'pain18', 'anxiety18', 'wherelive18', 'howlive18', 'euroqol18',
                            'deadordep18', 'ohs18', 'ordinal18', 'aliveind18', 'alivefav18',
                            'yrfu_code', 'missing18', 'censor18', 'surv18', 'plan18', 'disab_unknown18',
                            'vital_and_disabunknown18'],
    'r_scan_var': ['recR', 'R_scantype', 'R_scannorm', 'waiver_code', 'extracranial_bleed_site',
                   'R_acuteic', 'hypodeg', 'hypodegsite', 'mca', 'affmca', 'aspcau', 'asplen',
                   'aspins', 'aspint', 'aspm1', 'aspm2', 'aspm3', 'aspm4', 'aspm5', 'aspm6', 'oial',
                   'aca', 'pca', 'subinf', 'cbzinf', 'cinf', 'stem', 'tisswell', 'hdart1', 'hdart2',
                   'hdart3', 'hdart4', 'hdart5', 'hdart6', 'hdart7', 'seclesion', 'redbtvola',
                   'redbtvolb', 'wmla', 'wmlp', 'oldlesion', 'oldlesion1', 'oldlesion2', 'oldlesion3',
                   'oldlesion4', 'oldlesion5', 'oldlesion6', 'nslesion', 'nslesion1', 'nslesion2',
                   'nslesion3', 'nslesion4', 'nslesion5', 'scanqual', 'R_infarct_size', 'apca',
                   'subinf1', 'cbzinf1', 'cinf1', 'stem1', 'aca1', 'pca1', 'R_infarct_territory',
                   'R_hypodensity', 'R_swelling', 'R_hyperdense_arteries', 'R_atrophy', 'R_whitematter',
                   'R_oldlesion', 'R_nonstroke_lesion', 'R_isch_change', 'R_mca_aspects',
                   'R_tot_aspects', 'R_hyperdensity', 'vis_infarct'],
    'p_scan_var': ['recP', 'P_scantype', 'P_scannorm'],
    'death_var': ['deathcode', 'deathdate_unknown'],
}
#import data source
df = pd.read_sas(r"G:\My Drive\Portfolio\ISTD_v3_20260111\datashare_aug2015.sas7bdat",
                 encoding='utf-8')
#export raw dataset
if export_data:
    df.to_csv(r"G:\My Drive\Portfolio\ISTD_v3_20260111\datashare_aug2015.csv",
              index=False)
#summarise entries of variables
unique_df = pd.DataFrame(columns=df.columns)
for col in df.columns:
    unique_df[col] = df[col].drop_duplicates(ignore_index=True).sort_values(ignore_index=True)
if export_data:
    unique_df.to_csv(r"G:\My Drive\Portfolio\ISTD_v3_20260111\datashare_aug2015_unique.csv",
                     index=False)
#format data
df['age'] = df['age'].round()
#plot distribution of data (TBC)
if export_img:
    if not os.path.exists(r"G:\My Drive\Portfolio\ISTD_v3_20260111\distribution_plot"):
        os.makedirs(r"G:\My Drive\Portfolio\ISTD_v3_20260111\distribution_plot")
    for col in df.columns:
        plt.hist(df[col])
        plt.title(col)
        plt.savefig(r"G:\My Drive\Portfolio\ISTD_v3_20260111\distribution_plot\%s.png" %col)
        plt.close()
#supervised learning
target_variable = 'dead7'
drop_variables = ['randhosp_id', 'randpat_id', 'pretrialexp', 'country', 'trialphase', 'phase',
                 'gender', 'weight', 'glucose', 'agecat', 'ageimp', 'age_true', 'UKextra', 'age',
                 'randyear', 'randmonth', 'randhour', 'randmin', 'randdelay', 'livealone_rand',
                 'indepinadl_rand', 'nobleed_rand', 'infarct', 'antiplat_rand', 'atrialfib_rand',
                 'sbprand', 'dbprand', 'gcs_eye_rand', 'gcs_motor_rand', 'gcs_verbal_rand',
                 'gcs_score_rand', 'nihss', 'liftarms_rand', 'ablewalk_rand', 'weakface_rand',
                 'weakarm_rand', 'weakleg_rand', 'dysphasia_rand', 'hemianopia_rand', 'visuospat_rand',
                 'brainstemsigns_rand', 'otherdeficit_rand', 'stroketype', 'pred_nihss',
                 'randvioltype', 'sbpstart', 'sbp30min', 'sbp60min', 'sbp24h', 'dbpstart', 'dbp30min',
                 'dbp60min', 'dbp24h', 'treatdelay', 'itt_treat', 'recinfus', 'gotbolus', 'infus_start',
                 'infus_halt', 'totdose', 'nostartcode', 'treatment', 'haltcode', 'other_antiplat_pre',
                 'anticoag_pre', 'asl', 'rec7', 'consent_type', 'aspirin_pre', 'dipyridamole_pre',
                 'clopidogrel_pre', 'lowdose_heparin_pre', 'fulldose_heparin_pre', 'warfarin_pre',
                 'antithromb_pre', 'hypertension_pre', 'diabetes_pre', 'stroke_pre', 'aspirin_day1',
                  'antiplatelet_day1', 'lowdose_heparin_day1', 'full_anticoag_day1', 'lowerBP_day1',
                  'nontrial_thromb_day1', 'iv_fluids_day1', 'insulin_day1', 'aspirin_days2to7',
                  'antiplatelet_days2to7', 'lowdose_heparin_days2to7', 'full_anticoag_days2to7',
                  'lowerBP_days2to7', 'nontrial_thromb_days2to7', 'nasogastric_days2to7',
                  'antibiotics_days2to7', 'findiag7', 'brainsite7', 'haem_type7', 'nonstroke_type7',
                  'med_adno', 'critcareno', 'strk_unitno', 'genwardno', 'adjudicated', 'sevendaycase',
                  'final_status', 'sich7', 'dead7', 'myocard_infarct', 'extracranial_bleed',
                  'allergic_reaction', 'other_effect', 'adverse_reaction', 'gcs_eye_7', 'gcs_motor_7',
                  'gcs_verbal_7', 'liftarms_7', 'ablewalk_7', 'indepinadl_7', 'destination',
                  'other_effect_code', 'event_days', 'konprob', 'recsix', 'sixmonthform',
                  'sixcompleted_by', 'ohs6', 'ordinal6',  'aliveind6', 'alivefav6', 'dead6mo',
                  'imputed6', 'aspirin6', 'bloodthin6',  'clotbust6', 'stocking6', 'gotprobs6',
                  'needhelp6', 'walkhelp6', 'speakprob6',  'mobility6', 'selfcare6', 'activities6',
                  'pain6', 'anxiety6', 'wherelive6',  'howlive6', 'euroqol6', 'deadordep6', 'missing6',
                  'surv6', 'censor6',  'disab_unknown6', 'vital_and_disabunknown6', 'receighteen',
                  'eighteenmonthform', 'eighteencompleted_by', 'aspirin18',   'bloodthin18',
                  'clotbust18', 'stocking18', 'gotprobs18', 'needhelp18',   'walkhelp18', 'speakprob18',
                  'mobility18', 'selfcare18', 'activities18',   'pain18', 'anxiety18', 'wherelive18',
                  'howlive18', 'euroqol18',   'deadordep18', 'ohs18', 'ordinal18', 'aliveind18',
                  'alivefav18',   'yrfu_code', 'missing18', 'censor18', 'surv18', 'plan18',
                  'disab_unknown18', 'vital_and_disabunknown18', 'recR', 'R_scantype', 'R_scannorm',
                  'waiver_code', 'extracranial_bleed_site', 'R_acuteic', 'hypodeg', 'hypodegsite',
                  'mca', 'affmca', 'aspcau', 'asplen', 'aspins', 'aspint', 'aspm1', 'aspm2', 'aspm3',
                  'aspm4', 'aspm5', 'aspm6', 'oial', 'aca', 'pca', 'subinf', 'cbzinf', 'cinf', 'stem',
                  'tisswell', 'hdart1', 'hdart2', 'hdart3', 'hdart4', 'hdart5', 'hdart6', 'hdart7',
                  'seclesion', 'redbtvola', 'redbtvolb', 'wmla', 'wmlp', 'oldlesion', 'oldlesion1',
                  'oldlesion2', 'oldlesion3', 'oldlesion4', 'oldlesion5', 'oldlesion6', 'nslesion',
                  'nslesion1', 'nslesion2', 'nslesion3', 'nslesion4', 'nslesion5', 'scanqual',
                  'R_infarct_size', 'apca', 'subinf1', 'cbzinf1', 'cinf1', 'stem1', 'aca1', 'pca1',
                  'R_infarct_territory', 'R_hypodensity', 'R_swelling', 'R_hyperdense_arteries',
                  'R_atrophy', 'R_whitematter', 'R_oldlesion', 'R_nonstroke_lesion', 'R_isch_change',
                  'R_mca_aspects', 'R_tot_aspects', 'R_hyperdensity', 'vis_infarct', 'recP',
                  'P_scantype', 'P_scannorm', 'deathcode', 'deathdate_unknown']


breakpoint()