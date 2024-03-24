import pandas as pd
from enum import Enum, auto
from PIL import Image as PILImage
from utils import LOG

class ContentType(Enum):
    TEXT = auto()
    TABLE = auto()
    IMAGE = auto()

class Content:
    def __init__(self, content_type, original, translation=None):
        self.content_type = content_type
        self.original = original
        self.translation = translation
        self.status = False

    def set_translation(self, translation, status):
        if not self.check_translation_type(translation):
            raise ValueError(f"Invalid translation type. Expected {self.content_type}, but got {type(translation)}")
        self.translation = translation
        self.status = status

    def check_translation_type(self, translation):
        if self.content_type == ContentType.TEXT and isinstance(translation, str):
            return True
        elif self.content_type == ContentType.TABLE and isinstance(translation, list):
            return True
        elif self.content_type == ContentType.IMAGE and isinstance(translation, PILImage.Image):
            return True
        return False


class TableContent(Content):
    def __init__(self, data, translation=None):
        df = pd.DataFrame(data)

        # Verify if the number of rows and columns in the data and DataFrame object match
        if len(data) != len(df) or len(data[0]) != len(df.columns):
            raise ValueError("The number of rows and columns in the extracted table data and DataFrame object do not match.")
        
        super().__init__(ContentType.TABLE, df)
    

    

    def set_translation(self, translation, status):
        try:
            if not isinstance(translation, str):
                raise ValueError(f"Invalid translation type. Expected str, but got {type(translation)}")

            LOG.debug(f"translation_data={translation}")
            # Convert the string to a list of lists
            table_data = [row.strip().split() for row in translation.strip().split('\n')]
            LOG.debug(table_data)   

           
            if len(table_data[0]) > 3 and len(table_data[0])!=7:       
                # 使用切片获取倒数第二和倒数第三个元素  
                second_last = table_data[0][-2]  
                third_last = table_data[0][-3]  
                
                # 合并这两个元素（这里假设是字符串，使用加号连接）  
                merged_element = second_last + third_last  
                
                # 创建新的列表，除了倒数第二和倒数第三个元素外，其他元素与原列表相同  
                table_data[0] = table_data[0][:-3] + [merged_element] + table_data[0][-1:]      
            # Create a DataFrame from the table_data
            translated_df = pd.DataFrame(table_data[1:], columns=table_data[0])
            LOG.debug(translated_df)
            self.translation = translated_df
            self.translation = translation
            self.status = status
        except Exception as e:
            LOG.error(f"An error occurred during table translation: {e}")
            self.translation = None
            self.status = False
    
    def merge_last_two_elements(lst):  
        if len(lst) < 3:  
            raise ValueError("List must have at least 3 elements")  
        
        # 使用切片获取倒数第二和倒数第三个元素  
        second_last = lst[-2]  
        third_last = lst[-3]  
        
        # 合并这两个元素（这里假设是字符串，使用加号连接）  
        merged_element = second_last + third_last  
        
        # 创建新的列表，除了倒数第二和倒数第三个元素外，其他元素与原列表相同  
        new_lst = lst[:-3] + [merged_element] + lst[-1:]  
        
        return new_lst 

    def __str__(self):
        return self.original.to_string(header=False, index=False)

    def iter_items(self, translated=False):
        target_df = self.translation if translated else self.original
        for row_idx, row in target_df.iterrows():
            for col_idx, item in enumerate(row):
                yield (row_idx, col_idx, item)

    def update_item(self, row_idx, col_idx, new_value, translated=False):
        target_df = self.translation if translated else self.original
        target_df.at[row_idx, col_idx] = new_value

    def get_original_as_str(self):
        return self.original.to_string(header=False, index=False)