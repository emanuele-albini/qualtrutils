import os
import re
from typing import List, Dict
from posixpath import join as urljoin
from os.path import join as pathjoin

import requests
from tqdm import tqdm
import toml

__all__ = ['Question', 'QualtricsSurvey']

CONFIG_FILE = pathjoin(pathjoin(os.path.expanduser("~"), '.qualtrutils'), 'qualtrics.toml')


class Question(dict):
    """ 
        Extend dict (JSON format for a Qualtrics question) for easy modification
        
        This class allow to handle in an object oriented way the modiication of Qualtrics questions.
        
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__clean_question()

    def set_name(self, name: str):
        """Changes Question Name 

        Args:
            name (str): The name of the question. Must be unique.
        """
        self['DataExportTag'] = name
        return self

    def set_js(self, js: str):
        """
            Add JavaScript code to the question
        """
        self['QuestionJS'] = js
        return self

    def set_choices(self, choices: List[str]):
        """Set multiple choice question answers with the passed ones.


        Args:
            choices (List[str]): The mutliple answers

            choices : list
                List of answers (str)
        """
        self['Choices'] = {str(answ_idx + 1): {'Display': answ} for answ_idx, answ in enumerate(choices)}
        return self

    def set_sliders_starting_position(self, pos: float):
        """Set the slider initial position

        Args:
            pos (float): Initial position (0.0-1.0)

        """
        self['Configuration']['CustomStart'] = True
        self['Configuration']['SliderStartPositions'] = {
            k: pos
            for k, v in self['Configuration']['SliderStartPositions'].items()
        }
        return self

    def text_sub(self, sub_map: Dict[str, str]):
        """Substitute (using Python regex) the occurences in the passed substitution map

        Args:
            sub_map (Dict[str, str]): Dictionary of substitution.
            The key is the occurence to be replaced. The value the replacement.

        Returns:
            [type]: [description]
        """
        for old_value, new_value in sub_map.items():
            self['QuestionText'] = re.sub(old_value, new_value, self['QuestionText'])
            if 'Choices' in self:
                for choice_id in self['Choices']:
                    self['Choices'][choice_id]['Display'] = re.sub(
                        old_value, new_value, self['Choices'][choice_id]['Display']
                    )
        return self

    def __clean_question(self):
        del self['DataExportTag']
        if 'NextChoiceId' in self:
            del self['NextChoiceId']
        if 'NextAnswerId' in self:
            del self['NextAnswerId']
        del self['QuestionID']
        if 'DataVisibility' in self:
            del self['DataVisibility']
        if 'QuestionText_Unsafe' in self:
            assert self['QuestionText'] == self['QuestionText_Unsafe']
            del self['QuestionText_Unsafe']
        if 'GradingData' in self:
            del self['GradingData']
        if 'QuestionJS' in self:
            del self['QuestionJS']
        if 'ChoiceOrder' in self:
            del self['ChoiceOrder']


class QualtricsSurvey:
    """Class for easy handling of Qualtrics Surveys API

        Note: it is not possible to add questions to existing blocks. A new one will be automatically created.

        Note: Question are cached. If the question is change remotely (on the qualtrics interface) you must:
            - call reset_questions_cache, or
            - recreate this object

        
    """
    def __init__(
        self,
        survey_id: str = None,
        library_id: str = None,
        api_token: str = None,
        api_url: str = None,
        config_file: str = CONFIG_FILE,
    ):
        """Constructor for the QualtricsSurvey

        Args:
            survey_id (str, optional): Survey ID. Defaults to config['SURVEY_ID'] (loaded from ~/.qualtrutils/qualtrics.toml).
            library_id (str, optional): Files Library ID. Defaults to config['LIBRARY_ID'] (loaded from ~/.qualtrutils/qualtrics.toml).
            api_token (str, optional): Qualtrics API Token. Defaults to config['API_TOKEN'] (loaded from ~/.qualtrutils/qualtrics.toml).
            api_url (str, optional): Qualtrics Server URL. Defaults to config['API_URL'] (loaded from ~/.qualtrutils/qualtrics.toml).
        """
        config = dict(
            API_URL=None,  # e.g. 'https://subdomain.qualtrics.com/API/v3/'
            API_TOKEN=None,
            SURVEY_ID=None,
            LIBRARY_ID=None,
        )
        if os.path.exists(config_file):
            config.update(toml.load(config_file))

        self._api_url = api_url if api_url is not None else config['API_URL']
        self._api_token = api_token if api_token is not None else config['API_TOKEN']
        self._survey_id = survey_id if survey_id is not None else config['SURVEY_ID']
        self._library_id = library_id if library_id is not None else config['LIBRARY_ID']

        self.block_ids = {}
        self.questions_cache = None

    @property
    def api_url(self):
        if self._api_url is None:
            raise ValueError('No API_URL passed to the constructor or the config file.')
        return self._api_url

    @property
    def api_token(self):
        if self._api_token is None:
            raise ValueError('No API_TOKEN passed to the constructor or the config file.')
        return self._api_token

    @property
    def survey_id(self):
        if self._survey_id is None:
            raise ValueError('No SURVEY_ID passed to the constructor or the config file.')
        return self._survey_id

    @property
    def library_id(self):
        if self._library_id is None:
            raise ValueError('No LIBRARY_ID passed to the constructor or the config file.')
        return self._library_id

    def copy_question_by_name(self, template_name: str, new_name: str, block_name: str) -> Question:
        """Copy an exisiting question to a specified block

        Args:
            template_name (str): Name of the source question
            new_name (str): Name of the destination question
            block_name (str): Name of the block into which to copy the question

        Returns:
            Question : The questsion that has been created.
        """
        question = self.get_question_by_name(template_name, new_name)
        return self.create_question(question, block_name)

    def get_question_by_name(self, template_name: str, new_name: str) -> Question:
        """Get an existing question by name

        Args:
            template_name (str): The question name
            new_name (str): The new question name

        Returns:
            Question: The question with its name change to new_name
        """
        question = Question(self.__get_question_by_name(template_name))
        question.set_name(new_name)
        return question

    def __get_question_by_name(self, question_name: str, force: bool = False):
        # if self.questions_cache is None or force is True:
        self.questions_cache = self.__get(self.__api_questions())['elements']
        for question in self.questions_cache:
            if question['DataExportTag'] == question_name:
                return question
        # Force re-download if search fails
        # if not force:
        #     return self.__get_question_by_name(question_name, force = True)

    def reset_questions_cache(self):
        """
            Reset the questions cache.

            By default each question is loaded only once (when get or copy are called).
        """
        self.questions_cache = None

    def create_question(self, new_question: Question, block_name: str):
        """Create a question in the survey

        Args:
            new_question (Question): The question to create
            block_name (str): The name of the block into which to create the question
        """
        if block_name not in self.block_ids:
            self.create_block(block_name)
        self.__post(self.__api_questions(), new_question, params={'blockId': self.block_ids[block_name]})

    def create_block(self, block_name: str):
        """Create a block

        Args:
            block_name (str): The name of the block
        """
        block = {"Type": "Standard", "Description": block_name}
        # API not implemented (apparently)
        #     if random_questions_per_block is not None:
        #         block['Options'] = {
        #             'RandomizeQuestions': 'RandomWithOnlyX',
        #             'Randomization': {
        #                 'Advanced': {
        #                     'TotalRandSubset': 5,
        #                     'QuestionsPerPage': 0}
        #             }
        #         }
        response = self.__post(self.__api_block(), block)
        self.block_ids[block_name] = response['BlockID']

    def delete_all_blocks(self):
        """Delete all blocks that have been created from the survey.
            Use with care!! The operation is not easily reversible.

            Note: it does not remove all blocks. Only the ones that have been created using this object.
        """
        for block_id in tqdm(self.block_ids.values(), desc='Blocks Deletion'):
            self.__delete_block_by_id(block_id)
        self.block_ids = {}

    def get_flow(self):
        """Get the survey flow

        Returns:
            dict: The survey flow
        """
        return self.__get(self.__api_flow())

    def __get_block_by_id(self, block_id):
        return self.__get(urljoin(self.__api_block(), block_id))

    def __delete_block_by_id(self, block_id):
        return self.__delete(urljoin(self.__api_block(), block_id))

    def __api_survey(self):
        return urljoin(urljoin(self.api_url, 'survey-definitions'), self.survey_id)

    def __api_questions(self):
        return urljoin(self.__api_survey(), 'questions')

    def __api_flow(self):
        return urljoin(self.__api_survey(), 'flow')

    def __api_block(self):
        return urljoin(self.__api_survey(), 'blocks')

    def __api_library(self):
        return urljoin(urljoin(self.api_url, 'libraries'), self.library_id)

    def __api_graphics(self):
        return urljoin(self.__api_library(), 'graphics')

    def __get(self, api_url):
        response = requests.get(api_url, headers=self.__headers())
        if response.status_code == 200:
            return response.json()['result']
        else:
            print('[!ERROR API] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
            print(response.content)
            return None

    def __delete(self, api_url):
        response = requests.delete(api_url, headers=self.__headers())
        if response.status_code == 200:
            return response.json()
        else:
            print('[!ERROR API] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
            print(response.content)
            return None

    def __post(self, api_url, body, data=None, params=None, multipart=False):
        response = requests.post(api_url, data=data, params=params, json=body, headers=self.__headers())
        if response.status_code == 200:
            return response.json()['result']
        else:
            print('[!ERROR API] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
            print(response.content)
            return response

    def __post_files(self, api_url, data):
        response = requests.post(api_url, files=data, headers=self.__headers(json=False))
        if response.status_code == 200:
            return response.json()['result']
        else:
            print('[!ERROR API] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
            print(response.content)
            return response

    def __headers(self, json=True):
        headers = {'X-API-TOKEN': self.api_token}
        if json:
            headers['Content-Type'] = 'application/json'
        return headers