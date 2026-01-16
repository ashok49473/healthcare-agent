"""Tools for the healthcare agent to interact with FHIR API."""
from langchain.tools import tool
from typing import Dict, Any, Optional
from utils.fhir_client import FHIRClient
import json
import logging

logger = logging.getLogger(__name__)
fhir_client = FHIRClient()


@tool
def create_patient(patient_data: str) -> str:
    """Create a new patient in the FHIR system.

    Args:
        patient_data: JSON string containing patient information with fields like name, gender, birthDate

    Returns:
        Success message with patient ID or error message
    """
    try:
        data = json.loads(patient_data) if isinstance(patient_data, str) else patient_data
        result = fhir_client.create_resource("Patient", data)
        patient_id = result.get('id', 'Unknown')
        return f"Successfully created patient with ID: {patient_id}"
    except Exception as e:
        logger.error(f"Error creating patient: {e}")
        return f"Error creating patient: {str(e)}"


@tool
def get_patient(patient_id: str) -> str:
    """Retrieve patient information by ID.

    Args:
        patient_id: The FHIR patient ID

    Returns:
        Patient information as JSON string or error message
    """
    try:
        result = fhir_client.read_resource("Patient", patient_id)
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error retrieving patient: {e}")
        return f"Error retrieving patient: {str(e)}"


@tool
def search_patients(search_params: str) -> str:
    """Search for patients using various criteria.

    Args:
        search_params: JSON string with search parameters like family, given, birthdate, gender

    Returns:
        List of matching patients or error message
    """
    try:
        params = json.loads(search_params) if isinstance(search_params, str) else search_params
        result = fhir_client.search_resources("Patient", params)
        entries = result.get('entry', [])
        if not entries:
            return "No patients found matching the search criteria"

        patients_info = []
        for entry in entries[:10]:  # Limit to 10 results
            resource = entry.get('resource', {})
            patient_id = resource.get('id')
            name = resource.get('name', [{}])[0]
            patients_info.append({
                'id': patient_id,
                'name': name,
                'gender': resource.get('gender'),
                'birthDate': resource.get('birthDate')
            })

        return json.dumps(patients_info, indent=2)
    except Exception as e:
        logger.error(f"Error searching patients: {e}")
        return f"Error searching patients: {str(e)}"


@tool
def update_patient(patient_id: str, patient_data: str) -> str:
    """Update patient information.

    Args:
        patient_id: The FHIR patient ID
        patient_data: JSON string containing updated patient information

    Returns:
        Success message or error message
    """
    try:
        data = json.loads(patient_data) if isinstance(patient_data, str) else patient_data
        result = fhir_client.update_resource("Patient", patient_id, data)
        return f"Successfully updated patient {patient_id}"
    except Exception as e:
        logger.error(f"Error updating patient: {e}")
        return f"Error updating patient: {str(e)}"


@tool
def create_observation(observation_data: str) -> str:
    """Create a new medical observation (vital signs, lab results, etc.).

    Args:
        observation_data: JSON string containing observation data

    Returns:
        Success message with observation ID or error message
    """
    try:
        data = json.loads(observation_data) if isinstance(observation_data, str) else observation_data
        result = fhir_client.create_resource("Observation", data)
        obs_id = result.get('id', 'Unknown')
        return f"Successfully created observation with ID: {obs_id}"
    except Exception as e:
        logger.error(f"Error creating observation: {e}")
        return f"Error creating observation: {str(e)}"


@tool
def get_patient_observations(patient_id: str) -> str:
    """Retrieve all observations for a specific patient.

    Args:
        patient_id: The FHIR patient ID

    Returns:
        List of observations as JSON string or error message
    """
    try:
        observations = fhir_client.get_patient_observations(patient_id)
        if not observations:
            return f"No observations found for patient {patient_id}"

        obs_info = []
        for entry in observations[:20]:  # Limit to 20 results
            resource = entry.get('resource', {})
            obs_info.append({
                'id': resource.get('id'),
                'status': resource.get('status'),
                'code': resource.get('code'),
                'value': resource.get('valueQuantity') or resource.get('valueString'),
                'effectiveDateTime': resource.get('effectiveDateTime')
            })

        return json.dumps(obs_info, indent=2)
    except Exception as e:
        logger.error(f"Error retrieving observations: {e}")
        return f"Error retrieving observations: {str(e)}"


@tool
def search_observations(search_params: str) -> str:
    """Search for observations using various criteria.

    Args:
        search_params: JSON string with search parameters like patient, code, date

    Returns:
        List of matching observations or error message
    """
    try:
        params = json.loads(search_params) if isinstance(search_params, str) else search_params
        result = fhir_client.search_resources("Observation", params)
        entries = result.get('entry', [])
        if not entries:
            return "No observations found matching the search criteria"

        return json.dumps([entry.get('resource') for entry in entries[:10]], indent=2)
    except Exception as e:
        logger.error(f"Error searching observations: {e}")
        return f"Error searching observations: {str(e)}"


