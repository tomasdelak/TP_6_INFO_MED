from fhir.resources.medicationstatement import MedicationStatement
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference
from fhir.resources.annotation import Annotation


def create_medication_statement(patient_id, medication_code, medication_display, status="active", effective_date=None, note_text=None):
    med_statement = MedicationStatement(
        status=status,
        medicationCodeableConcept=CodeableConcept(
            coding=[Coding(
                system="http://www.nlm.nih.gov/research/umls/rxnorm",
                code=medication_code,
                display=medication_display
            )]
        ),
        subject=Reference(reference=f"Patient/{patient_id}")
    )

    if effective_date:
        med_statement.effectiveDateTime = effective_date

    if note_text:
        med_statement.note = [Annotation(text=note_text)]

    return med_statement