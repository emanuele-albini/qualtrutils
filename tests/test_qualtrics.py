import random
from qualtrutils import *

TEST_SURVEY = "SV_cGcY8PQewcpLz3U"


def test_survey():
    survey = QualtricsSurvey(survey_id=TEST_SURVEY)
    assert True


def test_get():
    survey = QualtricsSurvey(survey_id=TEST_SURVEY)
    question = survey.get_question_by_name('Q1', f'Qget{random.random()}')
    assert True


def test_copy():
    survey = QualtricsSurvey(survey_id=TEST_SURVEY)
    survey.copy_question_by_name('Q1', f'Qcopy{random.random()}', f'B{random.random()}')
    assert True