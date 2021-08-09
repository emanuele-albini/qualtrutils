# Utility package to interact with Qualtrics (v3) API
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/qualtrutils.svg)](https://pypi.python.org/pypi/qualtrutils/)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/emanuele-albini/qualtrutils/blob/master/LICENSE)
[![PyPI](https://badge.fury.io/py/qualtrutils.svg)](https://pypi.python.org/pypi/qualtrutils/)
[![GitHub commits](https://img.shields.io/github/commits-since/emanuele-albini/qualtrutils/v0.0.1)](https://github.com/emanuele-albini/qualtrutils/commit/)
[![Maintaner](https://img.shields.io/badge/maintainer-Emanuele-lightgrey)](https://www.emanuelealbini.com)

## Installation

Simply run the following commands.

```bash
git clone https://github.com/emanuele-albini/qualtrutils.git
pip install --editable qualtrutils
```

## Configuration (optional)

Global configuration is in `~\.qualtrutils\qualtrics.toml`. Example:

```toml
API_URL = "https://yourdatacenter.qualtrics.com/API/v3/"
API_TOKEN = "your_token"
LIBRARY_ID = "UR_XXXXXXXXXXXXX"
SURVEY_ID = "SV_XXXXXXXXXXXXX"
```

The configuration saved in `~\.qualtrutils\qualtrics.toml` will be used as default in `QualtricsSurvey` constructor.

## Usage example

```python
from qualtrutils import QualtricsSurvey

survey = QualtricsSurvey()

# Get a question from an existing survey
question = survey.get_question_by_name('QuestionName', 'MyNewQuestion')

# The following will replace (using regex) all the occurences
# of 'SOMETHING' in the question text and multiples choice answers (if any)
# with 'SOMETHING_ELSE'
question.text_sub('SOMETHING', 'SOMETHING_ELSE')

# The following will set the multiple choice answers
question.set_choices(['First Answer', 'Second Answer', 'Third Answer'])

# The flowwing will set the Javascript code of the question
question.set_js('var hello = 1;')

# Add this new question to the survey in a block called 'Block A'
# If the block does not exists it will be created
survey.create_question(question, 'Block A')
```

## Documentation

See [here](https://emanuele-albini.github.io/qualtrutils) for the complete documentation with all the functionalities.
