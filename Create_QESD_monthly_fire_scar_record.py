#!/usr/bin/env python
#import packages for Python 3
import requests
import argparse
import json

# Put the details of the template xml file into a dictionary. 
# From the input arguments the month and year will be changed to reflect the current dataset to be created.
# Maybe down the track, modify this script to read template dictionary from an input file.
templateDict = {
        "acknowledgements": "",
        "additional_info": "[\"Fire scars were automatically detected in Sentinel-2 imagery using differenced bare soil fraction values obtained using the Joint Remote Sensing Research Program’s (JRSRP) fractional cover model. A Sentinel-2 pixel is identified as likely burnt if there has been a significant increment in bare soil fraction relative to the previous fractional cover values. Once areas of likely change are detected, a region growing algorithm is applied to expand the area to capture the whole fire event. Areas are then filtered into burnt and unburnt classes using a decision tree analysis. Subsequent manual interpretation is used to delineate between false positives and true positives.\\nCompleteness (omission):\\n\\nThe Sentinel-2 fire scars product has been validated using 480,000 independent observations selected from a range of environments and periods within the fire season across Queensland. The validation result showed that a high proportion of burned area was correctly classified (f1score = 0.91) with commission and omission error of 13% and 8% respectively. The omission error does not include burned area missed because of missing data (e.g. long periods without cloud-free images) due to the lack of an independent validation data set.\\n\\nThe manual editing applied to the 2020 fire scar product should significantly reduce the number of missed fires, although this has not been quantified.\\nConsistency (conceptual):\\n\\nSentinel-2 analysis does not provide a complete record of fire history for this period. Fire scars may be missed or under-mapped due to:\\n- Lack of visibility due to cloud, haze and smoke, and cloud shadow;\\n- Misclassification as non-fire related change or cloud shadow;\\n- Lack of detection due to size or patchiness. Fire scars smaller than 2 ha may not be included;\\n- Lack of detection due to rapid regrowth of vegetation. This is particularly an issue when there have been multiple cloud-affected images in the time series;\\n- Lack of detection for cool grass/understorey fires, obscured by unburnt vegetation;\\n- Lack of detection in the nominated month due to satellite images downloaded to RSC's imagery storage later than expected;\\n\\nFalse burned areas or over-mapping may result from:\\n- Omission errors in the cloud/shadow masks, where cloud is classified as fire scar;\\n- Areas of high intensity land-use change where the extent of bare ground increases rapidly (e.g cropping, vegetation clearing);\\n- Areas of inundation (e.g tidal flats, wetlands, ephemeral lakes and channels).\\nPositional accuracy (external, absolute):\\n\\nAll the data described here has been generated from the analysis of Sentinel-2 data acquired as orthorectified images from the European Space Agency. Sentinel-2 imagery has band-dependent spatial resolutions of 10m and 20m. In-house analysis of Sentinel-2 image-to-image registration showed that in over 90% of image pairs, the geometric error was less than 10m.\\nAttribute accuracy (non quantitative):\\n\\nFire scars may persist and continue to be visible for several months in the image time sequence. Where there has been fire scar persistence for a given pixel within the compositing period, the earliest date of detection is recorded.\"]",
        "author": None,
        "author_email": None,
        "cited_in": "",
        "classification": "[\"https://linked.data.gov.au/def/resource-types/Dataset\"]",
        "classification_and_access_restrictions": "[\"https://linked.data.gov.au/def/qg-security-classifications/official-public\"]",
        "conforms_to": "",
        "contact_creator": "Dan Tindall - Science Leader",
        "contact_point": "76007888",
        "contact_publisher": "https://linked.data.gov.au/def/qg-agent/DES",
        "creator_user_id": "9641ffbb-ae5b-4829-94f6-cb328d1049dd",
        "data_quality_standard": "{\"calculated_quality_measure\":0,\"accessibility\":{\"score\":0,\"accessibility_links_to_data_and_context\":0,\"non_proprietary_format\":0,\"open_license\":0,\"open_standards\":0,\"structured_data\":0},\"accuracy\":{\"score\":0,\"data_assurance\":0,\"data_complete\":0,\"data_met_needs_of_primary_user\":0,\"no_changes_or_flaws_not_explained\":0,\"revised_when_errors_detected\":0},\"coherence\":{\"score\":0,\"consistent_methodology\":0,\"consistent_over_time\":0,\"consistent_with_related_datasets\":0,\"elements_can_be_compared\":0,\"consistent_data_collection_frequency\":0},\"institutional_environment\":{\"score\":0,\"authorized_data_collection\":0,\"custodian\":0,\"data_quality_framework\":0,\"governance_roles\":0,\"no_commercial_interest_or_conflict\":0},\"interpretability\":{\"score\":0,\"accuracy_evaluation\":0,\"concept_explanations\":0,\"data_dictionary_provided\":0,\"data_sources_and_methods\":0,\"technical_explanations\":0}}",
        "dataset_language": "[\"https://linked.data.gov.au/def/iso639-1/en\"]",
        "dataset_release_date": "2022-mmmm-01T00:00:00",
        "identifiers": "",
        "isopen": False,
        "landing_page": "https://qldspatial.information.qld.gov.au/catalogue/custom/detail.page?fid={BBF9AFE0-3858-4241-9C09-B1D0F39CFB6E}",
        "license_id": "https://linked.data.gov.au/def/qld-data-licenses/cc-by-4.0",
        "license_title": "https://linked.data.gov.au/def/qld-data-licenses/cc-by-4.0",
        "lineage_description": "Lineage statement:\r\nThe YYYY fire scar product was produced via five main steps:\r\n\r\n1. Conduct pre-processing of Sentinel-2 imagery to convert to surface reflectance, and screen out cloud and cloud shadow, topographic shadow, cropping lands and water.\r\n\r\n2. Apply fractional cover algorithm. Fractional cover is a per-pixel quantitative estimation of the photosynthetic vegetation, non-photosynthetic vegetation and bare soil cover fractions.\r\n\r\n3. Apply RapidFire algorithm:\r\n- Identify core pixels of potentially burned area, based on the temporal difference in bare soil cover fraction. Core pixels are spatial clusters (bigger than 15 pixels) where the change in bare cover fraction exceeds an optimised threshold.\r\n- Expand the extent of the pixels classified as potentially burned, using a region growing algorithm on the core pixels.\r\n- Use object-oriented classification to discriminate between burned and unburned areas. The classification tree was based on the median values of the temporal difference of NBR (dNBR) and NIR + IR (dNIRIR) of each potentially burned area.\r\n\r\n4. Conduct manual editing by trained analysts to reduce the number of false fires and omission errors.\r\n\r\n5. Mosaic individual scenes to form a monthly composite product for Queensland.\r\n\r\n\r\nThis approach has some important consequences:\r\n- Not all the pixels of an image are analysed due to cloud and shadow effects;\r\n- Time elapsed between observations for different pixels of the same image may differ, again due to cloud and shadow effects over time; and\r\n- Burned areas only appear once in the record. If for some reason a burned area is missed in the first unmasked observation it will be missed in the whole record.\r\n- Sometimes a burnt area may appear in a later mapping month. Satellite images downloaded to RSC's imagery storage can occur out of expected order.\r\n\r\n\r\nThis new method is a different approach from the previous Landsat-derived fire scar mapping program (1987-2016). That automated time series method identified large negative outliers in reflectance indices (based on NIR and SWIR1 bands) relative to the time series.\r\nProcess step:\r\nReferences:\r\n\r\nBastarrika, A.; Chuvieco, E.; Martín, M. P., 2011. Mapping burned areas from landsat tm/etm+ data with a two-phase algorithm: Balancing omission and commission errors. Remote Sensing of Environment., 115, 1003–1012.\r\n\r\nGoodwin, N. R.; Collett, L. J., 2014. Development of an automated method for mapping fire history\r\ncaptured in Landsat TM and ETM+ time series across Queensland, Australia. Remote Sensing of Environment., 148, 206–221.\r\n\r\nGuerschman, J. P.; Oyarzábal, M.; Malthus, T.; McVicar, T. R.; Byrne, G.; Randall, L.; Stewart, J., 2012. Evaluation of the MODIS-based vegetation fractional cover product. CSIRO., 31.",
        "lineage_inputs": "",
        "lineage_plan": "",
        "lineage_responsible_party": "[\"Deanna Vandenberg - Principal Scientist (Remote Sensing)\"]",
        "lineage_sensor": "[\"https://sentinel.esa.int/web/sentinel/missions/sentinel-2\"]",
        "maintainer": None,
        "maintainer_email": None,
        "metadata_contact_point": "71590218",
        "metadata_created": "",
        "metadata_modified": "",
        "metadata_review_date": "",
        "name": "sentinel-2-queensland-fire-scars-mmmm-YYYY",
        "notes": "This dataset is a statewide monthly composite of fire scars (burnt area) derived from all available Sentinel-2 images acquired over Queensland within the month identified in the name of this file. Fire scars have been mapped using an automated change detection method, with supplementary manual interpretation. This data contains both automated and manually edited data.1: burnt area detected. 0: NULL/not burnt.\r\nFor more information go to the Department website https://www.qld.gov.au/environment/land/management/mapping/statewide-monitoring/firescar.",
        "num_resources": 1,
        "num_tags": 3,
        "organization": {
            "id": "b71e4ecf-0a66-4e27-b8d8-b99b681291a4",
            "name": "department-of-environment-and-science",
            "title": "Department of Environment and Science",
            "type": "organization",
            "description": "",
            "image_url": "2021-07-01-005831.096785topic-5.png",
            "created": "2021-06-03T00:07:31.677442",
            "is_organization": True,
            "approval_status": "approved",
            "state": "active"
        },
        "owner_org": "b71e4ecf-0a66-4e27-b8d8-b99b681291a4",
        "private": False,
        "publication_status": "http://def.isotc211.org/iso19115/-1/2014/IdentificationInformation/code/MD_ProgressCode/completed",
        "purpose": "This state-wide composite of fire scars (burnt areas) is to provide regular monitoring and mapping of fire scars across Queensland, useful for managing natural resources, assessing fire hazard and risk, understanding the impacts of fire on grazing production and monitoring ecological impacts over time.",
        "rights_statement": "© State of Queensland (Department of Environment and Science) YYYY",
        "spatial": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        137.134557,
                        -10.676968
                    ],
                    [
                        153.911426,
                        -10.676968
                    ],
                    [
                        153.911426,
                        -29.162078
                    ],
                    [
                        137.134557,
                        -29.162078
                    ],
                    [
                        137.134557,
                        -10.676968
                    ]
                ]
            ]
        },
        "spatial_centroid": "",
        "spatial_content_resolution": "10",
        "spatial_datum_crs": "http://linked.data.gov.au/def/queensland-crs/gda1994",
        "spatial_geometry": "",
        "spatial_lower_left": "{\"type\":\"Point\",\"coordinates\":[137.1345572332344,-29.162077963363714]}",
        "spatial_name_code": "",
        "spatial_representation": "http://def.isotc211.org/iso19115/-1/2014/IdentificationInformation/code/MD_SpatialRepresentationTypeCode/grid",
        "spatial_resolution": "https://gcmd.earthdata.nasa.gov/kms/concept/abf43d91-a65d-4b3b-a6dd-593e211b2c7b",
        "spatial_upper_right": "{\"type\":\"Point\",\"coordinates\":[153.91142614303268,-10.676967563393484]}",
        "specialized_license": "",
        "state": "active",
        "temporal_end": "YYYY-mmmm-31",
        "temporal_precision_spacing": "P1M",
        "temporal_resolution_range": "https://gcmd.earthdata.nasa.gov/kms/concept/7b2a303c-3cb7-4961-9851-650548964674",
        "temporal_start": "YYYY-mmmm-01",
        "title": "Sentinel-2 Queensland Fire Scars MMMM YYYY",
        "topic": "[\"https://gcmd.earthdata.nasa.gov/kms/concept/e6f1ee58-fb71-42dd-b071-c1637da7e51f\",\"https://gcmd.earthdata.nasa.gov/kms/concept/c9ba3275-2fe3-4619-b7c0-881d4f6fa34e\"]",
        "type": "dataset",
        "update_schedule": "http://def.isotc211.org/iso19115/-1/2014/MaintenanceInformation/code/MD_MaintenanceFrequencyCode/asNeeded",
        "url": "",
        "version": None,
        "relationships_as_subject": [
            {
                "__extras": {
                    "subject_package_id": "",
                    "object_package_id": "1e088065-b364-4881-95cc-80998064ffec"
                },
                "id": "5a43fc5c-e421-4629-afbd-792bb75af6c8",
                "type": "Is Part Of"
            }
        ],
        "resources": [
            {
                "additional_info": "",
                "additional_info[0][]": "",
                "cache_last_updated": None,
                "cache_url": None,
                "compression": "http://publications.europa.eu/resource/authority/file-type/ZIP",
                "data_services[0][]": "",
                "description": "Fire scar mapping derived from Sentinel-2 imagery.",
                "format": "http://publications.europa.eu/resource/authority/file-type/TIFF",
                "hash": "",
                "id": "",
                "last_modified": None,
                "license": "http://linked.data.gov.au/def/licence-document/cc-by-4.0",
                "mimetype": None,
                "mimetype_inner": None,
                "name": "Fire Scar (Burnt Area) Mapping, MMMM YYYY",
                "package_id": "",
                "packaging": "http://publications.europa.eu/resource/authority/file-type/ZIP",
                "position": 0,
                "resource_type": None,
                "rights_statement": "© State of Queensland (Department of Environment and Science) 2022",
                "schema_standards": "",
                "schema_standards[0][]": "",
                "service_api_endpoint": "",
                "service_api_endpoint[0][]": "",
                "size": 50000,
                "state": "active",
                "token": "cbe49650e1a56f62510d79be7cc07b93b09a766f9dedd383ccf3ef1bd0afd18e",
				"url": "https://qldspatial.information.qld.gov.au/catalogue/custom/detail.page?fid={to be updated}",
                "url_type": None
            }
        ],
        "tags": [
            {
                "display_name": "burnt area",
                "id": "1caf3692-3ff2-4cd4-a1ac-e7dabc217c4c",
                "name": "burnt area",
                "state": "active",
                "vocabulary_id": None
            },
            {
                "display_name": "fire extent",
                "id": "f45b9b09-d10e-4143-82d6-6478cd645bbd",
                "name": "fire extent",
                "state": "active",
                "vocabulary_id": None
            },
            {
                "display_name": "wildfire",
                "id": "f0701090-7264-4149-91f9-98c73a70bd02",
                "name": "wildfire",
                "state": "active",
                "vocabulary_id": None
            }
        ],
        "groups": [],
        "relationships_as_object": []
}
#Get arguments for Year and Month from the user
def getCmdargs():
    """
    Get commandline arguments.
    """
    p = argparse.ArgumentParser()
    p.add_argument("-y", "--Year",
        help="Enter year fire scar mapping eg. 2022")
    p.add_argument("-m", "--Month",
        help="Enter month fire scar mapping eg. October")
    p.add_argument(
        "--debug", required=False, default=False, action="store_true",
        help="Do not remove tmp files after")
    cmdargs = p.parse_args()
    return cmdargs

