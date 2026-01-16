"""FHIR API client for healthcare data operations."""
import requests
from typing import Dict, List, Optional, Any
import logging
from config import FHIR_BASE_URL

logger = logging.getLogger(__name__)


class FHIRClient:
    """Client for interacting with FHIR API."""

    def __init__(self, base_url: str = FHIR_BASE_URL):
        """Initialize FHIR client.

        Args:
            base_url: Base URL for the FHIR server
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/fhir+json',
            'Content-Type': 'application/fhir+json'
        })

    def create_resource(self, resource_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new FHIR resource.

        Args:
            resource_type: Type of FHIR resource (e.g., 'Patient', 'Observation')
            data: Resource data as dictionary

        Returns:
            Created resource with ID
        """
        try:
            url = f"{self.base_url}/{resource_type}"
            response = self.session.post(url, json=data)
            response.raise_for_status()
            logger.info(f"Created {resource_type} resource successfully")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating {resource_type}: {e}")
            raise

    def read_resource(self, resource_type: str, resource_id: str) -> Dict[str, Any]:
        """Read a FHIR resource by ID.

        Args:
            resource_type: Type of FHIR resource
            resource_id: ID of the resource

        Returns:
            Resource data
        """
        try:
            url = f"{self.base_url}/{resource_type}/{resource_id}"
            response = self.session.get(url)
            response.raise_for_status()
            logger.info(f"Retrieved {resource_type}/{resource_id} successfully")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error reading {resource_type}/{resource_id}: {e}")
            raise

    def update_resource(self, resource_type: str, resource_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a FHIR resource.

        Args:
            resource_type: Type of FHIR resource
            resource_id: ID of the resource
            data: Updated resource data

        Returns:
            Updated resource
        """
        try:
            url = f"{self.base_url}/{resource_type}/{resource_id}"
            data['id'] = resource_id
            response = self.session.put(url, json=data)
            response.raise_for_status()
            logger.info(f"Updated {resource_type}/{resource_id} successfully")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error updating {resource_type}/{resource_id}: {e}")
            raise

    def delete_resource(self, resource_type: str, resource_id: str) -> bool:
        """Delete a FHIR resource.

        Args:
            resource_type: Type of FHIR resource
            resource_id: ID of the resource

        Returns:
            True if deleted successfully
        """
        try:
            url = f"{self.base_url}/{resource_type}/{resource_id}"
            response = self.session.delete(url)
            response.raise_for_status()
            logger.info(f"Deleted {resource_type}/{resource_id} successfully")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error deleting {resource_type}/{resource_id}: {e}")
            raise

    def search_resources(self, resource_type: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Search for FHIR resources.

        Args:
            resource_type: Type of FHIR resource
            params: Search parameters

        Returns:
            Bundle of matching resources
        """
        try:
            url = f"{self.base_url}/{resource_type}"
            response = self.session.get(url, params=params)
            response.raise_for_status()
            logger.info(f"Searched {resource_type} with params {params}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching {resource_type}: {e}")
            raise

    def get_patient_by_name(self, family_name: str, given_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for patients by name.

        Args:
            family_name: Patient's family name
            given_name: Patient's given name (optional)

        Returns:
            List of matching patient resources
        """
        params = {'family': family_name}
        if given_name:
            params['given'] = given_name

        result = self.search_resources('Patient', params)
        return result.get('entry', [])

    def get_patient_observations(self, patient_id: str) -> List[Dict[str, Any]]:
        """Get all observations for a patient.

        Args:
            patient_id: Patient ID

        Returns:
            List of observation resources
        """
        params = {'patient': patient_id}
        result = self.search_resources('Observation', params)
        return result.get('entry', [])

