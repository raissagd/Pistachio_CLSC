# Pistachio Supply Chain Optimization using Enhanced Metaheuristics

[![Research](https://img.shields.io/badge/Type-Research-blue.svg)](https://github.com/andre-batista/Pistachio_CLSC)
[![Status](https://img.shields.io/badge/Status-Active-green.svg)](https://github.com/andre-batista/Pistachio_CLSC)

## 📊 Overview

This repository contains the implementation and analysis of enhanced metaheuristic algorithms for optimizing pistachio supply chain networks. The research focuses on comparing Variable Neighborhood Search (VNS) against traditional population-based algorithms and exact methods.

## 👥 Authors

- **[Raissa Gonçalves Diniz](https://github.com/raissagd)**
- **[André Costa Batista](https://github.com/andre-batista)**

## 📝 Abstract

Supply chains are vital for the agricultural sector, particularly for high-value crops like pistachios, where efficient management can enhance both economic growth and sustainability. Although there has been research on optimizing pistachio supply chains, most studies rely heavily on population-based algorithms to solve these problems. 

In this study, we propose to apply a **Variable Neighborhood Search (VNS)** algorithm and compare its performance against a population-based metaheuristic (Genetic Algorithm, GA) and an exact method. Our findings reveal that VNS consistently outperforms GA in both execution time and objective function value, particularly for larger instances. Additionally, despite a slight compromise in the final solution evaluation, VNS reduces execution time by nearly **97%** compared to the exact method in some of the larger instances.

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Required dependencies (see `requirements.txt`)

### Installation
```bash
git clone https://github.com/andre-batista/Pistachio_CLSC.git
cd Pistachio_CLSC
pip install -r requirements.txt
```

## 📁 Repository Structure

```
├── Classes/       # Source code
├── data/          # Input datasets
├── experiments/   # Experimental results
├── tests/         # Unit tests and others tests
└── README.md      # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.