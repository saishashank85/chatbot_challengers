import typing
import datetime

from typing import Any, Optional, Text, Dict, List, Type

from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.training_data.message import Message

from modules_helping import *

from rasa.nlu.extractors.extractor import EntityExtractor

from rasa.shared.nlu.constants import (
    ENTITIES,
    ENTITY_ATTRIBUTE_VALUE,
    ENTITY_ATTRIBUTE_START,
    ENTITY_ATTRIBUTE_END,
    TEXT,
    ENTITY_ATTRIBUTE_TYPE,
    EXTRACTOR
)

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata


class NERv2(EntityExtractor):
   
    @classmethod
    def required_components(cls) -> List[Type[Component]]:
        

        return []

    
    defaults = {}

 
    supported_language_list = None

    
    not_supported_language_list = None

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super(NERv2,self).__init__(component_config)

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        
        pass

    def process(self, message: Message, **kwargs: Any) -> None:
        
        text = message.get('text',[])
                
        entities = []

        #lang
        try:
            lang_a=lang_detect(text)
            lang = 'en' if lang_a not in ['hi','en','te'] else lang_a
            entities.append(get_entity_format('language',None,None,lang_a,"NER-Language"))
        except:
            print('lang')
            pass    
        #amount 
        try:
            currency = get_currency(text,lang)
            if len(currency[0]) != 0 :
                for i in currency[0]:
                    amount = i['value']
                    curr = i['unit']
                    print("curr123",curr)
                    entities.append(get_entity_format('currency',None,None,curr,'NER-Currency'))
                    entities.append(get_entity_format('amount',None,None,amount,'NER-Currency'))
        except: 
            print("curr")
            
            pass             
        #amount range
        try:
            amt_range = get_num_range(text,lang)
            
            if len(amt_range[0]) != 0 :
                for i in amt_range[0]:
                    rng = i['min_value']+"-"+i['max_value']
                    entities.append(get_entity_format('amount_range',None,None,rng,'NER-Range'))
        except:
            print('range')
            
            pass            
        #date
        try:
            date = get_date(text,lang)
            if len(date[0]) != 0 :
                for i in date[0]:
                    d=i['dd']
                    m=i['mm']
                    y=i['yy']
                    date_obj = datetime.datetime(y,m,d)
                    entities.append(get_entity_format('date',None,None,date,'NER-Date'))
        except: 
            print('date')
            
            pass  
        #phone_number
        try:
            phno = get_phone(text,lang)
            if len(phno[0]) != 0 :
                for i,phonenumber in enumerate(phno[1]): 
                    if len(phonenumber) ==10:
                        entities.append(get_entity_format('phone_number',None,None,phonenumber,'NER-Phone_Number'))
        except: 
            print("pno:")

            
            pass            
                
        #time
        try:
            time = get_time(text,lang)
            if len(time[0]) != 0:
                for i in time[0]:
                    h=i['hh']
                    m=i['mm']
                    s=i['nn']

                    time = datetime.time(int(h),int(m),int(s))
                    entities.append(get_entity_format('time',None,None,time,'NER-Time'))
        except: 
            print("Time:")
            
            pass  
        try:
            message.set(
                ENTITIES, message.get(ENTITIES, []) + entities, add_to_output=True
            )
        except:
            pass
        
        try:
            t_std = stand(text)
            t_num = num2numeric(text)
            message.set('metadata',{"normalised_text":t_std,"text_to_num":t_num},add_to_output=True)
        except:
            print("Stand")
            pass
        pass

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
      

        pass

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional["Metadata"] = None,
        cached_component: Optional["Component"] = None,
        **kwargs: Any,
    ) -> "Component":
        """Load this component from file."""

        if cached_component:
            return cached_component
        else:
            return cls(meta)
