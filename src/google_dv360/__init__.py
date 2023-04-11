from .client import GoogleDV360Client, GoogleDV360ClientException  # noqa F401

_filter_table = {
    "FILTER_ACTIVE_VIEW_CUSTOM_METRIC_ID": "Active View: Custom Metric ID",
    "FILTER_ACTIVE_VIEW_CUSTOM_METRIC_NAME": "Active View: Custom Metric Name",
    "FILTER_ACTIVE_VIEW_EXPECTED_VIEWABILITY": "Active View Expected Viewability",
    "FILTER_ADVERTISER": "Advertiser ID",
    "FILTER_ADVERTISER_CURRENCY": "Advertiser Currency",
    "FILTER_ADVERTISER_INTEGRATION_CODE": "Advertiser Integration Code",
    "FILTER_ADVERTISER_INTEGRATION_STATUS": "Advertiser Status",
    "FILTER_ADVERTISER_NAME": "Advertiser",
    "FILTER_ADVERTISER_TIMEZONE": "Advertiser Time Zone",
    "FILTER_AD_POSITION": "Ad Position",
    "FILTER_AD_TYPE": "Ad Type",
    "FILTER_AGE": "Age",
    "FILTER_ALGORITHM": "Algorithm",
    "FILTER_ALGORITHM_ID": "Algorithm ID",
    "FILTER_AMP_PAGE_REQUEST": "AMP Page Request",
    "FILTER_ANONYMOUS_INVENTORY_MODELING": "Anonymous Inventory Modeling",
    "FILTER_APP_URL": "App/URL",
    "FILTER_APP_URL_EXCLUDED": "App/URL Excluded",
    "FILTER_ATTRIBUTED_USERLIST": "Attributed Userlist",
    "FILTER_ATTRIBUTED_USERLIST_COST": "Attributed Userlist Cost",
    "FILTER_ATTRIBUTED_USERLIST_TYPE": "Attributed Userlist Type",
    "FILTER_ATTRIBUTION_MODEL": "Attribution Model",
    "FILTER_AUDIENCE_LIST": "Audience List",
    "FILTER_AUDIENCE_LIST_COST": "Audience List Cost",
    "FILTER_AUDIENCE_LIST_TYPE": "Audience List Type",
    "FILTER_AUDIENCE_NAME": "Audience Name",
    "FILTER_AUDIENCE_TYPE": "Audience Type",
    "FILTER_AUDIO_FEED_TYPE_NAME": "Audio Feed Type",
    "FILTER_AUTHORIZED_SELLER_STATE": "Authorized Seller State",
    "FILTER_BILLABLE_OUTCOME": "Billable Outcome",
    "FILTER_BRAND_LIFT_TYPE": "Brand Lift Type",
    "FILTER_BROWSER": "Browser",
    "FILTER_BUDGET_SEGMENT_BUDGET": "Budget Segment Budget",
    "FILTER_BUDGET_SEGMENT_DESCRIPTION": "Budget Segment Name",
    "FILTER_BUDGET_SEGMENT_END_DATE": "Budget Segment End Date",
    "FILTER_BUDGET_SEGMENT_PACING_PERCENTAGE": "Budget Segment Pacing Percentage",
    "FILTER_BUDGET_SEGMENT_START_DATE": "Budget Segment Start Date",
    "FILTER_BUDGET_SEGMENT_TYPE": "Budget Type (Segment)",
    "FILTER_CAMPAIGN_DAILY_FREQUENCY": "Insertion Order Daily Frequency",
    "FILTER_CARRIER": "ISP or Carrier ID",
    "FILTER_CARRIER_NAME": "ISP or Carrier",
    "FILTER_CHANNEL_GROUPING": "Channel Grouping",
    "FILTER_CHANNEL_ID": "Channel ID",
    "FILTER_CHANNEL_NAME": "Channel",
    "FILTER_CHANNEL_TYPE": "Channel Type",
    "FILTER_CITY": "City ID",
    "FILTER_CITY_NAME": "City",
    "FILTER_CM360_PLACEMENT_ID": "CM360 Placement ID",
    "FILTER_COMPANION_CREATIVE_ID": "Companion Creative ID",
    "FILTER_COMPANION_CREATIVE_NAME": "Companion Creative",
    "FILTER_CONVERSION_AD_EVENT_TYPE": "Conversion Ad Event Type",
    "FILTER_CONVERSION_AD_EVENT_TYPE_ID": "Conversion Ad Event Type ID",
    "FILTER_CONVERSION_DELAY": "Time to Conversion",
    "FILTER_CONVERSION_SOURCE": "Conversion Source",
    "FILTER_CONVERSION_SOURCE_ID": "Conversion Source ID",
    "FILTER_COUNTRY": "Country",
    "FILTER_COUNTRY_ID": "Country",
    "FILTER_CREATIVE": "Creative",
    "FILTER_CREATIVE_ASSET": "Creative Asset",
    "FILTER_CREATIVE_ATTRIBUTE": "Creative Attributes",
    "FILTER_CREATIVE_HEIGHT": "Creative Height",
    "FILTER_CREATIVE_ID": "Creative ID",
    "FILTER_CREATIVE_INTEGRATION_CODE": "Creative Integration Code",
    "FILTER_CREATIVE_RENDERED_IN_AMP": "Creative Rendered in AMP",
    "FILTER_CREATIVE_SIZE": "Creative Size",
    "FILTER_CREATIVE_SOURCE": "Creative Source",
    "FILTER_CREATIVE_STATUS": "Creative Status",
    "FILTER_CREATIVE_TYPE": "Creative Type",
    "FILTER_CREATIVE_WIDTH": "Creative Width",
    "FILTER_DATA_PROVIDER": "Data Provider ID",
    "FILTER_DATA_PROVIDER_NAME": "Data Provider",
    "FILTER_DATA_SOURCE": "Data Source",
    "FILTER_DATE": "Date",
    "FILTER_DAY_OF_WEEK": "Day of Week",
    "FILTER_DETAILED_DEMOGRAPHICS": "Detailed Demographics",
    "FILTER_DETAILED_DEMOGRAPHICS_ID": "Detailed Demographics ID",
    "FILTER_DEVICE": "Device",
    "FILTER_DEVICE_MAKE": "Device Make",
    "FILTER_DEVICE_MODEL": "Device Model",
    "FILTER_DEVICE_TYPE": "Device Type",
    "FILTER_DFP_ORDER_ID": "DFP Insertion Order ID",
    "FILTER_DIGITAL_CONTENT_LABEL": "Digital Content Label",
    "FILTER_DMA": "DMA Code",
    "FILTER_DMA_NAME": "DMA",
    "FILTER_DOMAIN": "Domain",
    "FILTER_ELIGIBLE_COOKIES_ON_FIRST_PARTY_AUDIENCE_LIST": "Eligible Cookies on First-Party Audience List",
    "FILTER_ELIGIBLE_COOKIES_ON_THIRD_PARTY_AUDIENCE_LIST_AND_INTEREST":
        "Eligible Cookies on Third-Party Audience List and Interest",
    "FILTER_EVENT_TYPE": "Event Type",
    "FILTER_EXCHANGE": "Exchange",
    "FILTER_EXCHANGE_CODE": "Exchange Code",
    "FILTER_EXCHANGE_ID": "Exchange ID",
    "FILTER_EXTENSION": "Asset",
    "FILTER_EXTENSION_ASSET": "Asset (upgraded)",
    "FILTER_EXTENSION_ASSET_STATUS": "Asset Status (upgraded)",
    "FILTER_EXTENSION_ASSET_TYPE": "Asset Type (upgraded)",
    "FILTER_EXTENSION_STATUS": "Asset Status",
    "FILTER_EXTENSION_TYPE": "Asset Type",
    "FILTER_FIRST_PARTY_AUDIENCE_LIST_COST": "First Party Audience List Cost",
    "FILTER_FIRST_PARTY_AUDIENCE_LIST_TYPE": "First Party Audience List Type",
    "FILTER_FLOODLIGHT_ACTIVITY": "Floodlight Activity",
    "FILTER_FLOODLIGHT_ACTIVITY_ID": "Floodlight Activity ID",
    "FILTER_FORMAT": "Format",
    "FILTER_GAM_INSERTION_ORDER": "DFP Insertion Order",
    "FILTER_GAM_LINE_ITEM": "DFP Line Item",
    "FILTER_GAM_LINE_ITEM_ID": "DFP Line Item ID",
    "FILTER_GENDER": "Gender",
    "FILTER_GMAIL_AGE": "Age",
    "FILTER_GMAIL_CITY": "City",
    "FILTER_GMAIL_COUNTRY": "Country",
    "FILTER_GMAIL_COUNTRY_NAME": "Country",
    "FILTER_GMAIL_DEVICE_TYPE": "Device Type",
    "FILTER_GMAIL_DEVICE_TYPE_NAME": "Device Type",
    "FILTER_GMAIL_GENDER": "Gender",
    "FILTER_GMAIL_REGION": "Region",
    "FILTER_GMAIL_REMARKETING_LIST": "Remarketing List",
    "FILTER_HOUSEHOLD_INCOME": "Household Income",
    "FILTER_IMPRESSION_COUNTING_METHOD": "Impression Counting Method",
    "FILTER_IMPRESSION_LOSS_REJECTION_REASON": "Rejection Reason",
    "FILTER_INSERTION_ORDER": "Insertion Order ID",
    "FILTER_INSERTION_ORDER_GOAL_TYPE": "Insertion Order Goal Type",
    "FILTER_INSERTION_ORDER_GOAL_VALUE": "Insertion Order Goal Value",
    "FILTER_INSERTION_ORDER_INTEGRATION_CODE": "Insertion Order Integration Code",
    "FILTER_INSERTION_ORDER_NAME": "Insertion Order",
    "FILTER_INSERTION_ORDER_STATUS": "Insertion Order Status",
    "FILTER_INTEREST": "Interest",
    "FILTER_INVENTORY_COMMITMENT_TYPE": "Inventory Commitment Type",
    "FILTER_INVENTORY_DELIVERY_METHOD": "Inventory Delivery Method",
    "FILTER_INVENTORY_FORMAT": "Format",
    "FILTER_INVENTORY_MEDIA_COST_TYPE": "Inventory Media Cost Type",
    "FILTER_INVENTORY_RATE_TYPE": "Inventory Rate Type",
    "FILTER_INVENTORY_SOURCE": "Inventory Source ID (Legacy)",
    "FILTER_INVENTORY_SOURCE_EXTERNAL_ID": "Inventory Source ID (external)",
    "FILTER_INVENTORY_SOURCE_GROUP": "Inventory Source Group",
    "FILTER_INVENTORY_SOURCE_GROUP_ID": "Inventory Source Group ID",
    "FILTER_INVENTORY_SOURCE_ID": "Inventory Source ID",
    "FILTER_INVENTORY_SOURCE_NAME": "Inventory Source",
    "FILTER_INVENTORY_SOURCE_TYPE": "Inventory Source Type",
    "FILTER_KEYWORD": "Keyword",
    "FILTER_LIFE_EVENT": "Life Event",
    "FILTER_LIFE_EVENTS": "Life Events",
    "FILTER_LINE_ITEM": "Line Item ID",
    "FILTER_LINE_ITEM_BUDGET": "Line Item Budget",
    "FILTER_LINE_ITEM_DAILY_FREQUENCY": "Line Item Daily Frequency",
    "FILTER_LINE_ITEM_END_DATE": "Line Item End Date",
    "FILTER_LINE_ITEM_INTEGRATION_CODE": "Line Item Integration Code",
    "FILTER_LINE_ITEM_LIFETIME_FREQUENCY": "Line Item Lifetime Frequency",
    "FILTER_LINE_ITEM_NAME": "Line Item",
    "FILTER_LINE_ITEM_PACING_PERCENTAGE": "Line Item Pacing Percentage",
    "FILTER_LINE_ITEM_START_DATE": "Line Item Start Date",
    "FILTER_LINE_ITEM_STATUS": "Line Item Status",
    "FILTER_LINE_ITEM_TYPE": "Line Item Type",
    "FILTER_MATCHED_GENRE_TARGET": "Matched Genre Target",
    "FILTER_MATCH_RATIO": "Match Ratio",
    "FILTER_MEASUREMENT_SOURCE": "Measurement Source",
    "FILTER_MEDIA_PLAN": "Campaign ID",
    "FILTER_MEDIA_PLAN_NAME": "Campaign",
    "FILTER_MEDIA_TYPE": "Media Type",
    "FILTER_MOBILE_GEO": "Business Chain",
    "FILTER_MONTH": "Month",
    "FILTER_MRAID_SUPPORT": "MRAID Support",
    "FILTER_NIELSEN_AGE": "Age",
    "FILTER_NIELSEN_COUNTRY_CODE": "Country",
    "FILTER_NIELSEN_DATE_RANGE": "Date Range for Cumulative Metrics",
    "FILTER_NIELSEN_DEVICE_ID": "Device ID",
    "FILTER_NIELSEN_GENDER": "Gender",
    "FILTER_NIELSEN_RESTATEMENT_DATE": "Restatement Date",
    "FILTER_OMID_CAPABLE": "OM SDK Capable",
    "FILTER_OM_SDK_AVAILABLE": "OM SDK Available",
    "FILTER_ORDER_ID": "Order ID",
    "FILTER_OS": "Operating System",
    "FILTER_PAGE_CATEGORY": "Category",
    "FILTER_PAGE_LAYOUT": "Environment",
    "FILTER_PARENTAL_STATUS": "Parental Status",
    "FILTER_PARTNER": "Partner ID",
    "FILTER_PARTNER_CURRENCY": "Partner Currency",
    "FILTER_PARTNER_NAME": "Partner",
    "FILTER_PARTNER_STATUS": "Partner Status",
    "FILTER_PATH_EVENT_INDEX": "Path Event Index",
    "FILTER_PATH_PATTERN_ID": "Path Pattern ID",
    "FILTER_PLACEMENT_ALL_YOUTUBE_CHANNELS": "Placement (All YouTube Channels)",
    "FILTER_PLACEMENT_NAME_ALL_YOUTUBE_CHANNELS": "Placement Name (All YouTube Channels)",
    "FILTER_PLATFORM": "Platform",
    "FILTER_PLAYBACK_METHOD": "Playback Method",
    "FILTER_POSITION_IN_CONTENT": "Position in Content",
    "FILTER_PUBLIC_INVENTORY": "Public Inventory",
    "FILTER_PUBLISHER_PROPERTY": "Publisher Property",
    "FILTER_PUBLISHER_PROPERTY_ID": "Publisher Property ID",
    "FILTER_PUBLISHER_PROPERTY_SECTION": "Publisher Property Section",
    "FILTER_PUBLISHER_PROPERTY_SECTION_ID": "Publisher Property Section ID",
    "FILTER_PUBLISHER_TRAFFIC_SOURCE": "Publisher Traffic Source",
    "FILTER_QUARTER": "Quarter",
    "FILTER_REFRESHED_AD_NAME": "Refreshed Ad",
    "FILTER_REFUND_REASON": "Refund Reason",
    "FILTER_REGION": "Region ID",
    "FILTER_REGION_NAME": "Region",
    "FILTER_REMARKETING_LIST": "Remarketing List",
    "FILTER_REWARDED": "Rewarded",
    "FILTER_SENSITIVE_CATEGORY": "Sensitive Category",
    "FILTER_SERVED_PIXEL_DENSITY": "Served Pixel Density",
    "FILTER_SITE_ID": "App/URL ID",
    "FILTER_SITE_LANGUAGE": "Language",
    "FILTER_SKIPPABLE_SUPPORT": "Video Skippable Support",
    "FILTER_TARGETED_DATA_PROVIDERS": "Targeted Data Providers",
    "FILTER_TARGETED_USER_LIST": "Attributed Userlist ID",
    "FILTER_TARGETING_EXPANSION": "Targeting Expansion",
    "FILTER_THIRD_PARTY_AUDIENCE_LIST_COST": "Third Party Audience List Cost",
    "FILTER_THIRD_PARTY_AUDIENCE_LIST_TYPE": "Third Party Audience List Type",
    "FILTER_TIME_OF_DAY": "Time of Day",
    "FILTER_TRUEVIEW_AD": "YouTube Ad",
    "FILTER_TRUEVIEW_AD_GROUP": "YouTube Ad Group",
    "FILTER_TRUEVIEW_AD_GROUP_AD_ID": "YouTube Ad ID",
    "FILTER_TRUEVIEW_AD_GROUP_ID": "YouTube Ad Group ID",
    "FILTER_TRUEVIEW_AD_TYPE_NAME": "YouTube Ad Type",
    "FILTER_TRUEVIEW_AGE": "Age (YouTube)",
    "FILTER_TRUEVIEW_CATEGORY": "Category",
    "FILTER_TRUEVIEW_CITY": "City",
    "FILTER_TRUEVIEW_CLICK_TYPE_NAME": "Click Type",
    "FILTER_TRUEVIEW_CONVERSION_TYPE": "Conversion Type",
    "FILTER_TRUEVIEW_COUNTRY": "Country (YouTube)",
    "FILTER_TRUEVIEW_CUSTOM_AFFINITY": "Custom Affinity",
    "FILTER_TRUEVIEW_DETAILED_DEMOGRAPHICS": "Detailed Demographics",
    "FILTER_TRUEVIEW_DETAILED_DEMOGRAPHICS_ID": "Detailed Demographics ID",
    "FILTER_TRUEVIEW_DMA": "DMA ID",
    "FILTER_TRUEVIEW_DMA_NAME": "DMA",
    "FILTER_TRUEVIEW_GENDER": "Gender",
    "FILTER_TRUEVIEW_HOUSEHOLD_INCOME": "Household Income",
    "FILTER_TRUEVIEW_IAR_AGE": "Age",
    "FILTER_TRUEVIEW_IAR_CATEGORY": "Category",
    "FILTER_TRUEVIEW_IAR_CITY": "City",
    "FILTER_TRUEVIEW_IAR_COUNTRY": "Country",
    "FILTER_TRUEVIEW_IAR_COUNTRY_NAME": "Country",
    "FILTER_TRUEVIEW_IAR_GENDER": "Gender",
    "FILTER_TRUEVIEW_IAR_INTEREST": "Interest",
    "FILTER_TRUEVIEW_IAR_LANGUAGE": "Language",
    "FILTER_TRUEVIEW_IAR_PARENTAL_STATUS": "Parental Status",
    "FILTER_TRUEVIEW_IAR_REGION_NAME": "Region",
    "FILTER_TRUEVIEW_IAR_REMARKETING_LIST": "Remarketing List ID",
    "FILTER_TRUEVIEW_IAR_TIME_OF_DAY": "Time of Day",
    "FILTER_TRUEVIEW_IAR_YOUTUBE_CHANNEL": "YouTube Channel",
    "FILTER_TRUEVIEW_IAR_YOUTUBE_VIDEO": "YouTube Video",
    "FILTER_TRUEVIEW_IAR_ZIPCODE": "Zip Code",
    "FILTER_TRUEVIEW_INTEREST": "Interest",
    "FILTER_TRUEVIEW_KEYWORD": "Keyword",
    "FILTER_TRUEVIEW_PARENTAL_STATUS": "Parental Status",
    "FILTER_TRUEVIEW_PLACEMENT": "Placement (Managed)",
    "FILTER_TRUEVIEW_PLACEMENT_ID": "Placement ID (Managed)",
    "FILTER_TRUEVIEW_REGION": "Region ID",
    "FILTER_TRUEVIEW_REGION_NAME": "Region",
    "FILTER_TRUEVIEW_REMARKETING_LIST": "Remarketing List ID",
    "FILTER_TRUEVIEW_REMARKETING_LIST_NAME": "Remarketing List",
    "FILTER_TRUEVIEW_TARGETING_EXPANSION": "Optimized Targeting",
    "FILTER_TRUEVIEW_URL": "Placement (All)",
    "FILTER_TRUEVIEW_ZIPCODE": "Zipcode",
    "FILTER_USER_LIST": "Audience List ID",
    "FILTER_USER_LIST_FIRST_PARTY": "First Party Audience List ID",
    "FILTER_USER_LIST_FIRST_PARTY_NAME": "First Party Audience List",
    "FILTER_USER_LIST_THIRD_PARTY": "Third Party Audience List ID",
    "FILTER_USER_LIST_THIRD_PARTY_NAME": "Third Party Audience List",
    "FILTER_VARIANT_ID": "Variant ID",
    "FILTER_VARIANT_NAME": "Variant Name",
    "FILTER_VARIANT_VERSION": "Variant Version",
    "FILTER_VENDOR_MEASUREMENT_MODE": "Vendor Measurement Mode",
    "FILTER_VERIFICATION_AUDIBILITY_COMPLETE": "Audibility At Complete",
    "FILTER_VERIFICATION_AUDIBILITY_START": "Audibility At Start",
    "FILTER_VERIFICATION_VIDEO_PLAYER_SIZE": "Verification Video Player Size",
    "FILTER_VERIFICATION_VIDEO_PLAYER_SIZE_COMPLETE": "Video Player Size at Completion",
    "FILTER_VERIFICATION_VIDEO_PLAYER_SIZE_FIRST_QUARTILE": "Video Player Size at First Quartile",
    "FILTER_VERIFICATION_VIDEO_PLAYER_SIZE_MID_POINT": "Video Player Size at Midpoint",
    "FILTER_VERIFICATION_VIDEO_PLAYER_SIZE_START": "Video Player Size at Start",
    "FILTER_VERIFICATION_VIDEO_PLAYER_SIZE_THIRD_QUARTILE": "Video Player Size at Third Quartile",
    "FILTER_VERIFICATION_VIDEO_POSITION": "Verification Video Position",
    "FILTER_VERIFICATION_VIDEO_RESIZED": "Video Resized",
    "FILTER_VIDEO_AD_POSITION_IN_STREAM": "Video Ad Position In Stream",
    "FILTER_VIDEO_COMPANION_CREATIVE_SIZE": "Companion Creative Size",
    "FILTER_VIDEO_CONTENT_DURATION": "Video Content Duration",
    "FILTER_VIDEO_CONTENT_LIVE_STREAM": "Video Content Live Stream",
    "FILTER_VIDEO_CONTINUOUS_PLAY": "Video Continuous Play",
    "FILTER_VIDEO_CREATIVE_DURATION": "Video Creative Duration",
    "FILTER_VIDEO_CREATIVE_DURATION_SKIPPABLE": "Video Creative Duration (Skippable)",
    "FILTER_VIDEO_DURATION": "Video Duration",
    "FILTER_VIDEO_DURATION_SECONDS": "Max Video Duration",
    "FILTER_VIDEO_DURATION_SECONDS_RANGE": "Max Video Duration Range",
    "FILTER_VIDEO_FORMAT_SUPPORT": "Video Format Support",
    "FILTER_VIDEO_PLAYER_SIZE": "Video Player Size",
    "FILTER_VIDEO_RATING_TIER": "Digital Content Label",
    "FILTER_VIDEO_SKIPPABLE_SUPPORT": "Video Skippable Support",
    "FILTER_WEEK": "Week",
    "FILTER_YEAR": "Year",
    "FILTER_YOUTUBE_ADAPTED_AUDIENCE_LIST": "YouTube Adapted Audience List",
    "FILTER_YOUTUBE_AD_VIDEO": "YouTube Ad Video",
    "FILTER_YOUTUBE_AD_VIDEO_ID": "YouTube Ad Video ID",
    "FILTER_YOUTUBE_CHANNEL": "YouTube Channel",
    "FILTER_YOUTUBE_PROGRAMMATIC_GUARANTEED_ADVERTISER": "Advertiser",
    "FILTER_YOUTUBE_PROGRAMMATIC_GUARANTEED_INSERTION_ORDER": "Insertion Order",
    "FILTER_YOUTUBE_PROGRAMMATIC_GUARANTEED_PARTNER": "Partner",
    "FILTER_YOUTUBE_VIDEO": "YouTube Video",
    "FILTER_ZIP_CODE": "Zip Code ID",
    "FILTER_ZIP_POSTAL_CODE": "Zip Code"
}


def translate_filters(filter_constants: list[str]) -> list[str]:
    return [_filter_table.get(item) for item in filter_constants]


def get_filter_table() -> dict:
    return _filter_table