@tool
def get_patient_conditions(patient_id: str) -> str:
    """Retrieve all conditions/diagnoses for a specific patient.

    Args:
        patient_id: The FHIR patient ID

    Returns:
        List of conditions as JSON string or error message, or message if no data found
    """
    try:
        result = fhir_client.search_resources("Condition", {"patient": patient_id})
        entries = result.get('entry', [])
        if not entries:
            return f"No conditions found for patient {patient_id}. This patient may not have any recorded conditions in the system."

        conditions_info = []
        for entry in entries[:20]:
            resource = entry.get('resource', {})
            conditions_info.append({
                'id': resource.get('id'),
                'clinicalStatus': resource.get('clinicalStatus'),
                'verificationStatus': resource.get('verificationStatus'),
                'code': resource.get('code'),
                'recordedDate': resource.get('recordedDate'),
                'onsetDateTime': resource.get('onsetDateTime')
            })

        return json.dumps(conditions_info, indent=2)
    except Exception as e:
        logger.error(f"Error retrieving conditions: {e}")
        return f"Error retrieving conditions for patient {patient_id}: {str(e)}"


@tool
def get_patient_encounters(patient_id: str) -> str:
    """Retrieve all encounters for a specific patient.

    Args:
        patient_id: The FHIR patient ID

    Returns:
        List of encounters as JSON string or error message, or message if no data found
    """
    try:
        result = fhir_client.search_resources("Encounter", {"patient": patient_id})
        entries = result.get('entry', [])
        if not entries:
            return f"No encounters found for patient {patient_id}. This patient may not have any recorded visits in the system."

        encounters_info = []
        for entry in entries[:20]:
            resource = entry.get('resource', {})
            encounters_info.append({
                'id': resource.get('id'),
                'status': resource.get('status'),
                'class': resource.get('class'),
                'type': resource.get('type'),
                'period': resource.get('period'),
                'serviceProvider': resource.get('serviceProvider')
            })

        return json.dumps(encounters_info, indent=2)
    except Exception as e:
        logger.error(f"Error retrieving encounters: {e}")
        return f"Error retrieving encounters for patient {patient_id}: {str(e)}"


@tool
def get_patient_medications(patient_id: str) -> str:
    """Retrieve all medication requests for a specific patient.

    Args:
        patient_id: The FHIR patient ID

    Returns:
        List of medication requests as JSON string or error message, or message if no data found
    """
    try:
        result = fhir_client.search_resources("MedicationRequest", {"patient": patient_id})
        entries = result.get('entry', [])
        if not entries:
            return f"No medication requests found for patient {patient_id}. This patient may not have any recorded medications in the system."

        medications_info = []
        for entry in entries[:20]:
            resource = entry.get('resource', {})
            medications_info.append({
                'id': resource.get('id'),
                'status': resource.get('status'),
                'intent': resource.get('intent'),
                'medicationCodeableConcept': resource.get('medicationCodeableConcept'),
                'medicationReference': resource.get('medicationReference'),
                'authoredOn': resource.get('authoredOn'),
                'dosageInstruction': resource.get('dosageInstruction')
            })

        return json.dumps(medications_info, indent=2)
    except Exception as e:
        logger.error(f"Error retrieving medications: {e}")
        return f"Error retrieving medication requests for patient {patient_id}: {str(e)}"


@tool
def get_complete_patient_data(patient_id: str) -> str:
    """Retrieve comprehensive patient data including demographics, observations, conditions, encounters, and medications.

    Args:
        patient_id: The FHIR patient ID

    Returns:
        Complete patient data as JSON string or error message
    """
    try:
        # Get patient demographics
        patient_data = fhir_client.read_resource("Patient", patient_id)

        # Get all related data
        observations = fhir_client.search_resources("Observation", {"patient": patient_id}).get('entry', [])
        conditions = fhir_client.search_resources("Condition", {"patient": patient_id}).get('entry', [])
        encounters = fhir_client.search_resources("Encounter", {"patient": patient_id}).get('entry', [])
        medications = fhir_client.search_resources("MedicationRequest", {"patient": patient_id}).get('entry', [])

        complete_data = {
            "patient": {
                "id": patient_data.get('id'),
                "name": patient_data.get('name'),
                "gender": patient_data.get('gender'),
                "birthDate": patient_data.get('birthDate'),
                "address": patient_data.get('address'),
                "telecom": patient_data.get('telecom')
            },
            "observations": [entry.get('resource') for entry in observations[:10]],
            "conditions": [entry.get('resource') for entry in conditions[:10]],
            "encounters": [entry.get('resource') for entry in encounters[:10]],
            "medications": [entry.get('resource') for entry in medications[:10]],
            "summary": {
                "total_observations": len(observations),
                "total_conditions": len(conditions),
                "total_encounters": len(encounters),
                "total_medications": len(medications)
            }
        }

        return json.dumps(complete_data, indent=2)
    except Exception as e:
        logger.error(f"Error retrieving complete patient data: {e}")
        return f"Error retrieving complete data for patient {patient_id}: {str(e)}"


# Export all tools
healthcare_tools = [
    get_patient,
    get_patient_observations,
    get_patient_conditions,
    get_patient_encounters,
    get_patient_medications,
    get_complete_patient_data,
    search_patients,
    search_observations,
    create_patient,
    update_patient,
    create_observation,
]

