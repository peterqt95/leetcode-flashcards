from collections import namedtuple

def merge(*records):
    """
    :param records: (varargs list of namedtuple) The patient details.
    :returns: (namedtuple) named Patient, containing details from all records, in entry order.
    """

    # personal_details = records[0]
    # complexion = records[1]
    # Patient = namedtuple('Patient', personal_details._fields + complexion._fields)
    # return Patient(personal_details.date_of_birth, complexion.eye_color, complexion.hair_color)


    list_of_tuples = []
    for record in records:
        list_of_tuples += record._fields

    temp = {}
    for record in records:
        temp_record = record._asdict()
        for field in record._fields:
            temp[field] = temp_record[field]

    Patient = namedtuple('Patient', temp.keys())(*temp.values())
    return Patient

PersonalDetails = namedtuple('PersonalDetails', ['date_of_birth'])
personal_details = PersonalDetails(date_of_birth = '06-04-1972')
                                   
Complexion = namedtuple('Complexion', ['eye_color', 'hair_color'])
complexion = Complexion(eye_color = 'Blue', hair_color = 'Black')
  
print(merge(personal_details, complexion))