"""Tests for the FHIR client."""
import pytest
from utils.fhir_client import FHIRClient
from utils.fhir_templates import PATIENT_EXAMPLE


def test_fhir_client_initialization():
    """Test FHIR client initialization."""
    client = FHIRClient()
    assert client.base_url == "https://hapi.fhir.org/baseR4"


def test_search_patients():
    """Test searching for patients."""
    client = FHIRClient()
    try:
        result = client.search_resources("Patient", {"_count": "1"})
        assert "resourceType" in result
        assert result["resourceType"] == "Bundle"
    except Exception as e:
        pytest.skip(f"FHIR server unavailable: {e}")


if __name__ == "__main__":
    pytest.main([__file__])

