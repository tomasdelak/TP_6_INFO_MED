from patient import create_patient_resource
from medicationstatement import create_medication_statement
from base import send_resource_to_hapi_fhir, get_resource_from_hapi_fhir, search_patient_by_dni



if __name__ == "__main__":
    # Parámetros del paciente (se puede dejar algunos vacíos)
    family_name = "Doe"
    given_name = "John"
    birth_date = "1990-01-01"
    gender = "male"
    phone = None 

    # Crear y enviar el recurso de paciente 
    paciente = create_patient_resource("De la Llave", "Tomas", "2002-04-22", "male", None, "43992337")
    patient_id = send_resource_to_hapi_fhir(paciente, 'Patient')

    # Ver el recurso de paciente creado
    if patient_id:
        get_resource_from_hapi_fhir(patient_id,'Patient')


# Busco paciente por dni
print("\n Buscamos paciente por dni \n")
search_patient_by_dni(43992337)
 

# Actividad 3.c
    
# Ahora, crear un recurso MedicationStatement asociado al paciente
med_statement = create_medication_statement(
    patient_id=patient_id,
    medication_code="322236009",  # código snomed Paracetamol
    medication_display="Paracetamol 500mg tableta",
    status="active",
    effective_date="2024-06-01",
    note_text="Paciente refiere automedicación ocasional por dolor."
)

# Enviar el recurso MedicationStatement
med_statement_id = send_resource_to_hapi_fhir(med_statement, 'MedicationStatement')

if med_statement_id:
    print(f"MedicationStatement creado con ID: {med_statement_id}")
    get_resource_from_hapi_fhir(med_statement_id, 'MedicationStatement')
else:
    print("No se pudo crear el paciente.")
