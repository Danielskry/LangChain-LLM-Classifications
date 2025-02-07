""" JSON utils """

from datetime import datetime

def convert_datetimes_to_iso(incident_dict: dict) -> dict:
        """
        Convert all datetime objects in the given dictionary to ISO format strings.
        For example, datetime(2023, 6, 10, 15, 30) is converted to "2023-06-10T15:30:00".

        Parameters:
        - incident_dict (dict): Dictionary containing the incident data.
        
        Returns:
        - incident_dict (dict): Dictionary with datetime objects converted to ISO format strings.
        """
        for key, value in incident_dict.items():
            if isinstance(value, datetime):
                incident_dict[key] = value.isoformat()
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        for sub_key, sub_value in item.items():
                            if isinstance(sub_value, datetime):
                                item[sub_key] = sub_value.isoformat()
        return incident_dict
