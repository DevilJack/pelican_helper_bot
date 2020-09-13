from docxtpl import DocxTemplate
from config import WORK_HEADERS
from time import gmtime, strftime, localtime


def render_new_doc_sluzhebka(audit: str, building: str, date_time: str, responsable: str, goal: str):
    
    bul = {
        "gz": "в Главном учебном корпусе",
        "nik": "в Научно-исследовательском корпусе",
        "3k": "в 3 учебном корпусе",
        "act_zal": "в Актовом зале",
        "dom_uch": "в холле Дома ученых",
        "prime_time": "в зоне Prime Time Студенческого клуба ДКПиМТ СПбПУ"
    }

    doc = DocxTemplate(f"word_templates/sluzhebka/{building}.docx")

    context = { 
        'class': audit,
        'building': bul[building],
        'goal': goal,
        'date_time': date_time,
        'responsable': responsable,
        'date': strftime("%Y-%m-%d %H:%M:%S", localtime())
    }

    doc.render(context)
    doc.save("final.docx")

render_new_doc()