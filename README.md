# Building and Explaining a Movie Recommender System using Matrix Factorization

Course project for **AI for Machine Learning & Deep Learning**.

This repository contains the initial work for a recommender system project focused on
movie recommendations, matrix factorization, and explainability. The project is
designed as a manageable course implementation that combines a practical
recommendation pipeline with interpretable outputs.

## Project Overview

The goal is to build a simple recommender system that learns user and item
representations from rating data. The model predicts how much a user may like a
movie by comparing learned user and movie embeddings, for example through a dot
product interaction.

The project also includes an explainability component. Instead of only producing
recommendations, the system should help explain why specific movies are suggested
to a user.

## Objectives

- Build a recommendation pipeline using PyTorch.
- Train a matrix factorization model with user and movie embeddings.
- Evaluate recommendation quality with standard metrics.
- Generate top-k movie recommendations for users.
- Add explainability through embedding analysis and visualizations.
- Keep the implementation simple, reproducible, and suitable for a course project.

## Dataset

The primary dataset candidate is **MovieLens Latest Small** by GroupLens.

MovieLens Latest Small is a good starting point because it is lightweight,
well-known, publicly available, and realistic enough for building and evaluating a
recommendation model.

Alternative dataset ideas:

- [Case Recommender datasets](https://github.com/caserec/Datasets-for-Recommender-Systems)
- [UCSD recommender datasets](https://cseweb.ucsd.edu/~jmcauley/datasets.html)
- [Kaggle dataset discussion](https://www.kaggle.com/discussions/general/447175)
- [Steam Video Games dataset](https://www.kaggle.com/datasets/tamber/steam-video-games/data)

The final dataset should be selected based on project scope, availability, and
relevance to the course theme of AI for industry and environment.

## Planned Approach

1. **Data preparation**
   - Download and inspect the dataset.
   - Clean ratings and item metadata.
   - Encode user and item identifiers.
   - Split data into train, validation, and test sets.
   - Build PyTorch `Dataset` and `DataLoader` objects.

2. **Modeling**
   - Implement a matrix factorization model in PyTorch.
   - Learn user embeddings and movie embeddings.
   - Predict ratings from embedding interactions.
   - Optionally add user and item bias terms.

3. **Training**
   - Train the model with a suitable regression loss.
   - Tune basic hyperparameters such as embedding size, learning rate, batch size,
     and number of epochs.
   - Track training and validation performance.

4. **Evaluation**
   - Measure prediction quality with metrics such as RMSE and MAE.
   - Generate top-5 or top-10 recommendations for selected users.
   - Compare predicted recommendations with known user preferences.

5. **Explainability**
   - Analyze learned user and movie embeddings.
   - Use dimensionality reduction such as PCA for visualization.
   - Explain recommendations through similar movies, embedding proximity, and user
     preference patterns.

## Team Roles

| Role | Responsibility |
| --- | --- |
| Data Engineer | Downloads the data, cleans it, and builds the PyTorch dataset pipeline. |
| Model Architect | Implements the matrix factorization model and embedding layers. |
| Training Specialist | Builds the training loop, selects optimizer/loss, and tunes hyperparameters. |
| Explainability Specialist | Designs visualizations and explanations for recommended movies. |
| Evaluation & Integration | Computes final metrics, implements top-k recommendations, and prepares the final notebook. |

## Expected Repository Structure

The repository is currently at the planning stage. A possible structure for the
implementation is:

```text
.
|-- data/                  # Local datasets, ignored by git
|-- notebooks/             # Exploratory analysis and final Colab notebook
|-- src/
|   |-- data/              # Dataset loading and preprocessing
|   |-- models/            # Matrix factorization model
|   |-- training/          # Training and evaluation loops
|   |-- explainability/    # Embedding analysis and visualizations
|   `-- recommendations/   # Top-k recommendation utilities
|-- tests/                 # Unit and integration tests
|-- prompt.txt             # Initial project notes
`-- README.md
```

## Suggested Tech Stack

- Python
- PyTorch
- pandas
- NumPy
- scikit-learn
- Matplotlib or Seaborn
- Jupyter Notebook or Google Colab

## Getting Started

The implementation has not been added yet. Once the project code is available,
the expected workflow will be:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For notebook-based development, the project can also be developed in Google
Colab:

[Project Colab notebook](https://colab.research.google.com/drive/1CfgSGxnJeyC77AbjqF-7Mlu6jQYkmty3?usp=sharing)

## Evaluation Plan

Recommended metrics and checks:

- RMSE for rating prediction quality.
- MAE for average absolute prediction error.
- Top-k recommendation examples for qualitative review.
- Embedding visualizations for interpretability.
- Short explanation for each selected recommendation example.

## Project Status

Current status: **topic proposal and repository initialization**.

Next steps:

1. Confirm the final dataset.
2. Add the project structure.
3. Implement data loading and preprocessing.
4. Build the matrix factorization model.
5. Train, evaluate, and explain recommendations.

## Project Proposal Summary

Tentative title:

**Building and Explaining a Movie Recommender System using Matrix Factorization**

The project proposes a recommender system trained on a public dataset such as
MovieLens. It uses matrix factorization to learn user and item embeddings, then
evaluates predictions with standard metrics and adds an explainability layer to
show why particular movies are recommended.
