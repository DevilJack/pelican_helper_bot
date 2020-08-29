import pymorphy2
import json
from typing import Dict, List, Union, Any
from aiogram import types
from rutermextract import TermExtractor
from nltk.stem.snowball import SnowballStemmer


async def do_find_top_answers(message: types.Message, xl_data: Dict[str, str]) -> Union[str, bool, int]:
    try:
        await _do_increment_question_count(message.chat.id)

        top_answers = []
        
        for answer, kws in xl_data.items():
            count = 0
            for kw in kws:
                if kw.lower() in message.text.lower():
                    count += 1
            
            if count > 0:
                to_insert = {
                    "count": count,
                    "answer": answer
                }
                top_answers = await _do_insert_to_array(to_insert, top_answers)
        
        if len(top_answers) == 0:
            return False
        
        await _do_increment_suc_answers_count(message.chat.id)

        result = ""
        for ans in top_answers:
            result += ans['answer']
            result += "\n\n"
        
        return result
    except:
        return -1



async def _do_insert_to_array(to_insert: Any, array: List[Any]) -> Union[List[Any], bool]:
    try:
        array.append(to_insert)
        array = await _do_sort_by_count(array)
        return array[:2]
    except:
        return False


async def _do_sort_by_count(array: List[Any]) -> Union[List[Any], bool]:
    try:
        size = len(array)
        maximum = 0

        for i in range(0, size - 1):
            maximum = i

            for j in range(i + 1, size):
                
                if array[j]['count'] > array[maximum]['count']:
                    maximum = j

            array[i], array[maximum] = array[maximum], array[i]

        return array 
    except:
        return False


async def do_remember_user_start(message: types.Message) -> bool:
    try:
        with open("users.json", "r+", encoding="utf-8") as file:
            data = json.load(file)
            
            if str(message.chat.id) not in data["users"].keys():
                new_user = {
                    "username": message.from_user.username,
                    "first_last": message.from_user.first_name + " " + message.from_user.last_name,
                    "questions_count": 0,
                    "success_answers_count": 0
                }

                data["users"][message.chat.id] = new_user

            file.seek(0)
            file.write(json.dumps(data, ensure_ascii=False, indent=4))
            file.truncate()

        return True
    except:
        return False


async def _do_increment_question_count(chat_id: int) -> bool:
    try:
        with open("users.json", "r+", encoding="utf-8") as file:
            data = json.load(file)
            
            data["users"][str(chat_id)]["questions_count"] += 1

            file.seek(0)
            file.write(json.dumps(data, ensure_ascii=False, indent=4))
            file.truncate()

        return True
    except:
        return False


async def _do_increment_suc_answers_count(chat_id: int) -> bool:
    try:
        with open("users.json", "r+", encoding="utf-8") as file:
            data = json.load(file)
            
            data["users"][str(chat_id)]["success_answers_count"] += 1

            file.seek(0)
            file.write(json.dumps(data, ensure_ascii=False, indent=4))
            file.truncate()

        return True
    except:
        return False


        





# ========= ruter
# term_extractor = TermExtractor()
# text = 'Почему контрактники платят один раз, а я каждый месяц( бюджетник) ?'

# for term in term_extractor(text):
#     print(term)
#     print(term.normalized, term.count)

# ========= morph
# morph = pymorphy2.MorphAnalyzer()
# for word in text.split():
#     print(morph.parse(word)[0].normal_form)

# ======== nltk
  # $ pip install nltk
  
# stemmer = SnowballStemmer("russian")
# answer = 'Почему контрактники платят один раз, а я каждый месяц( бюджетник) ?'
# print(*map(stemmer.stem, answer.split()))