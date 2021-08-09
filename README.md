# QualtrUtils - A package to create questions from templates with Qualtrics (v3) API

[![PyPI pyversions](https://img.shields.io/pypi/pyversions/qualtrutils.svg)](https://pypi.python.org/pypi/qualtrutils/)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/emanuele-albini/qualtrutils/blob/master/LICENSE)
[![PyPI](https://badge.fury.io/py/qualtrutils.svg)](https://pypi.python.org/pypi/qualtrutils/)
[![Maintaner](https://img.shields.io/badge/maintainer-Emanuele-lightgrey)](https://www.emanuelealbini.com)

This package allows the creation of questions based on an existing template (i.e., a question created with the Qualtrics interface. The operations that this package supports are:

- Creating block
- Copying an existing question
- Replacing keywords
- Changing multiple choice answers
- Changing the initial position of the slider
- Changing a question JS code

## Installation

Simply run the following command.

```bash
pip install qualtrutils
```

#### For developers

To use the package in editable mode use instead the following.

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
