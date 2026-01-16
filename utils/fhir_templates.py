"""Example FHIR resource templates for common use cases."""

# Example Patient Resource
PATIENT_EXAMPLE = {
    "resourceType": "Patient",
    "name": [
        {
            "use": "official",
            "family": "Doe",
            "given": ["John"]
        }
    ],
    "gender": "male",
    "birthDate": "1990-01-01",
    "address": [
        {
            "use": "home",
            "line": ["123 Main St"],
            "city": "Boston",
            "state": "MA",
            "postalCode": "02101",
            "country": "USA"
        }
    ]
}

# Example Observation Resource (Blood Pressure)
BLOOD_PRESSURE_EXAMPLE = {
    "resourceType": "Observation",
    "status": "final",
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "vital-signs",
                    "display": "Vital Signs"
                }
            ]
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "85354-9",
                "display": "Blood pressure panel"
            }
        ]
    },
    "subject": {
        "reference": "Patient/example-id"
    },
    "effectiveDateTime": "2024-01-12T10:30:00Z",
    "component": [
        {
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8480-6",
                        "display": "Systolic blood pressure"
                    }
                ]
            },
            "valueQuantity": {
                "value": 120,
                "unit": "mmHg",
                "system": "http://unitsofmeasure.org",
                "code": "mm[Hg]"
            }
        },
        {
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8462-4",
                        "display": "Diastolic blood pressure"
                    }
                ]
            },
            "valueQuantity": {
                "value": 80,
                "unit": "mmHg",
                "system": "http://unitsofmeasure.org",
                "code": "mm[Hg]"
            }
        }
    ]
}

# Example Observation Resource (Body Temperature)
TEMPERATURE_EXAMPLE = {
    "resourceType": "Observation",
    "status": "final",
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "vital-signs",
                    "display": "Vital Signs"
                }
            ]
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "8310-5",
                "display": "Body temperature"
            }
        ]
    },
    "subject": {
        "reference": "Patient/example-id"
    },
    "effectiveDateTime": "2024-01-12T10:30:00Z",
    "valueQuantity": {
        "value": 98.6,
        "unit": "F",
        "system": "http://unitsofmeasure.org",
        "code": "[degF]"
    }
}


