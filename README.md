# Repro2 - an up to date version of the original repro

![Documentation](https://readthedocs.org/projects/repro/badge/?version=latest)
<a href="https://pypi.org/project/repro2/"><img src="https://img.shields.io/pypi/v/repro2?style=flat&logo=pypi"/></a>

Repro is a library for reproducing results from research papers, originally introduced by Daniel Deutsch. This version 2 of the library is an up to date version of the original repo.
For now, it is focused on making predictions with pre-trained models as easy as possible.

Currently, running pre-trained models can be difficult to do.
Some models require specific versions of dependencies, require complicated preprocessing steps, have their own input and output formats, are poorly documented, etc.

Repro addresses these problems by packaging each of the pre-trained models in its own Docker container, which includes the pre-trained models themselves as well as all of the code, dependencies, and environment setup required to run them.
Then, Repro provides lightweight Python code to read the input data, pass the data to a Docker container, run prediction in the container, and return the output to the user.
Since the complicated model-specific code is isolated within Docker, the user does not need to worry about setting up the environment correctly or know how the model is implemented at all.
**As long as you have a working Docker installation, then you can run every model included in repro with no additional effort.**
It should "just work" (at least that is the goal).

## Installation Instructions

First, you need to have a working Docker installation.
See [here](https://repro.readthedocs.io/en/latest/tutorials/docker.html) for installation instructions as well as scripts to verify your setup is working.

Then, we recommend creating a conda environment specific to repro before installing the library:

```sh
uv sync
```

For developers:

```sh
git clone https://github.com/omar2535/repro
cd repro
uv sync
```

## Example Usage

Here is an example of how Repro can be used, highlighting how simple it is to run a complex model pipeline.
We will demonstrate how to generate summaries of a document with three different models

- BertSumExtAbs from [Liu & Lapata (2019)](https://arxiv.org/abs/1908.08345) ([docs](https://repro.readthedocs.io/en/latest/models/liu2019.html))
- BART from [Lewis et al. (2020)](https://arxiv.org/abs/1910.13461) ([docs](https://repro.readthedocs.io/en/latest/models/lewis2020.html))
- GSum from [Dou et al. (2021)](https://arxiv.org/abs/2010.08014) ([docs](https://repro.readthedocs.io/en/latest/models/dou2021.html))

and then evaluate those summaries with three different text generation evaluation metrics

- ROUGE from [Lin (2004)](https://aclanthology.org/W04-1013/) ([docs](https://repro.readthedocs.io/en/latest/models/lin2004.html))
- BLEURT from [Sellam et al. (2020)](https://arxiv.org/abs/2004.04696) ([docs](https://repro.readthedocs.io/en/latest/models/sellam2020.html))
- QAEval from [Deutsch et al. (2021)](https://arxiv.org/abs/2010.00490) ([docs](https://repro.readthedocs.io/en/latest/models/deutsch2021.html))

Once you have Docker and Repro installed, all you have to do is instantiate the classes and run `predict`:

```python
from repro.models.liu2019 import BertSumExtAbs
from repro.models.lewis2020 import BART
from repro.models.dou2021 import SentenceGSumModel

# Each of these classes uses the pre-trained weights that we want to use
# by default, but you can specify others if you want to
liu2019 = BertSumExtAbs()
lewis2020 = BART()
dou2021 = SentenceGSumModel()

# Here's the document we want to summarize (it's not very long,
# but you get the point)
document = (
    "Joseph Robinette Biden Jr. was elected the 46th president of the United States "
    "on Saturday, promising to restore political normalcy and a spirit of national "
    "unity to confront raging health and economic crises, and making Donald J. Trump "
    "a one-term president after four years of tumult in the White House."
)

# Now, run `predict` to generate the summaries from the models
summary1 = liu2019.predict(document)
summary2 = lewis2020.predict(document)
summary3 = dou2021.predict(document)

# Import the evaluation metrics. We call them "models" even though
# they are metrics
from repro.models.lin2004 import ROUGE
from repro.models.sellam2020 import BLEURT
from repro.models.deutsch2021 import QAEval

# Like the summarization models, each of these classes take parameters,
# but we just use the defaults
rouge = ROUGE()
bleurt = BLEURT()
qaeval = QAEval()

# Here is the reference summary we will use
reference = (
    "Joe Biden was elected president of the United States after defeating Donald Trump."
)

# Then evaluate the summaries
for summary in [summary1, summary2, summary3]:
    metrics1 = rouge.predict(summary, [reference])
    metrics2 = bleurt.predict(summary, [reference])
    metrics3 = qaeval.predict(summary, [reference])
```

Behind the scenes, Repro is running each model and metric in its own Docker container.
`BertSumExtAbs`  is tokenizing and sentence splitting the input document with Stanford CoreNLP, then running BERT with `torch==1.1.0` and `transformers==1.2.0`.
`BLEURT` is running `tensorflow==2.2.2` to score the summary with a learned metric.
`QAEval` is chaining together pretrained question generation and question answering models with `torch==1.6.0` to evaluate the model outputs.
**But you don't need to know about any of that to run the models!**
All of the complex logic and environment details are taken care of by the Docker container, so all you have to do is call `predict()`.
It's that simple!

Abstracting the implementation details away in a Docker image is really useful for chaining together a complex NLP pipeline.
In this example, we summarize a document, ask a question, then evaluate how likely the QA prediction and expected answer mean the same thing.
The models used are:

- BART from [Lewis et al. (2020)](https://arxiv.org/abs/1910.13461) ([docs](https://repro.readthedocs.io/en/latest/models/lewis2020.html))
- A neural module network QA model from [Gupta et al. (2020)](https://arxiv.org/abs/1912.04971) ([docs](https://repro.readthedocs.io/en/latest/models/gupta2020.html))
- LERC from [Chen et al. (2020)](https://arxiv.org/abs/2010.03636) ([docs](https://repro.readthedocs.io/en/latest/models/chen2020.html))

```python
from repro.models.chen2020 import LERC
from repro.models.gupta2020 import NeuralModuleNetwork
from repro.models.lewis2020 import BART

document = (
    "Roger Federer is a Swiss professional tennis player. He is ranked "
    "No. 9 in the world by the Association of Tennis Professionals (ATP). "
    "He has won 20 Grand Slam men's singles titles, an all-time record "
    "shared with Rafael Nadal and Novak Djokovic. Federer has been world "
    "No. 1 in the ATP rankings a total of 310 weeks – including a record "
    "237 consecutive weeks – and has finished as the year-end No. 1 five times."
)

# First, summarize the document
bart = BART()
summary = bart.predict(document)

# Now, ask a question using the summary
question = "How many grand slam titles has Roger Federer won?"
answer = "twenty"

nmn = NeuralModuleNetwork()
prediction = nmn.predict(summary, question)

# Check to see if the expected answer ("twenty") and prediction ("20") mean the
# same thing in the summary
lerc = LERC()
score = lerc.predict(summary, question, answer, prediction)
```

More details on how to use the models implemented in Repro can be found [here](https://repro.readthedocs.io/en/latest/tutorials/using-models.html).

## Models Implemented in Repro

See [this page](https://repro.readthedocs.io/en/latest/models/index.html) to see the list of papers with models currently supported by Repro.
Each model's documentation contains information about how to use it as well as whether or not it currently reproduces the results reported in its respective paper or if it hasn't been tested yet.
If it has been tested, the code to reproduce the results is also included.

## Contributing a Model

See the tutorial [here](https://repro.readthedocs.io/en/latest/tutorials/adding-a-model.html) for instructions on how to add a new model.
