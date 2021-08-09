# Utility package to interact with Qualtrics (v3) API

## Installation

Simply run the following commands.

```bash
git clone https://github.com/emanuele-albini/qualtrutils.git
pip install --editable qualtrutils
```

To add a global configuration add in `~\.qualtrutils\qualtrics.toml` the desired configuration:

```toml
API_BASE_URL = "https://yourdatacenter.qualtrics.com/API/v3/"
API_TOKEN = "your_token"
LIBRARY_ID = "UR_XXXXXXXXXXXXX"
SURVEY_ID = "SV_XXXXXXXXXXXXX"
```

This configuration will be used as default in the constructor of `QualtricsSurvey`.

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
