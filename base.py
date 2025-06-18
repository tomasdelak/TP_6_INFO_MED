import requests
from patient import create_patient_resource


# Enviar el recurso FHIR al servidor HAPI FHIR
def send_resource_to_hapi_fhir(resource,resource_type):
    url = f"http://hapi.fhir.org/baseR4/{resource_type}"
    headers = {"Content-Type": "application/fhir+json"}
    resource_json = resource.json()

    response = requests.post(url, headers=headers, data=resource_json)

    if response.status_code == 201:
        print("Recurso creado exitosamente")
        
        # Devolver el ID del recurso creado
        return response.json()['id']
    else:
        print(f"Error al crear el recurso: {response.status_code}")
        print(response.json())
        return None

# Buscar el recurso por ID 
def get_resource_from_hapi_fhir(resource_id, resource_type):
    url = f"http://hapi.fhir.org/baseR4/{resource_type}/{resource_id}"
    response = requests.get(url, headers={"Accept": "application/fhir+json"})

    if response.status_code == 200:
        resource = response.json()
        print(resource)

        # Buscar el DNI en el campo identifier
        identifiers = resource.get("identifier", [])
        for identifier in identifiers:
            if identifier.get("system") == "https://www.argentina.gob.ar/interior/renaper":
                dni = identifier.get("value")
                print(f"DNI del paciente: {dni}")
                return dni  # Retorna el DNI para usarlo en otras funciones

        print("DNI no encontrado en los identificadores.")
        return None

    else:
        print(f"Error al obtener el recurso: {response.status_code}")
        print(response.json())

# Buscar paciente por DNI
def search_patient_by_dni(dni):
    url = "http://hapi.fhir.org/baseR4/Patient"
    params = {
        "identifier": f"https://www.argentina.gob.ar/interior/renaper|{dni}"
    }
    response = requests.get(url, params=params, headers={"Accept": "application/fhir+json"})

    if response.status_code == 200:
        bundle = response.json()
        entries = bundle.get("entry", [])
        if not entries:
            print(f"No se encontró ningún paciente con DNI {dni}.")
            return None
        
        # Se encontró al menos un paciente
        patient = entries[0]["resource"]
        print(f"Paciente encontrado: {patient.get('name', [{}])[0].get('given', [''])[0]} {patient.get('name', [{}])[0].get('family', '')}")
        return patient
    else:
        print(f"Error al buscar el paciente: {response.status_code}")
        print(response.json())
        return None
