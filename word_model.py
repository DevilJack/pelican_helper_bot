from docxtpl import DocxTemplate
from time import gmtime, strftime, localtime
from typing import Dict, Union
from random import randint as ri


async def render_new_doc_sluzhebka(state_data: Dict[str, str]) -> Union[str, None]:
    
    building_dict = {
        "gz": "в Главном учебном корпусе",
        "nik": "в Научно-исследовательском корпусе",
        "3k": "в III учебном корпусе",
        "du_holl": "холла в Доме учёных и выдачу ключа к нему",
        "du_actzal": "актового зала в Доме учёных и выдачу ключа к нему",
        "du_actzal_holl": "актового зала и холла в Доме учёных и выдачу ключей к ним", 
        "sc_actzal": "актового зала в Студенческом клубе ДКПиМТ СПбПУ и выдачу ключа к нему",
        "sc_prime_time": "зоны Prime Time в Студенческом клубе ДКПиМТ СПбПУ и выдачу ключа к ней",
        "sc_actzal_prime_time": "актового зала и зоны Prime Time в Студенческом клубе ДКПиМТ СПбПУ и выдачу ключа к ним"
    }

    filename = None
    building = state_data['building']
    date_interval = state_data['date_interval']
    time_interval = state_data['time_interval']
    goal = state_data['goal']
    responsible = state_data['responsible']
    time_now = strftime("%Y-%m-%d", localtime())
    random_number = ri(12345, 99999)

    doc = DocxTemplate(f"word_templates/sluzhebka/{building}.docx")

    if building in ("gz", "nik", "3k"):
        building_text = building_dict[building]
        
        audience = state_data['audience']
        context = { 
            'class': audience,
            'building': building_text,
            'goal': goal,
            'date_time': date_interval + " " + time_interval,
            'responsable': responsible,
            'date': f"от {time_now}"
        }

        doc.render(context)
        filename = f"Служебка_{random_number}.docx"
        doc.save(filename)
    else:
        room = state_data['room']
        building_text = building_dict[f"{building}_{room}"]
        context = { 
            'building': building_text,
            'goal': goal,
            'date_time': date_interval + " " + time_interval,
            'responsable': responsible,
            'date': f"от {time_now}"
        }
        
        doc.render(context)
        filename = f"Служебка_{random_number}.docx"
        doc.save(filename)

    return filename