def switch(month):
    try:
        return {
            "January": "01",
            "February": "02",
            "March": "03",
            "April": "04",
            "May": "05",
            "June": "06",
            "July": "07",
            "August": "08",
            "September": "09",
            "October": "10",
            "November": "11",
            "December": "12",
        }[month]
    except:
        return 0


def update_dictionary(targetDict, data, depth):

    key = []
    found = False
    
    for key in targetDict:
        
        entry = targetDict[key]

        if isinstance(entry, str):
            
            if entry.find("YYYY") > -1:
                print("found YYYY at depth: ", str(depth))
                entry = entry.replace("YYYY", data[0])
                found = True
     
            if entry.find("MMMM") > -1:
                print("found MMMM at depth: ", str(depth))
                entry = entry.replace("MMMM", data[1])
                found = True
                
            if entry.find("mmmm") > -1:
                print("found mmmm at depth: ", str(depth))
                entry = entry.replace("mmmm", data[2])
                found = True

            if found:
                #print(entry)
                found = False

        elif isinstance(entry, dict):
            update_dictionary(entry, data, depth + 1)

        elif isinstance(entry, list):
            for i in entry:
                if isinstance(i, dict):
                    update_dictionary(i, data, depth + 1)
                
        targetDict[key] = entry
        

            
def main(year, month):
    
    monthNum = switch(month)
    data = [year, month, monthNum]
    update_dictionary(templateDict, data, 0)
    # Use the json module to dump the dictionary to a string for posting.
    #data_string = urllib.quote(json.dumps(template_dict))

    # Setup the package_create function to create a new dataset.
    #request = urllib2.Request('http://qesdtst.des.qld.gov.au/api/action/package_create')
    API_ENDPOINT = ('http://qesdtst.des.qld.gov.au/api/action/package_create')

    # Include the authorization key for the user account on the CKAN site
    API_KEY = 'xxxx'

    # Convert template dictionary to a string using json module, although the data function should be able to do the conversion
    # params = json.dumps(templateDict)
    
    #Make the HTTP request.
    #response = urllib2.urlopen(request, data_string)
    response = requests.post(url = API_ENDPOINT, headers = {'Authorization' : API_KEY}, data = templateDict)
    print(response.text)
    

if __name__ == "__main__":
    cmdargs = getCmdargs()
    main(cmdargs.Year, cmdargs.Month)



