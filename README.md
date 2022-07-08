# FeaturesAnalyzer

<p align="center">
  <img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white"/>
  <img src="https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white"/>
  <img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
</p>

## Regression analysis system, classification and prediction of temporal series

<br></br>

### **🚧 Needs attention**

Temporarily to use this platform you need to add the data to the Data/Dump Director, with the Name:

```txt
    dump_[YYYY-MM-DD-HH-mm-SS].csv
```

In addition, several settings and several internal are still related to the original problem of the analysis platform.Além disso várias configurações e várias internas ainda são relativas ao problema original da plataforma de análise.

### - **Requirements**

- Python3.10.4 or higher

### - **Installation**

- With pip:

```sh
╭─user@host ~/FeaturesAnalyzer ‹main●›
╰─$ pip install -r requirements.txt
```

- With pipenv:

```sh
╭─user@host ~/FeaturesAnalyzer ‹main●›
╰─$ pipenv install --python 3.10.4
```

### - **Usage**

```sh
╭─user@host ~/FeaturesAnalyzer/src/ ‹main●›
╰─$ python main.py
```

Opinionally you can use Docker 🐋:

- To gain access to the graphic interface perform:

```sh
╭─user@host ~/FeaturesAnalyzer/src/ ‹main●›
╰─$ chmod +x ./pre-build.sh

╭─user@host ~/FeaturesAnalyzer/src/ ‹main●›
╰─$ ./pre-build.sh
```

- Finnaly, you can use the graphical interface:

```sh
╭─user@host ~/FeaturesAnalyzer/src/ ‹main●›
╰─$ docker-compose up --build
```

## Development

🚧 **Needs Attention**

It is possible to need some changes in [docker-compose.yml](docker-compose.yml) so that the project works properly with docker.

## Maintenance

If you need to install any dependence, use Pipenv.

- Basic tutorial on Pipenv: [Pipenv](https://docs.pipenv.org/basics/)

- After altering some dependence, use the command below to ensure a freeze of the project's depths.

```sh
╭─user@host ~/FeaturesAnalyzer ‹main●›
╰─$ chmod +x update_reqs.sh

╭─user@host ~/FeaturesAnalyzer ‹main●›
╰─$ ./update_reqs.sh
```

---

<p align="center">
  <strong> Maded with 💙 by: </strong>
  <p align="center">
    <a href="https://github.com/OakAnderson">
      <img src="https://github.com/OakAnderson.png" width="50" height="50" alt="OakAnderson" />
    </a>
    <a href="https://github.com/ZauJulio">
      <img src="https://github.com/ZauJulio.png" width="50" height="50" alt="OakAnderson" />
    </a>
    <a href="https://avatars.githubusercontent.com/u/6580651?v=4">
      <img src="https://avatars.githubusercontent.com/u/6580651?v=4.png" width="50" height="50" alt="OakAnderson" />
    </a>
  </p>
</p>
